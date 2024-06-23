import sqlite3
from scripts.fetch_sc_data import get_suttaplex
from scripts.utils import connect_to_basket_db
from scripts.preprocessing.data_cleanup import (
    cleanup_sutta_json,
    cleanup_sutta_menu_children,
    cleanup_sutta_menu_children_denorm
)
from scripts.final_data_ingestion import (
    ingest_textinfo, 
    ingest_leaflineage, 
    ingest_authors, 
    ingest_languages, 
    ingest_translations
)
from scripts.preprocessing.preprocessing_data_loader import (
    load_suttaplex_to_db,
    load_children_to_db,
    load_denormalized_children_to_db,
    load_collections_to_db,
)

# Get initial json data
print("Getting suttaplex data...")
get_suttaplex('sutta')
get_suttaplex('vinaya')
get_suttaplex('abhidhamma')

# Create preprocess.db
def load_preprocess(basket: str):
    load_suttaplex_to_db(basket)
    if basket == 'sutta':
        cleanup_sutta_json()
    load_children_to_db(basket)
    if basket == 'sutta':
        cleanup_sutta_menu_children()
    load_denormalized_children_to_db(basket)
    if basket == 'sutta':
        cleanup_sutta_menu_children_denorm()
print('Loading data to preprocess.db...')
load_collections_to_db()
load_preprocess('sutta')
load_preprocess('vinaya')
load_preprocess('abhidhamma')

# Create tables in tipitaka.db using tipitaka_schema.sql
def create_tables(basket: str):
    conn = connect_to_basket_db(basket)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")
    
    path = f'schemas/{basket}_schema.sql'
    with open(path, 'r') as f:
        cursor.executescript(f.read())
    conn.close()
    
# Ingest tables to tipitaka.db
print('Ingesting data to tipitaka.db...')
def ingest_data(basket: str) -> None:
    create_tables(basket)
    
    print(f'Ingesting {basket} authors...')
    ingest_authors(basket)
    print(f'Ingesting {basket} languages...')
    ingest_languages(basket)
    print(f'Ingesting {basket} textinfo...')
    ingest_textinfo(basket)
    print(f'Ingesting {basket} leaflineage...')
    ingest_leaflineage(basket)
    print(f'Ingesting {basket} translations...')    
    ingest_translations(basket)
    

print('Ingesting sutta data...')
ingest_data('sutta')
print('Ingesting vinaya data...')
ingest_data('vinaya')
print('Ingesting abhidhamma data...')
ingest_data('abhidhamma')

print('Done!')