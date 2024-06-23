import sqlite3
from scripts.utils import connect_to_preprocess_db, connect_to_basket_db
import pandas as pd

def cleanup_sutta_json() -> None:
    # Removing duplicates
    conn = connect_to_preprocess_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE sutta_json_temp AS SELECT DISTINCT * FROM sutta_json;")
    cur.execute("DROP TABLE sutta_json;")
    cur.execute("ALTER TABLE sutta_json_temp RENAME TO sutta_json;")
    conn.commit()
    conn.close()    
    
def cleanup_sutta_menu_children() -> None:
    # Connect to the SQLite database
    conn = connect_to_preprocess_db()

    # Create a cursor object
    cur = conn.cursor()

    # Execute the SQL command to update the uid column
    cur.execute("""
        UPDATE sutta_menu_children
        SET uid = CASE WHEN uid = 'dhp' THEN 'dhp_dharmapadas' ELSE uid END;
    """)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
        
def cleanup_sutta_menu_children_denorm() -> None:
    # Connect to the SQLite database
    conn = connect_to_preprocess_db()

    # Create a cursor object
    cur = conn.cursor()

    # Remove duplicate rows
    cur.execute("CREATE TABLE sutta_menu_children_denorm_temp AS SELECT DISTINCT * FROM sutta_menu_children_denorm;")
    cur.execute("DROP TABLE sutta_menu_children_denorm;")
    cur.execute("ALTER TABLE sutta_menu_children_denorm_temp RENAME TO sutta_menu_children_denorm;")
    
    # Update uid for `dhp` and `g2dhp` duplicates`
    cur.execute("UPDATE sutta_menu_children_denorm SET uid = 'dhp_dharmapadas' WHERE uid = 'dhp' AND parent_uid = 'dharmapadas';")
    cur.execute("UPDATE sutta_menu_children_denorm SET uid = 'g2dhp_dharmapadas' WHERE uid = 'g2dhp' AND parent_uid = 'dharmapadas';")
    print('executed')

    # cur.execute("DELETE FROM sutta_menu_children_denorm WHERE parent_uid = 'dharmapadas' AND uid = 'dhp';")
    # cur.execute("DELETE FROM sutta_menu_children_denorm WHERE parent_uid = 'g2dhp' AND uid = 'g2dhp';")
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
def cleanup_sutta_authors(df: pd.DataFrame) -> pd.DataFrame:
    # Step 1: Update duplicates with standardized values
    df['author_uid'] = df['author_uid'].str.lower()
    df['author_short'] = df['author_short'].str.lower().replace({
        'anandajoti': 'anandajoti',
        'laera': 'laera',
        'lucjan': 'lucjan',
        'patton': 'patton',
        'piyadassi': 'piyadassi',
        'sabbamitta': 'sabbamitta',
        'suddhaso': 'suddhaso',
        'sujato': 'sujato',
        'sv': 'sv'
    })
    df['author_fullname'] = df['author_fullname'].str.lower().replace({
        'anandajoti': 'bhikkhu ānandajoti',
        'laera': 'gabriel n. laera',
        'lucjan': 'paweł łucjan',
        'patton': 'charles patton',
        'piyadassi': 'piyadassi thera',
        'sabbamitta': 'sabbamitta',
        'suddhaso': 'bhante suddhāso',
        'sujato': 'bhikkhu sujato',
        'sv': 'sv theravada.ru'
    })
    
    # Step 2: Remove duplicate rows, keeping one
    df.drop_duplicates(subset='author_uid', keep='first', inplace=True)
    
    return df
