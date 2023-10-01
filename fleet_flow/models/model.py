# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VehicleModel(models.Model):
    _inherit = 'fleet.vehicle.model'
    
    image = fields.Image()

