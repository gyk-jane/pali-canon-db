import psycopg2
from prefect import task, flow

def connect_to_db():
    conn = psycopg2.connect(
        host='localhost',
        dbname='pali_canon',
        user='dbadmin',
        password='root'
    )
    return conn

def get_postgres_data(schema, table_name) -> list:
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

def split_into_batches(data, batch_size):
    """Splits data into batches of specified size."""
    for i in range(0,len(data), batch_size):
        yield data[i:i + batch_size]