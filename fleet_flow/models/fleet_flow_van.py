from odoo import models, api, fields, Command
from odoo.exceptions import UserError

class FleetFlowVan(models.Model):
    _name = "fleetflow.van"
    _description = "A fleet flow"
    _rec_name = "model"

    model = fields.Char()
    license_plate = fields.Char()
    driver_id = fields.Many2one("res.partner")
    color = fields.Char()
    image = fields.Image()
    location_id = fields.Many2one("stock.location")
    source_location_id = fields.Many2one("stock.location")
    quant_ids = fields.One2many(related="location_id.quant_ids")
    chassis_number = fields.Char()
    fuel_type = fields.Selection(
        [
            ("diesel", "Diesel"),
            ("gasoline", "Gasoline"),
            ("electric", "Electric"),
            ("lpg", "LPG"),
            ("hybrid", "Hybrid"),
        ]
    )
    operation_type_id = fields.Many2one("stock.picking.type")
    return_operation_type_id = fields.Many2one("stock.picking.type")
    model_year = fields.Char()
    transmission = fields.Selection(
        [
            ("manual", "Manual"),
            ("automatic", "Automatic"),
            ("hybrid", "Hybrid"),
        ]
    )
    # seats_number = fields.Selection([(2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])
    state = fields.Selection(
        [
            ("idle", "Idle"),
            ("loaded", "Loaded"),
            ("on_delivery", "On_delivery"),
            ("returned", "Returned"),
        ]
    )

    @api.model
    def create(self, vals):
        stock_location = self.env["stock.location"].create(
            {"name": vals["model"], "usage": "internal"}
        )
        van = super().create(vals)
        van.location_id = stock_location.id
        van.state = "idle"
        ops_type = self.env["stock.picking.type"].create(
            {
                "name": f"Load {van.model}",
                "code": "internal",
                "sequence_code": f"{van.license_plate}",
            }
        )

        ops_type.default_location_src_id = van.source_location_id
        ops_type.default_location_dest_id = van.location_id
        van.operation_type_id = ops_type.id

        return_ops_type = self.env["stock.picking.type"].create(
            {
                "name": f"Unload {van.model}",
                "code": "internal",
                "sequence_code": f"R{van.license_plate}",
            }
        )
        return_ops_type.default_location_src_id = van.location_id
        return_ops_type.default_location_dest_id = van.source_location_id
        van.return_operation_type_id = return_ops_type.id

        return van

    def open_stock(self):
        for rec in self:
            return {
                "name": rec.location_id.name,
                "type": "ir.actions.act_window",
                "res_model": "stock.quant",
                # "view_id": "stock.view_stock_quant_tree",
                "view_mode": "tree,form",
                "domain": [("location_id", "=", rec.location_id.id)],
            }

    def open_transfer(self):
        for rec in self:
            return {
                "name": "new",
                "type": "ir.actions.act_window",
                "res_model": "stock.picking",
                # "view_id": "stock.view_stock_quant_tree",
                "view_mode": "form",
                "context": {
                    "default_picking_type_id": rec.operation_type_id.id,
                },
            }

    def action_empty(self):
        for rec in self:
            for quant in rec.quant_ids:
                if quant.quantity > 0:
                    raise UserError("You have to return all products to source location")
            for quant in rec.quant_ids:
                quant.unlink()

            rec.state = "idle"

    def action_unload(self):
        for rec in self:
            quant_ids = rec.location_id.quant_ids
            # stock_picking = self.env["stock.picking"].create(
            #     {
            #         "location_id": rec.location_id.id,
            #         "location_dest_id": rec.source_location_id.id,
            #         "picking_type_id": rec.return_operation_type_id.id,
            #         "move_type": "direct",
            #     }
            # )

            # for quant in quant_ids:
            #     self.env["stock.move"].create(
            #         {
            #             "name": quant.product_id.name,
            #             "product_id": quant.product_id.id,
            #             # "product_uom_qty": quant.quantity,
            #             # "quantity_done": quant.quantity,
            #             "product_uom": quant.product_id.uom_id.id,
            #             "picking_id": stock_picking.id,
            #             "location_id": quant.location_id.id,
            #             "location_dest_id": rec.source_location_id.id,
            #         }
            #     )

            # stock_picking.action_confirm()
            # stock_picking.action_assign()

            # return {
            #     "name": "Return Products",
            #     "res_model": "stock.picking",
            #     "res_id": stock_picking.id,
            #     "type": "ir.actions.act_window",
            #     "view_mode": "form",
            # }
            # stock_picking.action_confirm()
            # stock_picking.button_validate()
            # rec.state = "returned"

            product_ids = []

            for quant in quant_ids:
                if quant.quantity > 0:
                    product_rec = self.env["product.quantity.transient"].create(
                        {"product_id": quant.product_id.id, "quantity": quant.quantity}
                    )
                    product_ids.append(product_rec.id)
            return {
                "name": "Select Transfer Quantities",
                "res_model": "transfer",
                "type": "ir.actions.act_window",
                "target": "new",
                "view_mode": "form",
                "context": {
                    # "tree_view_ref":
                    "default_product_ids": product_ids,
                    "default_dest_location_id": rec.source_location_id.id,
                    "default_source_location_id": rec.location_id.id,
                    "picking_type_id": rec.return_operation_type_id.id,
                    "van_id": rec.id,
                },
            }


class ResCompany(models.Model):
    _inherit = "res.company"

    location_id = fields.Many2one("stock.location")


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    location_id = fields.Many2one(
        related="company_id.location_id", string="Location", readonly=False
    )
