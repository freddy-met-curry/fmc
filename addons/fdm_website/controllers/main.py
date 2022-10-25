# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.website_sale.controllers import main
from odoo.http import request


class WebsiteSale(main.WebsiteSale):

    @http.route()
    def extra_info(self, **post):
        result = super(WebsiteSale, self).extra_info(**post)
        config_parameter = request.env['ir.config_parameter'].sudo()
        mindate = config_parameter.get_param('fdm_website.min_delay', 'False')
        if mindate:
            result.qcontext['mindate'] = mindate
        return result
