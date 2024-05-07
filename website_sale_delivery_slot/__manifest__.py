# © 2024 Tobias Zehntner
# © 2024 Niboo SRL (https://www.niboo.com/)
# License Other Proprietary

{
    "name": "Selectable delivery slots on eShop",
    "category": "eCommerce",
    "summary": "Let user choose delivery date and time slot during checkout",
    "website": "https://www.niboo.com/",
    "version": "17.0.1.0.0",
    "description": """
        1. Website > Configuration > Settings/Shop - Checkout Process > Delivery Schedule:
            Configure Delivery Calendar
        2. Inventory > Settings > Advanced Scheduling > Security Lead Time for Sales
            Configure default lead time for deliveries
        3. On Product > Inventory > Logistics > Customer Lead Time
            Configure lead time on products

        Users can only select slots after the configured lead days (either default or on specific product)
        """,
    "author": "Niboo",
    "license": "Other proprietary",
    "depends": ["website_sale", "sale_stock"],
    "data": [
        "templates/delivery_schedule_template.xml",
        "views/res_config_settings.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_delivery_slot/static/src/css/website_sale_delivery_slot.scss",
        ],
    },
    "installable": True,
    "application": False,
}

# TODO
# - Clean, optimise, comment code
# - Show selected delivery time slot on order summary page
# - Add config how-to in manifest description
# - Add translations
# - Format selected day when choosing slots (with weekday mentioned)
# - In calendar selection, highlight only dates with slots (no weekends, holidays)
# - Show slots immediately when date selected (JS) (one "Delivery" instead of two checkout steps)
# - Rename "Shipping" to "Address"
# - Make delivery-slot optional on product? if valid product selected, step will be shown
# - Add default delivery lead time in hours to config settings (currently hardcoded to next day)
