import sqlite3
import duckdb
import pandas as pd

# Connect to the SQLite database
sqlite_conn = sqlite3.connect('fedimint-observer/fedimint_observer.db')

# Connect to a new DuckDB database
duck_conn = duckdb.connect('freedom_one-duckdb.db')

# Get a list of all tables in the SQLite database
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

# Iterate through each table and copy it to DuckDB
for table in tables:
    table_name = table[0]
    
    # Read data from SQLite
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", sqlite_conn)
    print(table_name, len(df))
    
    # Write data to DuckDB
    duck_conn.register('temp_df', df)
    duck_conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM temp_df")
    duck_conn.unregister('temp_df')

# Close connections
sqlite_conn.close()
duck_conn.close()

print("Conversion completed successfully.")