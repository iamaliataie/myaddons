from odoo import api, models, fields


class Product(models.Model):
    _inherit = "product.template"

    van_id = fields.Many2one("fleetflow.van", string="Van")
