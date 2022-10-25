
# Copyright 2022 Eezee-IT (<http://www.eezee-it.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Freddymetcurry Website',
    'version': '15.0.1.0.0',
    'author': 'Eezee-It',
    'website': 'http://www.eezee-it.com',
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'website',
        'website_sale',

    ],
    'assets': {
        'web.assets_frontend': [
            'fdm_website/static/src/extra_infos.js',
            ]
    },
    'data': [
        'views/res_config_settings_views.xml',
        'views/sale_order_view.xml',
        'views/template_extra_infos.xml',
    ],
    'installable': True,
}