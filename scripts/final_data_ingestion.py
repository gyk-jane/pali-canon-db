import json
import sqlite3
import pandas as pd
from scripts.utils import (
    convert_to_json_string, 
    connect_to_preprocess_db, 
    connect_to_basket_db)
from scripts.preprocessing.data_cleanup import cleanup_sutta_authors

def ingest_authors(basket: str) -> None:
    # Reference table for authors
    # Getting distinct authors from the translations data
    conn = connect_to_preprocess_db()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT DISTINCT author, author_short, author_uid
                      FROM {basket}_translations_json""")
    authors = cursor.fetchall()
    conn.close()
    
    # Preparing data for insertion into tipitaka-db
    author_fullname = [value[0] for value in authors]
    author_short = [value[1] for value in authors]
    author_uid = [value[2] for value in authors]
    df = pd.DataFrame({'author_uid': author_uid,
                       'author_short': author_short,
                       'author_fullname': author_fullname})
    if basket == 'sutta':
        df = cleanup_sutta_authors(df)

    conn = connect_to_basket_db(basket)    
    df.to_sql('Authors', conn, if_exists='replace', index=False)
    conn.close()
    
def ingest_languages(basket: str) -> None:
    # Reference table for languages
    # Getting distinct languages from the translations data
    conn = connect_to_preprocess_db()
    cursor = conn.cursor()
    cursor.execute(f"""SELECT DISTINCT lang, lang_name
                      FROM {basket}_translations_json""")
    languages = cursor.fetchall()
    conn.close()
    
    # Preparing data for insertion into tipitaka-db
    lang = [value[0] for value in languages]
    lang_name = [value[1] for value in languages]
    df = pd.DataFrame({'lang': lang, 
                       'lang_name': lang_name})
    
    conn = connect_to_basket_db(basket)
    df.to_sql('Languages', conn, if_exists='replace', index=False)
    
def ingest_textinfo(basket: str) -> None:
    # Get data from preprocess.db
    conn = connect_to_preprocess_db()
    cursor = conn.cursor()
    cursor.execute(f'SELECT uid, parent_uid FROM {basket}_menu_children_denorm')
    denorm_table = cursor.fetchall()
    cursor.execute(f"""SELECT uid, blurb, original_title, translated_title, acronym, 
                   difficulty, root_lang_name, root_lang, type 
                   FROM {basket}_json""")
    basket_json_table = cursor.fetchall()
    conn.close()
    
    # Connect to {basket}_db to ingest data
    conn = connect_to_basket_db(basket)
    cursor = conn.cursor()
    
    # Add root node
    cursor.execute(f"""
                   INSERT INTO TextInfo (uid, parent_uid)
                   VALUES (?, ?)""", (basket, 'pitaka'))
    
    # Iterate over {basket}_menu_children_denorm in preprocess.db to get uid and parent_uid
    for row in denorm_table:
        uid, parent_uid = row
        
        # Insert into table
        cursor.execute(f"""
                       INSERT INTO TextInfo (uid, parent_uid)
                       VALUES (?, ?)""", (uid, parent_uid))
        
    # Iterate over sutta_json to ingest additional information
    for row in basket_json_table:
        uid, blurb, original_title, translated_title, \
            acronym, difficulty, root_lang_name, \
                root_lang, type = row
        
        # Insert into table
        cursor.execute(f"""
                       UPDATE TextInfo
                       SET blurb = ?, 
                           original_title = ?, 
                           translated_title = ?, 
                           acronym = ?, 
                           difficulty = ?, 
                           root_lang_name = ?, 
                           root_lang = ?, 
                           type = ?
                        WHERE uid = ?""", (blurb, original_title, translated_title, acronym,
                                          difficulty, root_lang_name, root_lang, type, uid))
        conn.commit()
    conn.close()
        
def ingest_leaflineage(basket: str) -> None:
    # Get distinct uid from {basket}_translations_json
    conn = connect_to_preprocess_db()
    lineage_df = pd.read_sql_query(f"""SELECT distinct uid 
                                   FROM {basket}_translations_json""", conn)
    
    # Connect to {basket}_db to ingest data
    conn = connect_to_basket_db(basket)
    
    # Retrieves the fullpath of a given uid
    def get_lineage(db: sqlite3, uid: str) -> list:
        lineage = []
        while uid is not None:
            cursor = db.execute("SELECT parent_uid FROM TextInfo WHERE uid = ?", (uid,))
            result = cursor.fetchone()
            if not result:
                break
            parent_uid = result[0]
            lineage.append(parent_uid)
            uid = parent_uid
        return lineage   
     
    # Ingest lineage to df
    lineage_df['lineage'] = lineage_df['uid'].apply(lambda x: get_lineage(conn, x))
    
    # Ingest lineage_df to {basket}_db
    lineage_df['lineage'] = lineage_df['lineage'].apply(json.dumps)
    lineage_df.to_sql('LeafLineage', conn, if_exists='replace', index=False)
    conn.close()
    
def ingest_translations(basket: str) -> None:
    # Connect to preprocess.db to get translations data
    conn = connect_to_preprocess_db()
    predb_translations_df = pd.read_sql_query(f"SELECT * FROM {basket}_translations_json", conn)
    
    # Ingest from predb_translations_df
    translations_df = predb_translations_df[['id', 'uid', 'lang', 'author_uid']]
    
    # Get actual text from Github/sc_data
    html_text_df = pd.read_sql_query("SELECT * FROM html_text", conn)
    sc_bilara_texts_df = pd.read_sql_query("SELECT * FROM sc_bilara_texts", conn)
    conn.close()
    
    # Merge html_text_df with translations_df
    merged_df = translations_df.merge(html_text_df[['_key', 'file_path']], left_on='id',
                                      right_on='_key', how='left')
    # Merge sc_bilara_texts with merged_df
    merged_df = merged_df.merge(sc_bilara_texts_df[['_key', 'file_path']], left_on='id',
                                right_on='_key', how='left',
                                suffixes=('_html', '_sc_bilara'))
    
    # Drop _key_html and _key_sc_bilara since they are the same as `id`
    merged_df = merged_df.drop(columns=['_key_html', '_key_sc_bilara'])
    # Combine file_path_html and file_path_sc_bilara into file_path
    merged_df['file_path'] = merged_df['file_path_html'].combine_first(merged_df['file_path_sc_bilara'])
    merged_df = merged_df.drop(columns=['file_path_html', 'file_path_sc_bilara'])
    merged_df['file_path'] = merged_df['file_path'].str.replace('^/opt/sc/sc-flask/', '', regex=True)
    
    # Note the suttas which don't have a corresponding text/translation
    missing_text = merged_df[merged_df['file_path'].isnull()]
    missing_text.to_csv(f'{basket}_missing_text.csv', index=False)
    
    # Populate `text` column using `file_path`
    def get_file_contents(file_path: str):
        if pd.isna(file_path):
            return None
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                if '.json' in file_path:
                    return json.load(file)
                return file.read()
        except FileNotFoundError:
            return None
                
    merged_df['text'] = merged_df['file_path'].apply(get_file_contents)
    
    # ingest merged_df to {basket}_db
    conn = connect_to_basket_db(basket)
    merged_df = convert_to_json_string(merged_df)
    merged_df.to_sql('Translations', conn, if_exists='replace', index=False)
    