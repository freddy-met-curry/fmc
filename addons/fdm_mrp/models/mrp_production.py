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
            orderby='date_planned_start ASC')
        if type == 'product':
            for record in daily_production_data:
                products = {}
                components = {}
                domain = record.get('__domain')
                mo_ids = self.search(domain)
                for mo in mo_ids:
                    if mo.product_id.id not in products.keys():
                        products[mo.product_id.id] = mo.product_qty
                    else:
                        products[mo.product_id.id] += mo.product_qty
                    for line in mo.move_raw_ids:
                        if line.product_id.id not in components.keys():
                            components[line.product_id.id] = line.product_uom_qty
                        else:
                            components[line.product_id.id] += line.product_uom_qty

                data.append(
                    {'date_planned': record.get('date_planned_start:day'),
                     'products': products,
                     'mo_ids': mo_ids.ids,
                     'components': components})
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
                    {'date_planned': record.get('date_planned_start:day'),
                     'clients': clients,
                     'mo_ids': mo_ids.ids})
        return data

    def _get_partner_name(self, origin):
        partner_name = ''
        if origin:
            origin_list = origin.split(',')
            for name in origin_list:
                so_id = self.env['sale.order'].search([('name', '=', name)], limit=1)
                if so_id and so_id.partner_id:
                    partner_name += '%s ' % so_id.partner_id.display_name
        return partner_name
