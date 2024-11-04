# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api


class PaymentAcquirer(models.Model):
    _inherit = "payment.provider"

    sh_is_public = fields.Boolean(string="Is public?")

    # === BUSINESS METHODS ===#

    @api.model
    def _get_compatible_providers(
        self, company_id, partner_id, amount, currency_id=None, force_tokenization=False,
        is_express_checkout=False, is_validation=False, **kwargs
    ):
        """ Override of payment to return partner specific and public  providers """
        providers = super()._get_compatible_providers(company_id=company_id, 
                                                      partner_id=partner_id, 
                                                      amount=amount, 
                                                      currency_id=currency_id, 
                                                      force_tokenization=force_tokenization,
                                                    is_express_checkout=is_express_checkout, 
                                                    is_validation=is_validation, **kwargs)

        if providers:
    
            public_providers_sudo = providers.filtered(lambda p:  p.sh_is_public)
            partner_specific_provider = self.env['payment.provider']
            partner = self.env['res.partner'].browse(partner_id)
            if partner and partner.sh_partner_pay_meth_payment_ids:
                partner_specific_provider = partner.sh_partner_pay_meth_payment_ids
            finalized_providers_sudo = public_providers_sudo | partner_specific_provider
            return finalized_providers_sudo


        return providers
    