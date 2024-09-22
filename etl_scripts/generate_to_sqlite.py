import sqlite3
import psycopg2 
import etl_scripts.util as util

# Connect to postgres db
pg_conn = util.connect_to_db()

# Connect to sqlite db
sqlite_conn = sqlite3.connect('data_dump/PaliCanon.db')

# Get all dev_erd tables from postgres db
pg_cur = pg_conn.cursor()
pg_cur.execute("""
                  select table_name
                  from information_schema.tables
                  where table_schema = 'dev_erd'
                  """)
tables = pg_cur.fetchall()

# Loop through all tables and copy data from postgres to sqlite
for table in tables:
    table_name = table[0]
    
    # Create same table in sqlite
    pg_cur.execute(f"""
                   select column_name, data_type
                   from information_schema.columns
                   where table_name = '{table_name}'
                   and table_schema = 'dev_erd'
                   """)
    columns = pg_cur.fetchall()
    
    column_defs = []
    for column_name, data_type in columns:
        sqlite_type = 'TEXT'
        if data_type in ['integer', 'bigint']:
            sqlite_type = 'INTEGER'
        elif data_type in ['numeric', 'real', 'double precision']:
            sqlite_type = 'REAL'
        column_defs.append(f'{column_name} {sqlite_type}')
        
    create_table_sql = f'create table {table_name} ({', '.join(column_defs)})'
    sqlite_conn.execute(create_table_sql)
    
    # Fetch data from postgres
    pg_cur.execute(f'select * from dev_erd."{table_name}"')
    rows = pg_cur.fetchall()        
    
    # Insert data into sqlite
    insert_sql = f"""
                insert into {table_name} 
                values ({', '.join(['?' for _ in range(len(columns))])})
                """
    sqlite_conn.executemany(insert_sql, rows)
    
sqlite_conn.commit()
pg_cur.close()
pg_conn.close()
sqlite_conn.close()

print("Data transferred to SQLite")
