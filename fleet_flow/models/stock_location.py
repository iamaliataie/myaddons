from odoo import models, fields, api


class StockLocation(models.Model):
    _inherit = 'stock.location'
    
    van_id = fields.One2many('fleetflow.van', 'location_id', store=True)
    
