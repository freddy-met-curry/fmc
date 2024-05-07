# © 2024 Tobias Zehntner
# © 2024 Niboo SRL (https://www.niboo.com/)
# License Other Proprietary

from odoo import _lt, fields, models


class Website(models.Model):
    _inherit = "website"

    delivery_slot_calendar_id = fields.Many2one(
        "resource.calendar", string="Delivery Slot Calendar"
    )
    delivery_slot_advance_days = fields.Integer(
        string="Propose delivery slots up to this number of days in advance", default=30
    )

    def _get_checkout_steps(self, current_step=None):
        """
        Add delivery to checkout process
        """
        checkout_steps = super()._get_checkout_steps(current_step=None)
        for step in checkout_steps:
            if "website_sale.address" in step[0]:
                # Rename 'Shipping' to 'Address
                step[1]["name"] = "Address"

        previous_step = next(
            step for step in checkout_steps if "website_sale.checkout" in step[0]
        )
        previous_step_index = checkout_steps.index(previous_step)
        next_step_index = previous_step_index + 2
        insert_index = previous_step_index + 1
        checkout_steps[insert_index:insert_index] = [
            (
                ["website_sale_delivery_slot.checkout_delivery_slot"],
                {
                    "name": "Delivery Slot",
                    "current_href": "/shop/delivery_slot",
                    "main_button": _lt("Continue checkout"),
                    "main_button_href": previous_step[1]["main_button_href"],
                    "back_button": _lt("Return to delivery address"),
                    "back_button_href": "/shop/checkout",
                },
            ),
        ]
        checkout_steps[previous_step_index][1][
            "main_button_href"
        ] = "/shop/delivery_slot"
        checkout_steps[next_step_index][1]["back_button"] = _lt(
            "Return to delivery slot"
        )
        checkout_steps[next_step_index][1]["back_button_href"] = "/shop/delivery_slot"

        if current_step:
            return next(step for step in checkout_steps if current_step in step[0])[1]
        return checkout_steps
