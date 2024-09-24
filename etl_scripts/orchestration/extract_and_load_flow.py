from pathlib import Path
from prefect import flow
from etl_scripts.util import connect_to_db
from etl_scripts.extract import api_fetch, arangodb_fetch
from etl_scripts.load.arangodb_helpers import start_suttacentral_docker
from etl_scripts.load.load import generate_create_sql, insert_to_db


@flow(log_prints=True)
def extract_suttaplex_flow(schema: str, basket: str):
    """Extract suttaplex data from SuttaCentral API.

    Args:
        schema (str): PostgreSQL schema in which data should be placed
        basket (str): Pali canon basket to be extracted
    """    
    conn = connect_to_db()
    
    json_data = api_fetch.get_suttaplex(basket)
    table_name = f'{basket}_suttaplex_sc'
    sql = generate_create_sql(json_data, schema, table_name)
    print(sql)
    
    print(f'Creating {schema}.{table_name} in pali_canon db')
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
    except Exception as e:
        print(f'Error occured: {e}')
        
    print('Inserting data...')
    insert_to_db(json_data, conn, schema, table_name)
    
    conn.close()
    
@flow(log_prints=True)
def extract_arangodb_flow(schema: str, collections):
    """Extract data from arangodb backend db.

    Args:
        schema (str): PostgreSQL schema in which data should be placed
        collections (str): Name of arangodb collection to be extracted
    """    
    conn = connect_to_db()
    start_suttacentral_docker()
    dump_directory = Path('data_dump/arangodb-dump')
    
    for collection in collections:
        # Find the file corresponding to the collection
        relevant_files = list(dump_directory.glob(f"*{collection}*.json.gz"))
        if not relevant_files:
            print(f"No file found for collection: {collection}")
            continue
        
        # Choose the most recent file
        collection_file = relevant_files[0]
        
        # Extract the file and generate the SQL
        json_data = arangodb_fetch.extract_gz_file(str(collection_file), collection)  # Extract the JSON from the file
        create_sql = generate_create_sql(json_data, schema, f"{collection}_arangodb")
        
        print(create_sql)        
        print(f'Creating {schema}.{collection}_arangodb table')
        try:
            with conn.cursor() as cur:
                cur.execute(create_sql)
                conn.commit()
        except Exception as e:
            print(f'Error occurred: {e}')
            
        print('Inserting data...')
        insert_to_db(json_data, conn, schema, f"{collection}_arangodb")
    
    conn.close()
    
@flow(log_prints=True)
def extract_and_load_flow():
    """Flow for extraction and loading of dev_raw tables
    """
    collections = ['sc_bilara_texts', 'html_text', 'super_nav_details_edges']
    schema = 'dev_raw'
    extract_suttaplex_flow(schema, 'sutta')
    extract_suttaplex_flow(schema, 'vinaya')
    extract_suttaplex_flow(schema, 'abhidhamma')

    extract_arangodb_flow(schema, collections)
    