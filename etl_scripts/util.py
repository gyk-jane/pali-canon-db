import psycopg2

def connect_to_db() -> psycopg2.connect:
    """Connects to PostgreSQL db pali_canon.

    Returns:
        psycopg2.connect: The db connection
    """
    conn = psycopg2.connect(
        host='localhost',
        dbname='pali_canon',
        user='dbadmin',
        password='root'
    )
    return conn

def get_postgres_data(schema: str, table_name: str) -> list:
    """Returns data from PostgreSQL table.

    Args:
        schema (str): Schema of table_name
        table_name (str): Name of the table we are fetching
            data from

    Returns:
        list: Data from schema.table_name
    """    
    sql = f"""select *
    from pali_canon.{schema}."{table_name}"
    """
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    conn.commit()
    cur.close()
    
    return data

def split_into_batches(data: list, batch_size: int) -> list:
    """Splits data into batches of specified size.
    
    Args:
        data (list): List to be separated into batches
        batch_size (int): Size of each batch
    Yields:
        list: The list batch
    """
    for i in range(0,len(data), batch_size):
        yield data[i:i + batch_size]