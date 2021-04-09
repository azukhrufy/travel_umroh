# -*- coding: utf-8 -*-
from odoo import http

# class NtiTravelUmroh(http.Controller):
#     @http.route('/nti_travel_umroh/nti_travel_umroh/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nti_travel_umroh/nti_travel_umroh/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('nti_travel_umroh.listing', {
#             'root': '/nti_travel_umroh/nti_travel_umroh',
#             'objects': http.request.env['nti_travel_umroh.nti_travel_umroh'].search([]),
#         })

#     @http.route('/nti_travel_umroh/nti_travel_umroh/objects/<model("nti_travel_umroh.nti_travel_umroh"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nti_travel_umroh.object', {
#             'object': obj
#         })