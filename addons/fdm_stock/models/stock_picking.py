# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    customer_id = fields.Many2one('res.partner', compute="_compute_customer", store=True)

    @api.depends('partner_id')
    def _compute_customer(self):
        for record in self:
            record.customer_id = record.partner_id.parent_id or record.partner_id
