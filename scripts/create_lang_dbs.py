import sqlite3
import os
from scripts.utils import (
    setup_logging,
    connect_to_basket_db,
    extract_table_data,
    create_tables,
    get_column_names_from_table
)

# Set up logging
logger = setup_logging('create_lang_db.log')

def extract_data_by_lang(basket: str, lang: str) -> dict:
    """
    Extracts data from the database for a specific language.

    Parameters:
    - basket (str): The name of the basket database.
    - lang (str): The language to extractå data for.

    Returns:
    - dict: A dictionary containing the extracted data 
    for the specified language, including tables: 'TextInfo', 
    'Authors', 'Languages', 'Translations', and 'LeafLineage'.
    """
    
    conn = connect_to_basket_db(basket)
    cursor = conn.cursor()
    
    # Extract Translations by language
    cursor.execute(f"""
                   SELECT * FROM Translations
                   WHERE lang = '{lang}'
                   """)
    translations = cursor.fetchall()
    
    # Extract all other tables
    authors = extract_table_data(cursor, 'Authors')
    languages = extract_table_data(cursor, 'Languages')
    textinfo = extract_table_data(cursor, 'TextInfo')
    leaflineage = extract_table_data(cursor, 'LeafLineage') 
    conn.close()
    
    return {
        'TextInfo': textinfo,
        'Authors': authors,
        'Languages': languages,
        'Translations': translations,
        'LeafLineage': leaflineage
    }
        
def create_lang_db(basket: str, lang: str, data: str) -> None:
    """
    Create a language-specific database and insert data into tables.

    Args:
        basket (str): The name of the basket.
        lang (str): The language of the data.
        data (str): The data to be inserted into tables.

    Returns:
        None
    """
    db_dir = 'data/output/lang_dbs'
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    db_name = f'{basket}_{lang}.db'
    db_path = os.path.join(db_dir, db_name)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create tables
    create_tables(basket, lang)
    
    # Insert data by lang into tables
    for table, rows in data.items():
        columns_list = get_column_names_from_table(cursor, table)
        columns = ', '.join(columns_list)
        placeholder = ', '.join('?' * len(columns.split(', ')))
        query = f"""
        INSERT INTO {table} ({columns})
        VALUES ({placeholder})
        """
        for row in rows:
            query = f"""
                    INSERT INTO {table} ({columns})
                    VALUES ({placeholder})
                    """
            cursor.execute(query, row)
    conn.commit()
    conn.close()
        
def main():
    baskets = ['sutta', 'vinaya', 'abhidhamma']
    languages = ['en', 'pli']
    
    for basket in baskets:
        for lang in languages:
            data = extract_data_by_lang(basket, lang)
            create_lang_db(basket, lang, data)
            
if __name__ == '__main__':
    main()          
        