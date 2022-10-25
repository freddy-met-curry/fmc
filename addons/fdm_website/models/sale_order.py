# -*- coding: utf-8 -*-
from odoo import fields, models


class sale_order(models.Model):
    _inherit = "sale.order"

    min_delay = fields.Datetime(string='Web order date')
