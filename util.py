"""_summary_

Returns:
    _type_: _description_
"""

import re
import json
import sqlite3
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
    return sqlite3.connect('preprocess.db')

def connect_to_basket_db(basket: str) -> sqlite3.Connection:
    """
    Connects to the specified SQLite database.
    
    Args:
        basket (str): The name of the database to connect to.
        
    Returns:
        sqlite3.Connection: The connection object.
    """
    return sqlite3.connect(f'{basket}.db')
