import logging
import pprint

from werkzeug import urls
from werkzeug.datastructures import MultiDict

from odoo import _, models, fields
from odoo.exceptions import ValidationError
from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment_vivawallet.const import VIVAWALLET_STATE_MAPPING

_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    vivawallet_order_code = fields.Char(string="Vivawallet Order Code")
    vivawallet_transaction_id = fields.Char(string="Vivawallet Transaction ID")

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return Vivawallet-specific rendering values.

        Note: self.ensure_one() from `_get_processing_values`

        :param dict processing_values: The generic and specific processing values of the transaction
        :return: The dict of acquirer-specific rendering values
        :rtype: dict
        """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'vivawallet':
            return res

        oauth_url, api_url, web_url = self.provider_id._vivawallet_endpoint()
        payload = self._vivawallet_prepare_smart_checkout_payload()
        _logger.info("sending '/payments' request for link creation:\n%s", pprint.pformat(payload))
        payment_data = self.provider_id._vivawallet_make_request(
            endpoint=api_url,
            path="/checkout/v2/orders",
            data=payload
        )

        # The acquirer reference is set now to allow fetching the payment status after redirection
        self.vivawallet_order_code = payment_data.get('orderCode')
        
        checkout_url = urls.url_join(web_url, "/web/checkout")
        return {'api_url': checkout_url, 'url_params': MultiDict([('ref', self.vivawallet_order_code)])}

    def _vivawallet_prepare_smart_checkout_payload(self):
        """ Create the payload for the payment request based on the transaction values.

        :return: The request payload
        :rtype: dict
        """

        return {
            'amount': payment_utils.to_minor_currency_units(self.amount, self.currency_id),
            'customerTrns': "C-%i-%i" %(self.id, self.partner_id),
            'customer': {
                'email': self.partner_id.email,
                'fullName': self.partner_id.name,
                'phone': self.partner_id.phone,
                'countryCode': self.partner_id.country_id.code or 'en-US',
                'requestLang': self.partner_id.country_id.code or 'en-US',
            },
            'paymentTimeout': 300,
            'preauth': False,
            'allowRecurring': False,
            'maxInstallments': 1,
            'paymentNotification': True,
            'tipAmount': 1,
            'disableExactAmount': False,
            'disableCash': True,
            'disableWallet': True,
            'sourceCode': self.provider_id.vivawallet_source_code,
            'merchantTrns': "T-%i" % (self.id),
            'tags': [
                self.partner_id.name,
                self.reference
            ],
        }

    def _get_vivawallet_transaction(self, data, match, key):
        return self.search([
            (match, '=', data.get(key)),
            ('provider_code', '=', 'vivawallet'),
            (match, '!=', False)
        ])

    def _get_tx_from_notification_data(self, provider, data):
        """ Override of payment to find the transaction based on Vivawallet data.

        :param str provider: The provider of the acquirer that handled the transaction
        :param dict data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider, data)
        if provider != 'vivawallet':
            return tx

        tx = self._get_vivawallet_transaction(data, "vivawallet_order_code", "t")
        if not tx:
            tx = self._get_vivawallet_transaction(data, "vivawallet_order_code", "s")
        
        if not tx:
            raise ValidationError(
                "Vivawallet: " + _("No transaction found matching transaction reference %s.", data.get('t'))
            )

        return tx

    def _process_notification_data(self, data):
        """ Override of payment to process the transaction based on Vivawallet data.

        Note: self.ensure_one()

        :param dict data: The notification data sent by the provider
        :return: None
        """
        super()._process_notification_data(data)
        if self.provider_code != 'vivawallet':
            return

        if not data.get("t"):
            self._set_pending()
            return

        self.vivawallet_transaction_id = data.get("t")

        oauth_url, api_url, web_url = self.provider_id._vivawallet_endpoint()
        vivawallet_transaction = self.provider_id._vivawallet_make_request(
            endpoint=api_url,
            path="/checkout/v2/transactions/%s" % (self.vivawallet_transaction_id),
            method="GET"
        )

        payment_status = VIVAWALLET_STATE_MAPPING[vivawallet_transaction.get("statusId")]

        if payment_status == 'pending':
            self._set_pending()
        elif payment_status == 'authorized':
            self._set_authorized()
        elif payment_status == 'done':
            self._set_done()
        elif payment_status in ['cancel', 'error']:
            self._set_canceled("Vivawallet: " + _("Canceled payment with status: %s", payment_status))
        else:
            _logger.info("Received data with invalid payment status: %s", payment_status)
            self._set_error(
                "Vivawallet: " + _("Received data with invalid payment status: %s", payment_status)
            )
