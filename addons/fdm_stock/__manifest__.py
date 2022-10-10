# Copyright 2022 Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Freddymetcurry Stock',
    'version': '15.0.1.0.1',
    'author': 'Eezee-It',
    'website': 'http://www.eezee-it.com',
    'category': 'Inventory',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'web',
        'base',
        'calendar',
    ],
    'data': [

    ],
    'assets': {
        'web.assets_backend': [
            'fred_stock/static/src/calendar_renderer.js',
        ],
    },
    'installable': True,
}
