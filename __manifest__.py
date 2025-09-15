# -*- coding: utf-8 -*-
{
    "name": "Daquota Connector",
    "summary": "Open Daquota apps from Odoo (free LocalFlow Maps included).",
    "version": "17.0.1.0.0",
    "category": "Tools",
    "author": "Renaud Pawlak",
    "website": "https://localflow.fr",
    "license": "LGPL-3",
    "depends": ["base", "web", 'partner_geolocalize'],
    "data": [
        "views/menus.xml",
        "views/settings_view.xml",
        "security/ir.model.access.csv",
        'data/sequence.xml',
    ],
    "application": True,
}
