# -*- coding: utf-8 -*-
from odoo import http

# class SanwaManufacturingCostReport(http.Controller):
#     @http.route('/sanwa_manufacturing_cost_report/sanwa_manufacturing_cost_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sanwa_manufacturing_cost_report/sanwa_manufacturing_cost_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sanwa_manufacturing_cost_report.listing', {
#             'root': '/sanwa_manufacturing_cost_report/sanwa_manufacturing_cost_report',
#             'objects': http.request.env['sanwa_manufacturing_cost_report.sanwa_manufacturing_cost_report'].search([]),
#         })

#     @http.route('/sanwa_manufacturing_cost_report/sanwa_manufacturing_cost_report/objects/<model("sanwa_manufacturing_cost_report.sanwa_manufacturing_cost_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sanwa_manufacturing_cost_report.object', {
#             'object': obj
#         })