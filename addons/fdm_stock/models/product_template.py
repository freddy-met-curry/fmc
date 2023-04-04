# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import datetime


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_auto_reser_unreserv = fields.Boolean('Automate reserve/unreserve')

    def action_auto_unreser_reserv_stock(self):
        product_template_ids = self.search([('detailed_type', '=', 'product'),
                                            ('is_auto_reser_unreserv', '=', True)])
        move_obj = self.env['stock.move']
        product_replenishment_obj = self.env['report.stock.report_product_product_replenishment']
        warehouse = self.env['stock.warehouse'].browse(product_replenishment_obj.get_warehouses()[0]['id'])
        wh_location_ids = [loc['id'] for loc in self.env['stock.location'].search_read(
            [('id', 'child_of', warehouse.view_location_id.id)],
            ['id'],
        )]
        to_unreserve = []
        to_reserve = []
        for product in product_template_ids:
            lines = product_replenishment_obj._get_report_lines(product.ids, product.product_variant_ids,
                                                                wh_location_ids)
            for line in lines:
                if line.get('document_out') and line.get('document_out')._name == 'mrp.production':
                    if line.get('move_out'):
                        delivery_date = datetime.strptime(line.get('delivery_date'), '%d/%m/%Y').date()
                        if fields.Date.today() < delivery_date and line.get('reservation'):
                            to_unreserve.append(line.get('move_out').id)
                        elif fields.Date.today() >= delivery_date:
                            to_reserve.append(line.get('move_out').id)
                elif line.get('document_out') and line.get('document_out')._name == 'sale.order':
                    if line.get('move_out') and line.get('move_out').picking_id:
                        picking_id = line.get('move_out').picking_id
                        delivery_date = picking_id.scheduled_date.date()
                        if fields.Date.today() < delivery_date and line.get('reservation'):
                            to_unreserve.append(line.get('move_out').id)
                        elif fields.Date.today() >= delivery_date and line.get('move_out').state in ('confirmed', 'partially_available'):
                            to_reserve.append(line.get('move_out').id)
        for move in move_obj.browse(to_unreserve):
            move._do_unreserve()
        for move_id in move_obj.browse(to_reserve):
            move_id._action_assign()
