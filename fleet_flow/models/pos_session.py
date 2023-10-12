from odoo import fields, api, models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _get_pos_ui_product_product(self, params):
        location = self.config_id.picking_type_id.default_location_src_id
        products = self.env["product.product"].search_read(
            [("id", "in", [quant.product_id.id for quant in location.quant_ids])]
        )
        quantities = {
            quant.product_id.id: quant.quantity for quant in location.quant_ids
        }

        for product in products:
            product["quantity_in_location"] = quantities[product["id"]]
        super()._process_pos_ui_product_product(products)
        return products

    def load_pos_data(self):
        loaded_data = super().load_pos_data()
        return loaded_data

    def get_product_quantity(self, product_id, quantity):
        quants = self.config_id.van_id.quant_ids

        # current_product_quantity = 0

        # for quant in quants:
        #     if quant.product_tmpl_id.id == product_id:
        #         current_product_quantity = quant.quantity

        # if not quantity < current_product_quantity:
        #     return False

        return True
