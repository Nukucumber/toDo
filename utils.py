import sqlite3

db_name = "data"

def get_db_connection():
    return sqlite3.connect(f'{db_name}.sqlite')