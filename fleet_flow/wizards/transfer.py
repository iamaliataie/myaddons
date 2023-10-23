from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductQuantity(models.TransientModel):
    _name = "product.quantity.transient"

    product_id = fields.Many2one("product.product", readonly=True)
    image = fields.Image(related="product_id.image_128")
    quantity = fields.Integer(readonly=True)
    quantity_transfer = fields.Integer()
    transfer_id = fields.Many2one("transfer")

    @api.constrains("quantity_transfer")
    def _check_transfer_quantity(self):
        for rec in self:
            if rec.quantity < rec.quantity_transfer:
                raise ValidationError("Can't transfer more than existing quantity")



class Transfer(models.TransientModel):
    _name = "transfer"

    product_ids = fields.One2many("product.quantity.transient", "transfer_id")
    dest_location_id = fields.Many2one("stock.location")
    source_location_id = fields.Many2one("stock.location")

    def action_transfer(self):
        for rec in self:
            stock_picking = self.env["stock.picking"].create(
                {
                    "location_id": rec.source_location_id.id,
                    "location_dest_id": rec.dest_location_id.id,
                    "picking_type_id": self.env.context["picking_type_id"],
                    "move_type": "direct",
                }
            )
            stock_picking.location_dest_id = rec.dest_location_id.id

            for product in rec.product_ids:
                if product.quantity_transfer < 1:
                    continue
                self.env["stock.move"].create(
                    {
                        "name": product.product_id.name,
                        "product_id": product.product_id.id,
                        "product_uom_qty": product.quantity_transfer,
                        "quantity_done": product.quantity_transfer,
                        "product_uom": product.product_id.uom_id.id,
                        "reserved_availability": product.quantity_transfer,
                        "picking_id": stock_picking.id,
                        "location_id": stock_picking.location_id.id,
                        "location_dest_id": stock_picking.location_dest_id.id,
                    }
                )

            stock_picking.action_confirm()
            stock_picking.action_assign()
            return {
                "name": "Return Products",
                "res_model": "stock.picking",
                "res_id": stock_picking.id,
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "context": {"van_id": self.env.context["van_id"], "state": "unload", "transfer": rec},
            }
