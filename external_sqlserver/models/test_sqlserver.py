import os
import pyodbc
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

try:
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={os.getenv('SQLSERVER_HOST')},{os.getenv('SQLSERVER_PORT')};"
        f"DATABASE={os.getenv('SQLSERVER_DB')};"
        f"UID={os.getenv('SQLSERVER_USER')};"
        f"PWD={os.getenv('SQLSERVER_PASS')};"
        "Encrypt=no;"   # cámbialo a yes si tienes TLS configurado en SQL Server
    )

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Prueba sencilla: obtener versión de SQL Server
    cursor.execute("SELECT @@VERSION;")
    row = cursor.fetchone()
    print("✅ Conexión exitosa. Versión SQL Server:")
    print(row[0])

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Error al conectar:", e)
