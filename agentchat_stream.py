import os
import asyncio
import autogen
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

# Get API token from environment variables
API_TOKEN = os.getenv('MARKETAUX_API_TOKEN')

# Constants
NEWS_API_URL = f'https://api.marketaux.com/v1/news/all?symbols=MSFT&filter_entities=true&language=en&api_token={API_TOKEN}'

config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")

def fetch_data_from_api(url):
    """Fetch data from API and return as JSON."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if invalid response
        return response.json()
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Failed to fetch data from API: {e}")
        return None

def get_market_news():
    """Fetch market news and return a summary."""
    data = fetch_data_from_api(NEWS_API_URL)
    if data and "data" in data:
        feeds = data["data"]
        feeds_summary = "\n".join(
            [
                f"News summary: {f.get('title')}. {f.get('description')}"
                for f in feeds
            ]
        )
        return feeds_summary
    else:
        print("Unexpected API response data.")
        return None

data = asyncio.Future()

async def add_market_data():
    for i in range(0, 2, 1):
        latest_news = get_market_news()
        if latest_news:
            if data.done():
                data.result().append(latest_news)
            else:
                data.set_result([latest_news])
        await asyncio.sleep(5)

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "request_timeout": 600,
        "seed": 41,
        "config_list": config_list,
        "temperature": 0,
    },
    system_message="You are a day trading bot, trading MSFT",
)

user_proxy = autogen.UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    code_execution_config=False,
    default_auto_reply=None,
)

async def add_data_reply(recipient, messages, sender, config):
    await asyncio.sleep(0.1)
    data = config["news_stream"]
    if data.done():
        result = data.result()
        if result:
            news_str = "\n".join(result)
            result.clear()
            return (
                True,
                f"Just got some latest market news. Merge your new suggestion with previous ones.\n{news_str}",
            )
    return False, None

user_proxy.register_reply(autogen.AssistantAgent, add_data_reply, 1, config={"news_stream": data})

async def main():
    data_task = asyncio.create_task(add_market_data())
    try:
        await user_proxy.a_initiate_chat(
            assistant,
            message="""Give me investment suggestion for how to trade MSFT: BUY, SELL, or HOLD. Explain your logic""",
        )
        while not data_task.done() and not data_task.cancelled():
            reply = await user_proxy.a_generate_reply(sender=assistant)
            if reply is not None:
                print(f"{assistant.name} (to {user_proxy.name}):")
                print()
                print(reply)
                print()
                print("-" * 80)
            else:
                break
    except asyncio.CancelledError:
        pass  # Ignore the CancelledError
    finally:
        data_task.cancel()
        await data_task

if __name__ == "__main__":
    asyncio.run(main())