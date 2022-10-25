# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class sale_order(models.Model):
    _inherit = "sale.order"

    min_delay = fields.Datetime(string='Web order date')
