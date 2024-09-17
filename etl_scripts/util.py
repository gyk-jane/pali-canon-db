import psycopg2
from prefect import task, flow

@task(log_prints=True)
def connect_to_db() -> psycopg2.connect:
    conn = psycopg2.connect(
        host='localhost',
        dbname='pali_canon',
        user='janekim',
        password='2358'
    )
    return conn

@task(log_prints=True)
def get_postgres_data(schema, table_name) -> list:
    sql = f"""select *
    from pali_canon.{schema}.{table_name}
    """
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    conn.commit()
    cur.close()
    
    return data
