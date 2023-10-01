# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    
    comapny = fields.Char()

