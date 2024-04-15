-- disable vivawallet payment provider
UPDATE payment_provider
   SET vivawallet_merchant_id = NULL,
   vivawallet_api_key = NULL,
   vivawallet_client_id = NULL,
   vivawallet_client_secret = NULL,
   vivawallet_source_code = NULL;
