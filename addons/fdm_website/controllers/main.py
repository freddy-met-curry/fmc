# -*- coding: utf-8 -*-
from odoo import http
from odoo.addons.website_sale.controllers import main
from odoo.addons.website.controllers.form import WebsiteForm
from odoo.http import request
from datetime import date, timedelta, datetime


class WebsiteSale(main.WebsiteSale):

    def get_date(self, from_date, add_days):
        business_days_to_add = add_days
        current_date = from_date
        while business_days_to_add > 0:
            current_date += timedelta(days=1)
            weekday = current_date.weekday()
            if weekday >= 5:
                continue
            business_days_to_add -= 1
        return current_date

    @http.route()
    def extra_info(self, **post):
        result = super(WebsiteSale, self).extra_info(**post)
        config_parameter = request.env['ir.config_parameter'].sudo()
        mindate = config_parameter.get_param('fdm_website.min_delay') or 0
        if mindate:
            date_min = self.get_date(date.today(), int(mindate))
            result.qcontext['mindate'] = date_min
        return result


class WebsiteSaleForm(WebsiteForm):
    @http.route()
    def website_form_saleorder(self, **kwargs):
        if kwargs.get('datetimepickerExtraInfo'):
            order = request.website.sale_get_order()
            min_date = datetime.strptime(kwargs.get('datetimepickerExtraInfo'), '%m/%d/%Y %H:%M %p').date()
            order.write({'min_delay': min_date})
        return super(WebsiteSaleForm, self).website_form_saleorder(**kwargs)
