import pyodbc
from config import Config

def get_connection():
    connection_string = (
        f"SERVER={Config.DB_SERVER},{Config.DB_PORT};"
        f"DATABASE={Config.DB_DATABASE};"
        f"UID={Config.DB_USER};"
        f"PWD={Config.DB_PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Connection Timeout=30;"
    )
    connection = pyodbc.connect(connection_string)
    return connection
