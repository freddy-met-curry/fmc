# -*- coding: utf-8 -*-

from odoo import models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def _get_tab_daily_production(self, type):
        data = []
        daily_production_data = self.read_group(
            [('id', 'in', self.ids)], ['date_planned_start'],
            groupby=['date_planned_start:day', 'date_planned_start:month',
                     'date_planned_start:year', 'product_id'],
            orderby='date_planned_start DESC')
        if type == 'product':
            for record in daily_production_data:
                products = {}
                domain = record.get('__domain')
                mo_ids = self.search(domain)
                for mo in mo_ids:
                    if mo.product_id.id not in products.keys():
                        products[mo.product_id.id] = mo.product_qty
                    else:
                        products[mo.product_id.id] += mo.product_qty
                data.append(
                    {'date_planned': record.get('date_planned_start:day'), 'products': products, 'mo': mo_ids.ids})
        if type == 'client':
            for record in daily_production_data:
                clients = {}
                domain = record.get('__domain')
                mo_ids = self.search(domain)
                for mo in mo_ids:
                    if mo.origin not in clients.keys():
                        clients[mo.origin] = mo.product_qty
                    else:
                        clients[mo.origin] += mo.product_qty
                data.append(
                    {'date_planned': record.get('date_planned_start:day'), 'clients': clients, 'mo': mo_ids.ids})
        return data
