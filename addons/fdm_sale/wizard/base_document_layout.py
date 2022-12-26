# -*- coding: utf-8 -*-

from odoo import models, fields


class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    logo2 = fields.Binary(related='company_id.logo2')
