from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass

# print('${} is available as buying power.'.format(account.buying_power))

class AlpacaClient:
    def __init__(self, api_key, secret_key):
        self.trading_client = TradingClient(api_key, secret_key)

    def buying_power(self):
        account = self.trading_client.get_account()

        if account.trading_blocked:
            raise Exception('Account is currently restricted from trading.')
        
        return account.buying_power
    
    def gain_loss(self):
        account = self.trading_client.get_account()

        if account.trading_blocked:
            raise Exception('Account is currently restricted from trading.')
        
        return float(account.equity) - float(account.last_equity)
    
    def get_all_assets(self):
        search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)

        return self.trading_client.get_all_assets(search_params)