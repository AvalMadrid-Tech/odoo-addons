from odoo import models, api
import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()  # cargar credenciales desde .env

class SqlServerConnector(models.AbstractModel):
    _name = 'sqlserver.connector'
    _description = 'Conector genérico SQL Server'

    @api.model
    def _get_connection(self):
        conn_str = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={os.getenv('SQLSERVER_HOST')},{os.getenv('SQLSERVER_PORT')};"
            f"DATABASE={os.getenv('SQLSERVER_DB')};"
            f"UID={os.getenv('SQLSERVER_USER')};"
            f"PWD={os.getenv('SQLSERVER_PASS')};"
            "Encrypt=no;"
        )
        return pyodbc.connect(conn_str)

    @api.model
    def run_query(self, query, params=None, fetch=True):
        """Ejecuta consulta en SQL Server"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        data = cursor.fetchall() if fetch else None
        conn.commit()
        cursor.close()
        conn.close()
        return data
