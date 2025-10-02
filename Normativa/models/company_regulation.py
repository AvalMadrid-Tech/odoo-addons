from odoo import models, fields, api, http
from odoo.http import request
from odoo.exceptions import UserError
import subprocess
import json


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
    active = fields.Boolean("Activo (Odoo)", default=True)
    status = fields.Selection(
        [
            ("active", "Activo"),
            ("revoked", "Derogado"),
        ],
        string="Estatus",
        default="active",
        required=True
    )
    status_class = fields.Char(
        string="Estatus (coloreado)",
        compute="_compute_status_class",
        store=False
    )

    # =====================
    # Métodos de acciones
    # =====================
    def action_download_document(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/company_regulation/download/{self.id}',
            'target': 'self',
        }

    def action_preview_document(self):
        self.ensure_one()
        if self.document and self.document_filename:
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{self._name}/{self.id}/document/{self.document_filename}',
                'target': 'new',
            }

    @api.depends("status")
    def _compute_status_class(self):
        for rec in self:
            if rec.status == "active":
                rec.status_class = "text-success fw-bold"
            elif rec.status == "revoked":
                rec.status_class = "text-danger fw-bold"
            else:
                rec.status_class = ""


class CompanyRegulationController(http.Controller):

    @http.route('/company_regulation/download/<int:record_id>', type='http', auth='user')
    def download_regulation(self, record_id, **kwargs):
        record = request.env['company.regulation'].browse(record_id)
        if not record or not record.document:
            return request.not_found()

        filecontent = record.document
        filename = record.document_filename or "documento.bin"

        return request.make_response(
            filecontent,
            headers=[
                ('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', f'attachment; filename="{filename}"'),
            ]
        )


class CompanyRegulationCategory(models.Model):
    _name = "company.regulation.category"
    _description = "Categoría de Normativas"

    name = fields.Char("Nombre de la categoría", required=True)
    description = fields.Text("Descripción")
    parent_id = fields.Many2one("company.regulation.category", string="Categoría padre")
    child_ids = fields.One2many("company.regulation.category", "parent_id", string="Subcategorías")
    regulation_ids = fields.One2many("company.regulation", "category_id", string="Normativas")

    def action_llm(self):
        categories = self.search([])  # todas las categorías
        try:
            result = subprocess.run(
                ["/home/gsr/llm_import/.venv/bin/python3",
                "/home/gsr/llm_import/agent_import_odoo.py"],
                capture_output=True,
                text=True,
                check=True
            )
            salida = result.stdout.strip() if result.stdout else "{}"
        except subprocess.CalledProcessError as e:
            raise UserError(f"Error al ejecutar el LLM:\n{e.stderr}")

        try:
            data = json.loads(salida)
            print(data)
        except json.JSONDecodeError:
            data = {}

        total = data.get("total_docs", 0)
        activos = data.get("active_docs", 0)
        derogados = data.get("revoked_docs", 0)
        omitidos = data.get("skipped_docs", 0)

        # 🎨 Formateo HTML bonito
        mensaje_html = f"""
            <h3 style="color:#4a90e2;">📊 Resumen importación</h3>
            <p><b>Total documentos:</b> {total}</p>
            <p><span style="color:green;">✔ Activos:</span> {activos}</p>
            <p><span style="color:red;">✘ Revocados:</span> {derogados}</p>
            <p><span style="color:gray;">➖ Omitidos:</span> {omitidos}</p>
        """

        wizard = self.env['import.summary.wizard'].create({
            'message': mensaje_html
        })

        return {
            "name": "Resumen de Importación",
            "type": "ir.actions.act_window",
            "res_model": "import.summary.wizard",
            "view_mode": "form",
            "res_id": wizard.id,
            "target": "new",
        }
        
