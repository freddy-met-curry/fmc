# Copyright 2022 Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Freddymetcurry Sale',
    'version': '15.0.1.0.3',
    'author': 'Eezee-It',
    'website': 'http://www.eezee-it.com',
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': [
        'sale',
        'sale_stock',

    ],
    'data': [
        'views/sale_views.xml',
        'report/report_sale_order.xml',
    ],
    'installable': True,
}
