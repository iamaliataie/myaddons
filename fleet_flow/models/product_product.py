from odoo import api, models, fields


class Product(models.Model):
    _inherit = "product.product"

    location_id = fields.Many2one("stock.location", string="Location")
