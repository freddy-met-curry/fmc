# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields


class Partner(models.Model):
    _inherit = "res.partner"

    sh_partner_pay_meth_payment_ids = fields.Many2many(comodel_name="payment.provider",
                                                       string="Payment Providers",
                                                       relation="sh_partner_pay_meth_payment_acq_rel")
