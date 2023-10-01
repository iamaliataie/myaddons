# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    
    state = fields.Selection([
        ('idle', 'Idle'),
        ('loaded', 'Loaded'),
        ('in-delivery', 'In Delivery'),
        ('unload', 'Unload'),
        ('returned', 'Returned'),
    ])

    image = fields.Image(related='model_id.image', readonly=True)

