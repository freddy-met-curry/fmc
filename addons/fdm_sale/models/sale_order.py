# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    nbre_pax = fields.Char()
    nbre_staff = fields.Char()
    notes_comp = fields.Char('Additional notes')

    def write(self, values):
        res = super(SaleOrder, self).write(values)
        for record in self:
            if values.get('nbre_pax'):
                record.picking_ids.write({'nbre_pax': record.nbre_pax})
            if values.get('nbre_staff'):
                record.picking_ids.write({'nbre_staff': record.nbre_staff})
            if values.get('notes_comp'):
                record.picking_ids.write({'notes_comp': record.notes_comp})

        return res

    def _action_confirm(self):
        res = super(SaleOrder, self)._action_confirm()
        self.picking_ids.write({'nbre_pax': self.nbre_pax,
                                'nbre_staff': self.nbre_staff,
                                'notes_comp': self.notes_comp,
                                })
        return res
