from psycopg2 import pool
import json
from bs4 import BeautifulSoup
from prefect import task, flow, unmapped
from prefect_dask import DaskTaskRunner
from etl_scripts.util import split_into_batches

# Function to create the connection pool
def create_pool():
    return pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host='localhost',
        port='5432',
        dbname='pali_canon',
        user='dbadmin',
        password='root'
    )

# Function to connect to the database
def connect_to_db():
    db_pool = create_pool()  # Pool created each time within function scope
    return db_pool.getconn(), db_pool

# Task to clean file content
@task(log_prints=True)
def clean_text_content(file_path: str) -> str:
    file_name = file_path.split('/')[-1]
    file_type = file_name.split('.')[-1].lower()
    
    if file_type == 'html':
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            return soup.get_text(separator=' ')
    
    if file_type == 'json':
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return " ".join(value for value in data.values()).strip()
    
    raise ValueError(f'Unsupported file type: {file_type}')

# Task to insert cleaned text into the database
@task(log_prints=True)
def insert_texts_from_files(translations_batch: list, schema: str, table_name: str) -> None:
    conn, db_pool = connect_to_db()  # Create new connection within task
    cur = conn.cursor()

    try:
        for translation in translations_batch:
            _key, file_path = translation
            if file_path:
                text_content = clean_text_content(file_path)

                cur.execute(f"""
                    UPDATE {schema}."{table_name}"
                    SET text_content = %s
                    WHERE _key = %s
                """, (text_content, _key))
        
        conn.commit()
    finally:
        cur.close()
        db_pool.putconn(conn)  # Ensure connection is released back to pool

# Main flow to run the translation updates
@flow(task_runner=DaskTaskRunner(cluster_kwargs={"n_workers": 2, "processes": False}))
def update_translations_in_parallel(schema, table_name, batch_size=3000):
    conn, db_pool = connect_to_db()  # Create connection to fetch initial data
    cur = conn.cursor()

    cur.execute(f"""
        SELECT _key, local_file_path
        FROM {schema}."{table_name}"
    """)
    translations = cur.fetchall()

    cur.close()
    db_pool.putconn(conn)  # Release connection after fetching

    # Split into smaller batches
    batches = list(split_into_batches(translations, batch_size))
    
    # Map the insert task over the batches
    insert_texts_from_files.map(batches, unmapped(schema), unmapped(table_name))

# Main entry point
if __name__ == '__main__':
    update_translations_in_parallel('dev_stage', 'html_text_arangodb')