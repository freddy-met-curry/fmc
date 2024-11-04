# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
{
    "name": "Payment Method Restriction",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "version": "0.0.1",
    "category": "Accounting",
    "summary": "Restrict Payment Acquirers Fix Payment Methods Website Payment Acquirer App Safe Payment Options Module Control Payment Method Choose Payment Method Odoo Restrict Specific User Payment Method Specific Payment Acquirers Ecommerce Payment Acquirer E-commerce Payment Acquirer e-Commerce Payment Acquirer Public Payment Acquirer",
    "description": """ Do you want to restrict the payment acquirers method? This module restricts payment acquirers methods for specific users. You can configure payment acquirers from particular payment acquirers or from particular users, for configure that you have to tick the tickbox "Is Public" in a particular payment method. So when the user will pay the payment selected payment acquirers will visible. """,
    "depends": [
        "website_sale",
        "payment",
    ],
    "data": [
        "views/payment_views.xml",
        "views/partner_views.xml",
    ],
    "images": ["static/description/background.png", ],
    "license": "OPL-1",
    "installable": True,
    "auto_install": False,
    "application": True,
    "price": 20,
    "currency": "EUR"
}
