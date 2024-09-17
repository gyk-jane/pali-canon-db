import json
from prefect import task

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
def insert_to_db(data, conn, schema, table_name) -> None:
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
        