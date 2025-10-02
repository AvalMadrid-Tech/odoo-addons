{
    'name': 'Normativas de la Empresa',
    'version': '1.0',
    'summary': 'Gestión de normativas internas de AvalMadrid',
    'description': """
Módulo para la gestión de normativas internas de la empresa.
Permite:
- Subir y almacenar documentos (PDF, DOCX, etc.)
- Clasificar normativas por categorías
- Definir responsables y fechas de publicación/vencimiento
- Marcar normativas de cumplimiento obligatorio
""",
    'author': 'AvalMadrid',
    'website': 'https://www.avalmadrid.es',
    'category': 'Human Resources',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/Normativa_view.xml',
        'views/import_summary_wizard.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
