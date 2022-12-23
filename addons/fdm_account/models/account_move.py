# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.tools.misc import get_lang


class AccountMove(models.Model):
    _inherit = "account.move"

    delivery_dates = fields.Char(compute='_compute_delivery_dates')

    def _compute_delivery_dates(self):
        for move in self:
            move.delivery_dates = ''
            pickings = []
            lg = self.env['res.lang']._lang_get(move.partner_id.lang) or get_lang(self.env)
            orders_ids = move.invoice_line_ids.sale_line_ids.mapped('order_id')
            for order in orders_ids:
                pickings.extend(order.picking_ids.ids)
            if pickings:
                move.delivery_dates = ', '.join(
                    str(s.date_done.strftime(lg.date_format)) for s in self.env['stock.picking'].browse(pickings) if
                    s.date_done)
