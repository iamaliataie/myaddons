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
    "depends": [
        "base",
        "stock",
        "point_of_sale",
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/fleetflow_van.xml",
        "wizards/transfer_view.xml",
        "wizards/van_operation_view.xml",
        "views/pos_config_view.xml",
        "views/fleetflow_van_transfer.xml",
        # "static/src/xml/fleet_flow_van.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
    "assets": {
        "web.assets_backend": [
            "fleet_flow/static/src/components/*/*.js",
            "fleet_flow/static/src/components/*/*.xml",
            "fleet_flow/static/src/components/*/*.scss",
            "fleet_flow/static/src/js/van_kanban_extend.js",
            "fleet_flow/static/src/xml/van_kanban_button.xml",
        ],
        "point_of_sale.assets": [
            "fleet_flow/static/src/pos/**/*.js",
            "fleet_flow/static/src/pos/**/*.xml",
            "fleet_flow/static/src/pos/**/*.scss",
        ],
    },
}
