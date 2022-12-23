# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    logo2 = fields.Binary()
    note_report = fields.Text()
