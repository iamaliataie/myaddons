from odoo import fields, api, models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _get_pos_ui_product_product(self, params):
        location = self.config_id.van_id.location_id
        products = self.env["product.product"].search_read(
            [("id", "in", [quant.product_id.id for quant in location.quant_ids])]
        )

        super()._process_pos_ui_product_product(products)
        return products

    def load_pos_data(self):
        for quant in self.config_id.van_id.location_id.quant_ids:
            print(quant.product_id.name, quant.quantity)
        loaded_data = super().load_pos_data()
        return loaded_data
