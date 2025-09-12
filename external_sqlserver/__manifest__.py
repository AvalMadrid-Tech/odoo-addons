{
    "name": "External SQL Server Connector",
    "version": "18.0.1.0",
    "author": "Guillermo",
    "license": "LGPL-3",
    "category": "Tools",
    "summary": "Conector genérico para SQL Server",
    "description": """
Módulo base para conexión a SQL Server desde Odoo.
Permite probar la conexión y ejecutar consultas.
    """,
    'assets': {
        'web.assets_backend': [
            'external_sqlserver/static/src/css/sqlserver_connector.css',
            ],
        },

    "depends": ["base"],
    'data': [
        'security/ir.model.access.csv',
        'security/sqlserver_security.xml',
        'views/res_config_settings_views.xml',
        'views/test_connection_wizard_views.xml',
    ],

    "application": False,
    "installable": True,
}
