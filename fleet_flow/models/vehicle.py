# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Vehicle(models.Model):
    _name = 'fleetflow.vehicle'
    _description = 'Fleet Flow Vehicle'
    # _inherit = 'fleet.vehicle'
    
    name = fields.Char()

