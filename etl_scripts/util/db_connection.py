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

if __name__ == '__main__':
    connect_to_db()
    