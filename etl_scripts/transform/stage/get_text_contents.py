import os
import sys
import json
import logging
from bs4 import BeautifulSoup
from prefect_dask import DaskTaskRunner
from prefect import task, flow, unmapped
from etl_scripts.util import connect_to_db, split_into_batches

def clean_text_content(file_path: str) -> str:
    file_name = file_path.split('/')[-1]
    file_type = file_name.split('.')[-1].lower()
    
    if file_type == 'html':
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            text = soup.get_text(separator=' ')
        return text
    
    if file_type == 'json':
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Concatenate all values from the json
            text = " ".join(value for value in data.values()).strip()
        return text
    
    raise ValueError(f'Unsupported file type: {file_type}')

@task(log_prints=True)
def process_translations_batch(translations_batch: list, schema: str, table_name: str):
    conn = None
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        for translation in translations_batch:
            _key, file_path = translation
            if file_path:
                if not os.path.exists(file_path):
                    print(f'File not found: {file_path}')
                    print(os.getcwd())
                    break
                try:
                    text_content = clean_text_content(file_path).strip()
                    cur.execute(f"""
                                UPDATE {schema}."{table_name}"
                                SET text_content = %s
                                WHERE _key = %s
                                """, (text_content, _key))
                except Exception as e:
                    print(f'Error processing translation {_key}: {e}')
        conn.commit()
        cur.close()
    except Exception as e:
        print.error(f'Error processing batch: {e}')
    finally:
        if conn:
            conn.close()

@flow(log_prints=True, task_runner=DaskTaskRunner(cluster_kwargs={"n_workers": 1, 
                                                                  "threads_per_worker": 10,
                                                                  "processes": False}))
def update_translations_in_parallel(schema, table_name, batch_size=500):
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(f"""
                SELECT _key, local_file_path
                FROM {schema}."{table_name}"
                """)
    translations = cur.fetchall()
    conn.close()

    batches = list(split_into_batches(translations, batch_size))
    process_translations_batch.map(batches, unmapped(schema), unmapped(table_name))
    
    