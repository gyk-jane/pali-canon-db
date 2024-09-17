import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from prefect import task, flow
from util.db_connection import connect_to_db
from pathlib import Path
import util.arangodb_helpers as arangodb
from extract.arangodb_fetch import extract_gz_file, export_arangodb_data
from extract.api_fetch import get_suttaplex

@task(log_prints=True)
def generate_create_sql(json_data, schema, table_name) -> str:
    """
    Generates a CREATE TABLE statement dynamically from all keys in the given JSON data.

    Args:
        json_data (json): JSON file from API get request
        table_name (string): Name of target table in Postgres

    Returns:
        str: SQL CREATE TABLE statement
    """
    all_columns = {}

    # Iterate through all records to collect all unique keys
    for rec in json_data:
        for key, value in rec.items():
            # If the key is already added, skip it
            if key not in all_columns:
                # Infer the type from the first occurrence of the key
                if isinstance(value, bool):
                    all_columns[key] = 'BOOLEAN'
                elif isinstance(value, int):
                    all_columns[key] = "INTEGER"
                elif isinstance(value, float):
                    all_columns[key] = "FLOAT"
                elif isinstance(value, dict) or isinstance(value, list):
                    all_columns[key] = "JSONB"
                else:
                    all_columns[key] = "TEXT"
    
    # Build the CREATE TABLE SQL statement
    sql = f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} ("
    columns = [f"{key} {data_type}" for key, data_type in all_columns.items()]
    sql += ", ".join(columns)
    sql += ");"
    
    return sql

@task(log_prints=True)
def load_source_to_dw(data, conn, schema, table_name) -> None:
    """Inserts data into PostgreSQL

    Args:
        data (json): Data to be ingested
        conn (psycopg2 object): Connection to data warehouse
        table_name (string): Target table name
    """
    with conn.cursor() as cur:
        for rec in data:
            # Convert dictionaries or lists to JSON strings
            for key, value in rec.items():
                if isinstance(value, (dict, list)):
                    rec[key] = json.dumps(value)
            
            keys = ", ".join(rec.keys())
            values = ", ".join(["%s"] * len(rec))
            insert_sql = f"INSERT INTO pali_canon.{schema}.{table_name} ({keys}) VALUES ({values})"            
            
            try:
                cur.execute(insert_sql, tuple(rec.values()))
            except Exception as e:
                print(f"Error {e} on: {rec.values()}")
                break
        conn.commit()
        
@flow
def html_test_flow():
    conn = connect_to_db()
    
    # html_text
    html_text_json = extract_gz_file('data_dump/arangodb-dump/html_text_8a00c848c7b3360945795d3bc52ebe88.data.json.gz')
    html_sql = generate_create_sql(html_text_json, 'raw', 'html_text_arangodb')
    print(html_sql)
    
    print('Creating raw html_text table')
    try:
        with conn.cursor() as cur:
            cur.execute(html_sql)
            conn.commit()
    except Exception as e:
        print(f'Error occurred: {e}')
        
    print('Inserting data...')
    load_source_to_dw(html_text_json, conn, 'raw', 'html_text_arangodb')
    
    conn.close()
    
@flow
def suttaplex_test_flow():
    conn = connect_to_db()
    
    # sutta
    sutta_json = get_suttaplex('sutta')
    sutta_sql = generate_create_sql(sutta_json, 'dev_raw', 'sutta_suttaplex_sc')
    print(sutta_sql)
    
    print('Creating raw sutta_suttaplex table')
    try:
        with conn.cursor() as cur:
            cur.execute(sutta_sql)
            conn.commit()
    except Exception as e:
        print(f'Error occured: {e}')
        
    print('Inserting data...')
    load_source_to_dw(sutta_json, conn, 'dev_raw', 'sutta_suttaplex_sc')
    
    conn.close()
    
@flow
def arangodb_test_exports():
    # dumping interesting arangodb collections to postgres... just playin around    
    conn = connect_to_db()
    arangodb.start_suttacentral()
    dump_directory = Path('/Users/janekim/Developer/tipitaka_db/data_dump/arangodb-dump')

    collections = ['sc_bilara_texts', 'html_text', 'super_nav_details_edges', 'super_nav_details']
    dump_path = export_arangodb_data(collections=collections)
    
    for collection in collections:
        # Find the file corresponding to the collection
        relevant_files = list(dump_directory.glob(f"*{collection}*.json.gz"))
        if not relevant_files:
            print(f"No file found for collection: {collection}")
            continue
        
        # Choose the most recent file (if there are multiple, you can adjust the selection)
        collection_file = relevant_files[0]  # You can use sorting to get the most recent if needed
        
        # Step 4: Extract the file and generate the SQL
        json_data = extract_gz_file(str(collection_file), collection)  # Extract the JSON from the file
        create_sql = generate_create_sql(json_data, 'dev_raw', f"{collection}_arangodb")
        
        # Print or execute the generated SQL
        print(create_sql)
        
        print('Creating raw html_text table')
        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                conn.commit()
        except Exception as e:
            print(f'Error occurred: {e}')
            
        print('Inserting data...')
        load_source_to_dw(json_data, conn, 'dev_raw', f"{collection}_arangodb")
    
    conn.close()
    
    
    
if __name__ ==  '__main__':
    suttaplex_test_flow()