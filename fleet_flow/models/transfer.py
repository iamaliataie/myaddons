from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VanProductQuantity(models.Model):
    _name = "van.product.quantity"

    product_id = fields.Many2one("product.product", readonly=True)
    image = fields.Image(related="product_id.image_128")
    quantity = fields.Integer(readonly=True)
    transfer_id = fields.Many2one("van.transfer")


class VanTransfer(models.Model):
    _name = "van.transfer"

    product_ids = fields.One2many("van.product.quantity", "transfer_id")
    dest_location_id = fields.Many2one("stock.location")
    source_location_id = fields.Many2one("stock.location")
    van_id = fields.Many2one("fleetflow.van")
    type = fields.Selection([
        ("in", "In"),
        ("out", "Out"),
    ])
