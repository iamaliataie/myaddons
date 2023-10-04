from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    @api.model
    def create(self, vals):
        stock_picking = super().create(vals)
        print('=================================')
        stock_picking.location_dest_id.van_id.state = 'loaded'
        
        return stock_picking