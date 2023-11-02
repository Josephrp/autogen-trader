import autogen
from dotenv import load_dotenv
from alpaca_client import AlpacaClient
import os
load_dotenv()

client = AlpacaClient(os.getenv('ALPACA_API_KEY'), os.getenv('ALPACA_API_SECRET'))

config_list = autogen.config_list_from_dotenv(
    dotenv_file_path='.env',
    filter_dict={
        "model": {
            "gpt-4",
            "gpt-3.5-turbo",
        }
    }
)

llm_config = {
    "functions": [
        {
            "name": "buying_power",
            "description": "Run this function to determine the available powering power of the portfolio",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            }
        },
        {
            "name": "current_positions",
            "description": "Run this function to get the positions in the portfolio",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            }
        },
        {
            "name": "create_buy_order",
            "description": "Run this function to execute a buy order at market price",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "ticker symbol of the security to order. must be in all caps",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Quantity amount to the security to purchase",
                    },
                },
                "required": ["ticker", "quantity"],
            },
        },
        {
            "name": "create_sell_order",
            "description": "Run this function to execute a sell order at market price",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "ticker symbol of the security. Must be in all caps",
                    },
                    "quantity": {
                        "type": "integer",
                        "description": "Quantity amount to the security to sell",
                    },
                },
                "required": ["ticker", "quantity"],
            },
        },
        {
            "name": "get_open_orders",
            "description": "Run this function to retrieve all pending open orders",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            }
        },
        {
            "name": "gain_loss_status",
            "description": "Run this function the current gain or loss of the portfolio",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            }
        },
    ],
    "config_list": config_list,
    "request_timeout": 6000,
    "seed": 42,
    "temperature": 0,
}

user_proxy = autogen.UserProxyAgent(
    name="User_proxy", 
    system_message="A human admin.",
    human_input_mode="TERMINATE", 
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 2, 
        "work_dir": "coding", 
        "use_docker": False,
    }
)


researcher = autogen.AssistantAgent(
    name="researcher",
    llm_config=llm_config,
)

pm = autogen.AssistantAgent(
    name="Trader",
    system_message="based on latest year to date gain for TESLA only, decide which stock is a buy, sell, or wait. Give a BUY, SELL, OR WAIT recommendation even if there is not enough data, just give a random recommendation.",
    llm_config=llm_config,
)

pm.register_function(
    function_map={
        "buying_power": client.buying_power,
        "current_positions": client.get_all_positions,
        "create_buy_order": client.create_buy_market_order,
        "create_sell_order": client.get_open_position,
        "get_open_orders": client.get_all_open_orders,
        "gain_loss_status": client.gain_loss
    }
)

groupchat = autogen.GroupChat(agents=[user_proxy, researcher, pm], messages=[], max_round=24)
manager = autogen.GroupChatManager(groupchat=groupchat)

user_proxy.initiate_chat(manager, message="Get today's date. Get TESLA year to date gain in the market using yfinance")
