from odoo import models, fields, api

class CompanyRegulation(models.Model):
    _name = "company.regulation"
    _description = "Normativas de AvalMadrid"

    name = fields.Char("Título", required=True)
    category_id = fields.Many2one("company.regulation.category", string="Categoría", required=True)
    document = fields.Binary("Documento", attachment=True, required=True)
    document_filename = fields.Char("Nombre del archivo")
    description = fields.Text("Descripción")
    published_date = fields.Date("Fecha de publicación")
    expiration_date = fields.Date("Fecha de vencimiento")
    responsible_id = fields.Many2one("res.users", string="Responsable")
    is_mandatory = fields.Boolean("De cumplimiento obligatorio", default=True)
    active = fields.Boolean("Activo", default=True)

class CompanyRegulationCategory(models.Model):
    _name = "company.regulation.category"
    _description = "Categoría de Normativas"

    name = fields.Char("Nombre de la categoría", required=True)
    description = fields.Text("Descripción")
