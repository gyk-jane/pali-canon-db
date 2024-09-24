import sqlite3
import etl_scripts.util as util

def generate_to_sqlite(sqlite_filepath: str='data_dump/PaliCanon.db',
                       schema: str='dev_erd'):
    """Copies schema (and it's tables) from PostgreSQL to a sqlite PaliCanon.db

    Args:
        sqlite_filepath (str, optional): File path of target (sqlite db).
            Defaults to 'data_dump/PaliCanon.db'.
        schema (str, optional): Schema from PostreSQL db to be copied.
            Defaults to 'dev_erd'.
    """    
    # Connect to postgres db
    pg_conn = util.connect_to_db()

    # Connect to sqlite db
    sqlite_conn = sqlite3.connect(sqlite_filepath)

    # Get all schema tables from postgres db
    pg_cur = pg_conn.cursor()
    pg_cur.execute(f"""
                    select table_name
                    from information_schema.tables
                    where table_schema = '{schema}'
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
                    and table_schema = '{schema}'
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
        pg_cur.execute(f'select * from {schema}."{table_name}"')
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

if __name__ == '__main__':
    generate_to_sqlite()