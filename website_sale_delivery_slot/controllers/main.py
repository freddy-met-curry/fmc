# © 2024 Tobias Zehntner
# © 2024 Niboo SRL (https://www.niboo.com/)
# License Other Proprietary

import datetime

import pytz
from dateutil.relativedelta import relativedelta

from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleDeliverySlot(WebsiteSale):
    """
    Add /shop/delivery routes
    """

    @http.route()
    def checkout(self, **kw):
        # Prevent express checkout
        if kw.get("express"):  # TODO check if delivery slot set
            kw.pop("express")
        return super().checkout(**kw)

    @http.route()
    def address(self, **kw):
        kw["callback"] = "/shop/delivery_slot"
        return super().address(**kw)

    @http.route(
        ["/shop/delivery_slot"], type="http", auth="public", website=True, sitemap=False
    )
    def delivery_slot(self, **post):
        order_sudo = request.website.sale_get_order()
        if not order_sudo:
            return
        redirection = self.checkout_redirection(order_sudo)
        if redirection:
            return redirection

        values = self.checkout_values(order_sudo, **post)

        website = request.env["website"].browse(request.env.context.get("website_id"))
        errors = []

        if order_sudo.commitment_date:
            values["delivery_datetime"] = order_sudo.commitment_date
        if website.delivery_slot_calendar_id:
            slot_calendar, valid_datetimes = self.get_slots_by_day(order_sudo, website)

            if slot_calendar:
                values["slot_calendar"] = slot_calendar
            else:
                errors.append(
                    (
                        "Unavailable",
                        "There are currently no delivery slots available",
                    )
                )
        else:
            errors.append(
                ("Missing Configuration", "No delivery calendar has been specified")
            )

        if request.httprequest.method == "GET":
            if errors:
                values["errors"] = errors
                return request.render(
                    "website_sale_delivery_slot.checkout_delivery_slot",
                    values,
                )

            # Avoid useless rendering if called in ajax
            if post.get("xhr"):
                return "ok"
            return request.render(
                "website_sale_delivery_slot.checkout_delivery_slot", values
            )
        if request.httprequest.method == "POST":
            delivery_datetime_str = post.get("slot")
            delivery_datetime = False
            if not delivery_datetime_str:
                errors.append(("Missing Date", "Please select a slot for delivery"))
            else:
                delivery_datetime = datetime.datetime.fromisoformat(post["slot"])
                if delivery_datetime not in valid_datetimes:
                    errors.append(
                        ("Unavailable Slot", "Please select a valid slot for delivery")
                    )
            if errors:
                values["errors"] = errors
                return request.render(
                    "website_sale_delivery_slot.checkout_delivery_slot",
                    values,
                )
            order_sudo.commitment_date = delivery_datetime.astimezone(
                pytz.timezone("utc")
            ).replace(tzinfo=None)
            return request.redirect("/shop/confirm_order")

        return request.redirect("/shop/cart")

    def get_slots_by_day(self, order, website):
        now = datetime.datetime.now(pytz.timezone(request.env.context.get("tz", "utc")))
        calendar_id = website.delivery_slot_calendar_id
        security_lead = order.company_id.security_lead
        delivery_slot_advance_days = website.delivery_slot_advance_days

        # Lead time: min 1 day or max of default security lead time and product lead times
        lead_time_days = max(
            1, max(security_lead, max(order.order_line.mapped("product_id.sale_delay")))
        )
        min_date = (now + relativedelta(days=lead_time_days)).replace(hour=0, minute=0)
        max_date = (now + relativedelta(days=delivery_slot_advance_days)).replace(
            hour=23, minute=59
        )

        work_intervals = calendar_id.sudo()._work_intervals_batch(min_date, max_date)[
            False
        ]
        slot_calendar = {}
        valid_datetimes = []
        for work_interval in work_intervals:
            date_start, date_stop, _attendance = work_interval
            year = date_start.year
            week = date_start.isocalendar()[1]
            day = date_start.weekday()
            if not slot_calendar.get(year):
                slot_calendar[year] = {}
            if not slot_calendar.get(year).get(week):
                slot_calendar[year][week] = {}
            if not slot_calendar.get(year).get(week).get(day):
                slot_calendar[year][week][day] = []

            slot_calendar[year][week][day].append(
                (
                    date_stop,
                    f"{date_start.strftime('%H:%M')} - {date_stop.strftime('%H:%M')}",
                )
            )
            valid_datetimes.append(date_stop)

        return slot_calendar, valid_datetimes
