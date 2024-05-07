# © 2024 Tobias Zehntner
# © 2024 Niboo SRL (https://www.niboo.com/)
# License Other Proprietary

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    delivery_slot_calendar_id = fields.Many2one(
        "resource.calendar",
        string="Delivery Slot Calendar",
        compute="_compute_delivery_slot_calendar_id",
        inverse="_inverse_delivery_slot_calendar_id",
        readonly=False,
        required=True,
    )
    delivery_slot_advance_days = fields.Integer(
        string="Propose delivery slots up to this number of days in advance",
        compute="_compute_delivery_slot_advance_days",
        inverse="_inverse_delivery_slot_advance_days",
        readonly=False,
    )

    @api.depends("website_id.delivery_slot_calendar_id")
    def _compute_delivery_slot_calendar_id(self):
        for record in self:
            record.delivery_slot_calendar_id = (
                record.website_id.delivery_slot_calendar_id
            )

    def _inverse_delivery_slot_calendar_id(self):
        for record in self:
            if not record.website_id:
                continue
            record.website_id.delivery_slot_calendar_id = (
                record.delivery_slot_calendar_id
            )

    @api.depends("website_id.delivery_slot_advance_days")
    def _compute_delivery_slot_advance_days(self):
        for record in self:
            record.delivery_slot_advance_days = (
                record.website_id.delivery_slot_advance_days
            )

    def _inverse_delivery_slot_advance_days(self):
        for record in self:
            if not record.website_id:
                continue
            record.website_id.delivery_slot_advance_days = (
                record.delivery_slot_advance_days
            )
