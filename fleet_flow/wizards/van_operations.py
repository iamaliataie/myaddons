from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductQuantityUnload(models.TransientModel):
    _name = "van.operation.unload.product"

    product_id = fields.Many2one("product.product", readonly=True)
    image = fields.Image(related="product_id.image_128")
    quantity = fields.Integer(readonly=True)
    quantity_transfer = fields.Integer()
    operation_id = fields.Many2one("van.operation.unload")

    @api.constrains("quantity_transfer")
    def _check_transfer_quantity(self):
        for rec in self:
            if rec.quantity < rec.quantity_transfer:
                raise ValidationError("Can't transfer more than existing quantity")


class VanOperationUnload(models.TransientModel):
    _name = "van.operation.unload"

    product_ids = fields.One2many("van.operation.unload.product", "operation_id")
    dest_location_id = fields.Many2one("stock.location")
    source_location_id = fields.Many2one("stock.location", related="van_id.location_id")
    van_id = fields.Many2one("fleetflow.van")

    def action_transfer(self):
        for rec in self:
            stock_picking = self.env["stock.picking"].create(
                {
                    "location_id": rec.source_location_id.id,
                    "location_dest_id": rec.dest_location_id.id,
                    "picking_type_id": 5,
                }
            )
            stock_picking.location_id = rec.source_location_id.id
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
                "context": {"van_id": self.van_id.id, "state": "unload"},
            }

    @api.onchange("van_id")
    def set_product_ids(self):
        for rec in self:
            quant_ids = rec.van_id.location_id.quant_ids

            product_ids = []

            for quant in quant_ids:
                if quant.quantity > 0:
                    product_rec = self.env["van.operation.unload.product"].create(
                        {"product_id": quant.product_id.id, "quantity": quant.quantity}
                    )
                    product_ids.append(product_rec.id)
            rec.product_ids = product_ids


class ProductQuantityLoad(models.TransientModel):
    _name = "van.operation.load.product"

    product_id = fields.Many2one("product.product", readonly=True)
    image = fields.Image(related="product_id.image_128")
    quantity = fields.Integer(readonly=True)
    quantity_transfer = fields.Integer()
    operation_id = fields.Many2one("van.operation.load")

    @api.constrains("quantity_transfer")
    def _check_transfer_quantity(self):
        for rec in self:
            if rec.quantity < rec.quantity_transfer:
                raise ValidationError("Can't transfer more than existing quantity")


class VanOperationLoad(models.TransientModel):
    _name = "van.operation.load"

    product_ids = fields.One2many("van.operation.load.product", "operation_id")
    dest_location_id = fields.Many2one("stock.location", related="van_id.location_id")
    source_location_id = fields.Many2one("stock.location")
    van_id = fields.Many2one("fleetflow.van")

    def action_transfer(self):
        for rec in self:
            stock_picking = self.env["stock.picking"].create(
                {
                    "location_id": rec.source_location_id.id,
                    "location_dest_id": rec.dest_location_id.id,
                    "picking_type_id": 5,
                }
            )
            stock_picking.location_id = rec.source_location_id.id
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
                "name": "Load Products",
                "res_model": "stock.picking",
                "res_id": stock_picking.id,
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "context": {"van_id": rec.van_id.id, "state": "load"},
            }

    @api.onchange("source_location_id")
    def set_product_ids(self):
        for rec in self:
            quant_ids = rec.source_location_id.quant_ids

            product_ids = []

            for quant in quant_ids:
                if quant.quantity > 0:
                    product_rec = self.env["van.operation.load.product"].create(
                        {"product_id": quant.product_id.id, "quantity": quant.quantity}
                    )
                    product_ids.append(product_rec.id)
            rec.product_ids = product_ids
