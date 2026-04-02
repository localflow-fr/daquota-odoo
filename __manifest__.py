{
    'name': 'Daquota Connector',
    'version': '17.0.1.0.0',
    'summary': 'Connect Odoo with Daquota applications like LocalFlow Maps.',
    'description': """
The Daquota Connector allows Odoo users to seamlessly open and interact with Daquota apps directly from within Odoo.
    """,
    'author': 'LocalFlow',
    'website': 'https://localflow.fr',
    'license': 'LGPL-3',
    'category': 'Tools',
    'depends': [
        'base_setup',
        'base_geolocalize',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/settings_view.xml',
        'views/localflow_views.xml',
        'views/menu_items.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}