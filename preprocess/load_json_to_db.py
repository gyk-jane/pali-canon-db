"""Creates tables from the suttaplex json data for the given basket:
    1. A table for the main suttaplex data with the name {basket}_json.
    2. A table for the translations data with the name {basket}_translations_json.
"""

import json
import sqlite3
import pandas as pd
import os
import ast
from get_sc_data import get_menu_data
from util import (
    connect_to_preprocess_db, 
    decode_unicode_column,
    convert_to_json_string
)

def load_suttaplex_to_db(basket: str) -> None:
    """
    Load suttaplex data from a JSON file and write it to a SQLite database.
    Creates the following tables:
        - {basket}_json: A table for the main suttaplex data.
        - {basket}_translations_json: A table for the translations data.
    Parameters:
    - basket (str): The name of the basket to load the data from.
    Returns:
    - None
    """
    # Load suttaplex json data
    with open(f'{basket}.json', encoding='utf-8') as f:
        suttaplex_data = json.load(f)
        
    # Decode Unicode escape sequences
    columns_to_decode_suttaplex = ['blurb', 'original_title', 'root_lang_name']
    suttaplex_df = decode_unicode_column(pd.DataFrame(suttaplex_data), columns_to_decode_suttaplex)
    
    # Denormalize translations nested in the suttaplex data
    translations = []
    for _, row in suttaplex_df.iterrows():
        if row['type'] == 'leaf':
            for translation in row['translations']:
                translation['uid'] = row['uid']
                translations.append(translation)
                
    # Convert translations to a DataFrame
    columns_to_decode_translations = ['lang_name', 'author', 'author_short', 'title']
    translations_df = decode_unicode_column(pd.DataFrame(translations), columns_to_decode_translations)
    
    # Converting any columns that are of type list, dict, tuple, or set to JSON strings
    translations_df = convert_to_json_string(translations_df)
    suttaplex_df = convert_to_json_string(suttaplex_df)
    
    # Write the data to the database
    conn = connect_to_preprocess_db()
    suttaplex_df.to_sql(f'{basket}_json', conn, if_exists='replace', index=False)
    translations_df.to_sql(f'{basket}_translations_json', conn, if_exists='replace', index=False)
    conn.close()
    
def load_children_to_db(basket: str) -> None:
    """
    Load children data from menu API calls into SQLite database preprocess.db.
    Args:
        basket (str): The name of the basket.
    Returns:
        None
    """
    # Connect to the preprocess database
    conn = connect_to_preprocess_db()
    cursor = conn.cursor()
    
    if f'{basket}_children.csv' in os.listdir():
        children_df = pd.read_csv(f'{basket}_children.csv', quotechar='"')
    else:
        # Call menu on the ~1000 branches and root of the basket json
        cursor.execute(f"SELECT uid FROM {basket}_json WHERE type = 'branch' OR type = 'root'")
        parent_uids = [values[0] for values in cursor.fetchall()]
        children_df_list = []
        for uid in parent_uids:
            menu_data = get_menu_data(uid)
            children_df_list.append(pd.DataFrame(menu_data))
        children_df = pd.concat(children_df_list)
    
        # Save the children data to a .csv for future use
        children_df.to_csv(f'{basket}_children.csv', index=False)
    
    # Clean up:
    # Change 'dhp' to 'dhp_dharmapadas' if uid is 'dharmapadas'
    # Convert columns to JSON strings if they are of type list, dict, tuple, or set
    children_df = convert_to_json_string(children_df)
    
    # Write data to database
    children_df.to_sql(f'{basket}_menu_children', conn, if_exists='replace', index=False)
    
def load_denormalized_children_to_db(basket: str) -> None:
    """
    Load denormalized children data to the database.
    Args:
        basket (str): The name of the basket.
    Returns:
        None
    """
    # Load children data from table {basket}_menu_children
    conn = connect_to_preprocess_db()
    children_df = pd.read_sql(f"SELECT * FROM {basket}_menu_children", conn)
    
    # Convert 'children' to list of dictionaries for easier manipulation
    children_df['children'] = children_df['children'].apply(ast.literal_eval)
    children_df.rename(columns={"uid": "parent_uid"}, inplace=True)
    
    # Explode 'children' to separate rows
    children_df = children_df.explode('children')
    # Select only 'uid' from exploded 'children' column so that 'uid' represents the child uid of each 'parent_uid'
    children_df['uid'] = children_df['children'].apply(lambda x: x['uid'])    
    
    # Load DataFrame as new table in SQLite db
    children_df = convert_to_json_string(children_df)
    children_df.to_sql(f'{basket}_menu_children_denorm', conn, if_exists='replace', index=False)
    
def load_collections_to_db() -> None:
    """
    Load arangodb collections in /collections into preprocess.db.
    Each JSON file is converted into a pandas DataFrame, 
    which is then converted to a JSON string.
    The resulting JSON string is stored in a table in the SQLite database.
    """
    PATHS = ['collections/html_text.data.json',
             'collections/sc_bilara_texts.data.json']
    conn = connect_to_preprocess_db()
    for path in PATHS:
        with open(path, encoding='utf-8') as f:
            data = [json.loads(line) for line in f]
        df = pd.DataFrame(data)
        df = convert_to_json_string(df)
        df.to_sql(path.split('/')[1].split('.')[0], conn, 
                  if_exists='replace', index=False)
    conn.close()
    