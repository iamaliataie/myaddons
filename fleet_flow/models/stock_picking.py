from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        stock_picking = super().create(vals)
        stock_picking.location_dest_id.van_id.state = "loaded"

        return stock_picking

    def button_validate(self):
        van_id = self.env.context.get("van_id", None)
        if van_id:
            van = self.env["fleetflow.van"].browse(van_id)
            van.state = "returned"
        return super().button_validate()
