import autogen
import asyncio
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
    "temperature": 0.4,
}

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)  

analyst = autogen.AssistantAgent(
    name="Financial_Analyst",
    system_message="You are a financial trading expert and your job is to analyze financial news and provide advice to the Portfolio Manager with respect to buy, sell, or wait decision on stocks. Don't advize to buy stocks until you explained the news. It you're sending a JSON payload that includes a calculation, perform the calculation in advance and only send the result.Microsoft's Cloud Division Soars 51%, Tesla Faces New Regulatory Hurdles Over Autopilot. Apple Unveils Revolutionary Battery Technology.",
    llm_config=llm_config,
)

news_agent = autogen.AssistantAgent(
    name="News_Agent",
    system_message="Your job is to provide the latest market news and here is the latest market news: Microsoft's Cloud Division Soars 51%, Tesla Faces New Regulatory Hurdles Over Autopilot. Apple Unveils Revolutionary Battery Technology.",
    llm_config=llm_config,
)

pm = autogen.AssistantAgent(
    name="Portfolio_Manager",
    system_message="Your job is the manage the stock portoflio through Alpaca API functions based on latest financial news from News Agent. Always undersatnd buying power and current positions before buying or selling stocks based on latest news. If you're sending a JSON payload that includes a calculation, perform the calculation in advance and only send the result.",
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

async def main():

    # Setup the group chat and manager
    groupchat = autogen.GroupChat(agents=[user_proxy, news_agent, analyst, pm], messages=[], max_round=46)
    manager = autogen.GroupChatManager(groupchat=groupchat)

    # Initiate the chat
    await user_proxy.a_initiate_chat(manager, message="Get today's date. Get the last price for MSFT, AAPL, and TSLA using yfinance python code.")

# Run the main function
asyncio.run(main())