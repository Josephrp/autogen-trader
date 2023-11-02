from dotenv import load_dotenv
from alpaca_client import AlpacaClient
import os
load_dotenv()

client = AlpacaClient(os.getenv('ALPACA_API_KEY'), os.getenv('ALPACA_API_SECRET'))

print(client.buying_power)