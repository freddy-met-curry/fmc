# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_menu = fields.Boolean('Details of the articles to be produced',
                             help="This field allows you to detail the items of the nomenclature"
                                  " to be produced for the products to "
                                  "be delivered to the customer on the production sheet")
