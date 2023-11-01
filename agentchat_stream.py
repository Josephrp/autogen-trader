import os
import asyncio
import autogen
from dotenv import load_dotenv
import requests
import json

# Constants
API_URL = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&sort=LATEST&limit=5&apikey='

# Load environment variables
load_dotenv()

# Load Alphavantage API key from environment variable
alphavantage_api_key = os.getenv('ALPHAVANTAGE_API_KEY')
if alphavantage_api_key is None:
    alphavantage_api_key = input("Please enter your Alphavantage API key: ")

# Ensure API key is not None
if not alphavantage_api_key:
    raise ValueError("API key is not set.")

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

def get_market_news(ind, ind_upper):
    """Fetch market news and return a summary."""
    data = fetch_data_from_api(API_URL + alphavantage_api_key)
    if data and "feed" in data:
        feeds = data["feed"][ind:ind_upper]
        feeds_summary = "\n".join(
            [
                f"News summary: {f.get('title')}. {f.get('summary')} overall_sentiment_score: {f.get('overall_sentiment_score')}"
                for f in feeds
            ]
        )
        return feeds_summary
    else:
        print("Unexpected API response data.")
        return None

data = asyncio.Future()

async def add_stock_price_data():
    for i in range(0, 5, 1):
        latest_news = get_market_news(i, i + 1)
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
    system_message="You are a financial expert.",
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
    data_task = asyncio.create_task(add_stock_price_data())
    await user_proxy.a_initiate_chat(
        assistant,
        message="""Give me investment suggestion in 3 bullet points.""",
    )
    while not data_task.done() and not data_task.cancelled():
        reply = await user_proxy.a_generate_reply(sender=assistant)
        if reply is not None:
            await user_proxy.a_send(reply, assistant)

if __name__ == "__main__":
    asyncio.run(main())