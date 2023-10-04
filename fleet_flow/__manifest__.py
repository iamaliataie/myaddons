# -*- coding: utf-8 -*-
{
    "name": "fleet_flow",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "My Company",
    "website": "https://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    "application": True,
    "sequence": -1001,
    # any module necessary for this one to work correctly
    "depends": ["base", "stock"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/fleetflow_van.xml",
    ],
    "qweb": ["views/pos_location_filter.xml"],
    "assets": {
        "web.assets_backend": [
            "static/src/js/pos_location_filter.js",  # Path to your JavaScript file
        ],
    },
    # only loaded in demonstration mode
    "demo": [],
}
