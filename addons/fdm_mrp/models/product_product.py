# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_menu = fields.Boolean('Menu')
