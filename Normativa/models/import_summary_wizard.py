from odoo import models, fields, api

class ImportSummaryWizard(models.TransientModel):
    _name = "import.summary.wizard"
    _description = "Resumen de Importación de Normativas"

    message = fields.Html("Resumen", readonly=True)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        res["message"] = self.env.context.get("import_summary_message", "")
        return res
