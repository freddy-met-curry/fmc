{
    'name': 'Vivawallet Payment Acquirer',
    'version': '1.0',
    'category': 'Accounting/Payment Acquirers',
    'sequence': 356,
    'summary': 'Payment Acquirer: Vivawallet Implementation',
    'description': """Vivawallet Payment Acquirer""",
    'images': [
        "static/images/thumbnail.png"
    ],

    'author': 'Alessandro Gessa, Bootando',
    'website': 'https://www.bootando.com',

    'price': 89.99,
    'currency': 'EUR',

    'depends': ['payment'],
    'data': [
        'views/payment_vivawallet_templates.xml',
        'views/payment_views.xml',
        'data/payment_provider_data.xml',
    ],
    'application': True,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3'
}
