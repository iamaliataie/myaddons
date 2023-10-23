from odoo import models, fields, api, Command


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def create(self, vals):
        stock_picking = super().create(vals)
        stock_picking.location_dest_id.van_id.state = "loaded"

        return stock_picking

    def button_validate(self):
        van_id = self.env.context.get("van_id", None)
        state = self.env.context.get("state", None)
        
        if van_id:
            van = self.env["fleetflow.van"].browse(van_id)

            van.state = "returned" if state == "unload" else "loaded"
                
            van_transfer = self.env["van.transfer"].create({
                "dest_location_id": self.location_dest_id.id,
                "source_location_id": self.location_id.id,
                "van_id": van_id,
                "type": "in" if self.location_dest_id.id == van.location_id.id else "out",
                "product_ids": [
                    Command.create(
                            {
                                "product_id": movline.product_id.id,
                                "quantity": movline.quantity_done,
                            }
                        ) for movline in self.move_ids
                    ]
                })
        
        return super().button_validate()
