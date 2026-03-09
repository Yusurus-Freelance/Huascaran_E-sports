import os
import pymysql
from dotenv import load_dotenv

# Carga las variables
load_dotenv()

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST') or 'localhost',
            user=os.getenv('DB_USER') or 'root',
            password=os.getenv('DB_PASSWORD') or '',
            database=os.getenv('DB_NAME') or 'Huascaran_E-sports',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"Error crítico al conectar a la base de datos: {e}")
        return None