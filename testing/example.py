from dotenv import load_dotenv
from alpaca_tool import AlpacaTool
import os
load_dotenv()

client = AlpacaTool(os.getenv('ALPACA_API_KEY'), os.getenv('ALPACA_API_SECRET'))

print(client.buying_power())
print(client.gain_loss())
# print(client.get_all_assets())
print(client.get_all_positions())

# print(client.create_buy_market_order("SPY", 1))
# print(client.get_open_position("SPY"))
print(client.get_all_positions())
print(client.get_all_open_orders())