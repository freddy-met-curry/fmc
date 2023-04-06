# -*- coding: utf-8 -*-

from odoo import models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def _get_tab_daily_production_product(self, daily_production_data):
        data = []
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
        return data

    def _get_tab_daily_production_client(self, daily_production_data):
        data = []
        bom_lines_obj = self.env['mrp.bom.line']
        for record in daily_production_data:
            clients = {}
            bom_line_menu_list = []
            menu_list = []
            domain = record.get('__domain')
            mo_ids = self.search(domain)
            for mo in mo_ids:
                if mo.origin not in clients.keys():
                    clients[mo.origin] = mo.product_qty
                    mo.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id
                    if mo.procurement_group_id and mo.procurement_group_id.mrp_production_ids and \
                            mo.procurement_group_id.mrp_production_ids.move_dest_ids and \
                            mo.procurement_group_id.mrp_production_ids.move_dest_ids.group_id and \
                            mo.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id:
                        sale_id = mo.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id
                        if sale_id:
                            product_bom_menu_ids = sale_id.order_line.filtered(
                                lambda p: p.product_id.is_menu).mapped('product_id')
                            if product_bom_menu_ids:
                                menu_list.extend(product_bom_menu_ids.ids)
                                bom_ids = bom_lines_obj.search(
                                    [('bom_id.type', '=', 'phantom'), '|', '|',
                                     ('bom_id.byproduct_ids.product_id', 'in', product_bom_menu_ids.ids),
                                     ('bom_id.product_id', 'in', product_bom_menu_ids.ids), '&',
                                     ('bom_id.product_id', '=', False),
                                     ('bom_id.product_tmpl_id', 'in',
                                      product_bom_menu_ids.mapped('product_tmpl_id').ids)])
                                if bom_ids:
                                    bom_line_menu_list.extend(bom_ids.ids)
                else:
                    clients[mo.origin] += mo.product_qty
            bom_line_menu = bom_lines_obj.read_group([('id', 'in', bom_line_menu_list)],
                                                     ['product_id', 'product_qty'],
                                                     groupby=['product_id'])
            mo_products = self.read_group([('id', 'in', mo_ids.ids)],
                                          ['product_id', 'product_qty'],
                                          groupby=['product_id'])
            data.append(
                {'date_planned': record.get('date_planned_start:day'),
                 'clients': clients,
                 'menu_list': menu_list,
                 'bom_line_menu': bom_line_menu,
                 'mo_products': mo_products,
                 'mo_ids': mo_ids.ids})
        return data

    def _get_tab_daily_production(self, type):
        data = []
        daily_production_data = self.read_group(
            [('id', 'in', self.ids)], ['date_planned_start'],
            groupby=['date_planned_start:day', 'date_planned_start:month',
                     'date_planned_start:year', 'product_id'],
            orderby='date_planned_start ASC')
        if type == 'product':
            data = self._get_tab_daily_production_product(daily_production_data)
        elif type == 'client':
            data = self._get_tab_daily_production_client(daily_production_data)
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
