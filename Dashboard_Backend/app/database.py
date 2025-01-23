import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
conn_str = os.getenv('SQL_CONNECTION_STRING')

def get_db_connection():
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        print("Database connection failed:", str(e))
        return None
