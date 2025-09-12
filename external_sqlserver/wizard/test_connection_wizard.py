from odoo import models, fields, api

class TestConnectionWizard(models.TransientModel):
    _name = "sqlserver.test.connection.wizard"
    _description = "Probar conexión SQL Server"

    result = fields.Text("Resultado", readonly=True)

    @api.model
    def default_get(self, fields_list):
        """Ejecutar la prueba al abrir el wizard"""
        defaults = super().default_get(fields_list)
        try:
            connector = self.env['sqlserver.connector']
            rows = connector.run_query("SELECT @@VERSION;")
            defaults['result'] = rows[0][0] if rows else "Sin respuesta"
        except Exception as e:
            defaults['result'] = f"❌ Error: {e}"
        return defaults
