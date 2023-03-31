# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_auto_unreser_reserv_stock(self, product_ids=False):
        products = self.search([('detailed_type', '=', 'product')])
        mo_obj = self.env['mrp.production']
        if product_ids:
            products = self.search([('id', 'in', product_ids)])
        product_replenishment_obj = self.env['report.stock.report_product_product_replenishment']
        warehouse = self.env['stock.warehouse'].browse(product_replenishment_obj.get_warehouses()[0]['id'])
        wh_location_ids = [loc['id'] for loc in self.env['stock.location'].search_read(
            [('id', 'child_of', warehouse.view_location_id.id)],
            ['id'],
        )]
        to_unreserve = []
        to_reserve = []
        for product in products:
            lines = product_replenishment_obj._get_report_lines(product.ids, product.product_variant_ids, wh_location_ids)
            for line in lines:
                if line.get('document_out') and line.get('document_out')._name == 'mrp.production':
                    delivery_date = datetime.strptime(line.get('delivery_date'), '%d/%m/%Y').date()
                    if fields.Date.today() < delivery_date and line.get('reservation'):
                        to_unreserve.append(line.get('document_out').id)
                    elif fields.Date.today() >= delivery_date and not line.get('replenishment_filled'):
                        to_reserve.append(line.get('document_out').id)
        for mo in mo_obj.browse(to_unreserve):
            mo.do_unreserve()
        for mo_id in mo_obj.browse(to_reserve):
            mo_id.action_assign()


