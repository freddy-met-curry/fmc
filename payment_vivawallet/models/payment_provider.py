from werkzeug import urls
from requests.auth import HTTPBasicAuth
from odoo import _, api, fields, models, service
from odoo.exceptions import ValidationError
from odoo.addons.payment_vivawallet.const import SUPPORTED_CURRENCIES, DEFAULT_PAYMENT_METHODS_CODES
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'
 
    code = fields.Selection(
        selection_add=[('vivawallet', "Vivawallet")],
        ondelete={'vivawallet': 'set default'}
    )

    vivawallet_merchant_id = fields.Char(
        string="Merchant ID",
        required_if_provider='vivawallet'
    )

    vivawallet_api_key = fields.Char(
        string="API Key",
        required_if_provider='vivawallet'
    )
    
    vivawallet_client_id = fields.Char(
        string="Client ID",
        required_if_provider='vivawallet'
    )

    vivawallet_client_secret = fields.Char(
        string="Client Secret",
        required_if_provider='vivawallet',
        groups='base.group_system'
    )

    vivawallet_source_code = fields.Char(
        string="Source Code",
        required_if_provider='vivawallet'
    )

    def _get_supported_currencies(self):
        """ Override of `payment` to return the supported currencies. """
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'vivawallet':
            supported_currencies = supported_currencies.filtered(
                lambda c: c.name in SUPPORTED_CURRENCIES
            )
        return supported_currencies
    
    
    def _vivawallet_endpoint(self):
        """ Returns correct Vivawallet endpoint based on acquirer environment
        """

        if self.state != "test":
            return "https://accounts.vivapayments.com/", "https://api.vivapayments.com/", "https://www.vivapayments.com/"
        else:
            return "https://demo-accounts.vivapayments.com/	", "https://demo-api.vivapayments.com/", "https://demo.vivapayments.com/"

    def _vivawallet_get_bearer(self):
        """ Authenticates via OAuth2 to obtain Bearer Token
        """

        self.ensure_one()
        oauth_url, api_url, web_url = self._vivawallet_endpoint()
        url = urls.url_join(oauth_url, "/connect/token")
        basic_auth = HTTPBasicAuth(self.vivawallet_client_id, self.vivawallet_client_secret)
        data = {'grant_type': 'client_credentials',}

        response = requests.post(url, data=data, auth=basic_auth)
        if response.status_code != 200:
            _logger.error("VivaWallet: " + response.text)
            raise ValidationError("Vivawallet: " + _("Could not authenticate the connection to the API."))
        
        accesss_token = json.loads(response.text).get('access_token')
        return accesss_token

    def _vivawallet_make_request(self, endpoint, path, data=None, basic_auth=False, method='POST'):
        """ Make a request at vivawallet endpoint.

        Note: self.ensure_one()

        :param str endpoint: The endpoint to be reached by the request
        :param dict data: The payload of the request
        :param str method: The HTTP method of the request
        :return The JSON-formatted content of the response
        :rtype: dict
        :raise: ValidationError if an HTTP error occurs
        """
        self.ensure_one()

        url = urls.url_join(endpoint, path)
        odoo_version = service.common.exp_version()['server_version']
        module_version = self.env.ref('base.module_payment_vivawallet').installed_version
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f'Odoo/{odoo_version} Vivawalletdoo/{module_version}',
        }

        try:
            if basic_auth:
                basic_auth = HTTPBasicAuth(self.vivawallet_merchant_id, self.vivawallet_api_key)
                response = requests.request(method,url, json=data, headers=headers, timeout=60, auth=basic_auth)
            else:
                headers["Authorization"] = "Bearer %s" % (self._vivawallet_get_bearer())
                response = requests.request(method, url, json=data, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            _logger.exception("Unable to communicate with Vivawallet: %s", url)
            raise ValidationError("Vivawallet: " + _("Could not establish the connection to the API."))

        return response.json()
    
    def _get_default_payment_method_codes(self):
        """ Override of `payment` to return the default payment method codes. """
        default_codes = super()._get_default_payment_method_codes()
        if self.code != 'vivawallet':
            return default_codes
        return DEFAULT_PAYMENT_METHODS_CODES