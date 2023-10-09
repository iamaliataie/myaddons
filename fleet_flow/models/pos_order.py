from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def create_from_ui(self, orders, draft=False):
        """Create and update Orders from the frontend PoS application.

        Create new orders and update orders that are in draft status. If an order already exists with a status
        diferent from 'draft'it will be discareded, otherwise it will be saved to the database. If saved with
        'draft' status the order can be overwritten later by this function.

        :param orders: dictionary with the orders to be created.
        :type orders: dict.
        :param draft: Indicate if the orders are ment to be finalised or temporarily saved.
        :type draft: bool.
        :Returns: list -- list of db-ids for the created and updated orders.
        """
        order_ids = []
        for order in orders:
            existing_order = False
            if "server_id" in order["data"]:
                existing_order = self.env["pos.order"].search(
                    [
                        "|",
                        ("id", "=", order["data"]["server_id"]),
                        ("pos_reference", "=", order["data"]["name"]),
                    ],
                    limit=1,
                )
            if (
                existing_order and existing_order.state == "draft"
            ) or not existing_order:
                order_ids.append(self._process_order(order, draft, existing_order))

        print("======================>>>", order_ids)

        return self.env["pos.order"].search_read(
            domain=[("id", "in", order_ids)],
            fields=["id", "pos_reference", "account_move"],
            load=False,
        )

        # super().create_from_ui(orders,draft)
