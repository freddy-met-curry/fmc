# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    nbre_pax = fields.Char()
    nbre_staff = fields.Char()
    notes_comp = fields.Char('Additional notes')
