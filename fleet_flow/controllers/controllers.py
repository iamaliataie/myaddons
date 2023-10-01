# -*- coding: utf-8 -*-
# from odoo import http


# class FleetFlow(http.Controller):
#     @http.route('/fleet_flow/fleet_flow', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fleet_flow/fleet_flow/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('fleet_flow.listing', {
#             'root': '/fleet_flow/fleet_flow',
#             'objects': http.request.env['fleet_flow.fleet_flow'].search([]),
#         })

#     @http.route('/fleet_flow/fleet_flow/objects/<model("fleet_flow.fleet_flow"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fleet_flow.object', {
#             'object': obj
#         })
