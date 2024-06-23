import re
import json
import sqlite3
import logging
import pandas as pd

def decode_unicode_column(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Decodes Unicode escape sequences in the specified columns of a DataFrame.
    Args:
        df (pd.DataFrame): The DataFrame containing the columns to be decoded.
        columns (list): A list of column names to decode.
    Returns:
        pd.DataFrame: The DataFrame with the specified columns decoded.
    """
    decode_unicode_escape = lambda s: s.encode().decode('unicode-escape') \
        if isinstance(s, str) and re.search(r'\\u[0-9a-fA-F]{4}', s) else s
    
    for column in columns:
        if column in df.columns:
            df[column] = df[column].apply(decode_unicode_escape)
    return df

def convert_to_json_string(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the values in columns of a DataFrame to JSON strings 
    if they are of type list, dict, tuple, or set.
    Args:
        df (pd.DataFrame): The DataFrame containing the data.
    Returns:
        pd.DataFrame: The DataFrame with the specified 
        column values converted to JSON strings.
    """
    return df.map(lambda x: json.dumps(x) if isinstance(x, (list, dict, tuple, set)) else x)

def fix_json_format(json_str: str) -> json:
    """
    Fixes the JSON format by replacing single quotes with double quotes.
    
    Args:
        json_str (str): The JSON string to be fixed.
        
    Returns:
        json: The fixed JSON object.
    """
    # Replace python None with JSON null and lowercase False and True
    json_str = json_str.replace('None', 'null')
    json_str = json_str.replace('False', 'false')
    json_str = json_str.replace('True', 'true')
    
    
    # This pattern captures characters before and after the single quote 
    # and replaces single quotes with double quotes for JSON keys
    fixed_json_str = re.sub(r"(\{|\, )'(\w+)':", r'\1"\2":', json_str)
    fixed_json_str = re.sub(r": '([^']*)'", r': "\1"', fixed_json_str)
    
    try:
        return json.loads(fixed_json_str)
    except Exception as e:
        print(f"Error: {e}")
        print(fixed_json_str)
        return None
    
def connect_to_preprocess_db() -> sqlite3.Connection:
    """
    Connects to the preprocess.db SQLite database.
    
    Returns:
        sqlite3.Connection: The connection object.
    """
    path = 'data/processed/preprocess.db'
    return sqlite3.connect(path)

def connect_to_basket_db(basket: str) -> sqlite3.Connection:
    """
    Connects to the specified SQLite database.
    
    Args:
        basket (str): The name of the database to connect to.
        
    Returns:
        sqlite3.Connection: The connection object.
    """
    path = f'data/output/{basket}.db'
    return sqlite3.connect(path)

def get_file_contents(file_path: str):
    """
    Read and return the contents of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str or dict or None: The contents of the file as a string, 
        a dictionary (if the file is a JSON file), 
        or None if the file is not found or the file_path is empty.

    """
    if pd.isna(file_path):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            if '.json' in file_path:
                return json.load(file)
            return file.read()
    except FileNotFoundError:
        return None
    
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

def setup_logging(log_file):
    """
    Set up the logging configuration and return a logger instance.

    Args:
        log_file (str): The file to which logs should be written.

    Returns:
        logging.Logger: Configured logger instance.
    """
    log_path = f'data/logs/{log_file}'
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, mode='w'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    return logger
