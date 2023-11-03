import autogen
import asyncio


config_list = autogen.config_list_from_dotenv(
    dotenv_file_path='.env',
    filter_dict={
        "model": {
            "gpt-4",
            "gpt-3.5-turbo",
        }
    }
)

def get_market_news(ind, ind_upper):
    import requests
    import json

    data = {
        "feed": [
            {
                "title": "Microsoft's Cloud Division Soars 51%",
                "summary": "Microsoft's (NASDAQ: MSFT) Azure cloud services continue to gain market share, with a significant surge in demand from enterprise customers leading to robust revenue growth.",
            },
            {
                "title": "Tesla Faces New Regulatory Hurdles Over Autopilot",
                "summary": "Tesla (NASDAQ: TSLA) encounters new regulatory challenges as federal investigations into its Autopilot system intensify, causing concerns among investors.",
            },
             {
                "title": "Apple Unveils Revolutionary Battery Technology",
                "summary": "Apple Inc. (NASDAQ: AAPL) reveals a groundbreaking battery technology that promises to extend the life of its devices, sending its stock price to new highs.",
            },
            {
                "title": "IBM's Quarterly Earnings Miss Estimates Amid Slowing Software Sales",
                "summary": "International Business Machines (NYSE: IBM) reports lower-than-expected earnings for the quarter as its software segment shows a surprising downturn in sales.",
            },
            {
                "title": "Salesforce Announces Record-Breaking Deal with Major Retailer - CRM's Outlook Brightens",
                "summary": "Salesforce (NYSE: CRM) secures a landmark contract with a leading global retailer, signifying the strength and adaptability of its CRM solutions in the competitive market.",
             }
        ]
    }
    feeds = data["feed"][ind:ind_upper]
    feeds_summary = "\n".join(
        [
            f"News summary: {f['title']}. {f['summary']}"
            for f in feeds
        ]
    )
    return feeds_summary

data = asyncio.Future()

async def add_stock_price_data():
    # simulating the data stream
    for i in range(0, 5, 1):
        latest_news = get_market_news(i, i + 1)
        if data.done():
            data.result().append(latest_news)
        else:
            data.set_result([latest_news])
        # print(data.result())
        await asyncio.sleep(5)

# create an AssistantAgent instance named "assistant"
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
# create a UserProxyAgent instance named "user"
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
        message="""Decide whether to buy, sell, or wait on the stock based on the latest market news. Only give a one word answer: BUY, SELL, or WAIT. In addition, give a one sentence reason limited to 15 words, no more.""",
    )
    while not data_task.done() and not data_task.cancelled():
        reply = await user_proxy.a_generate_reply(sender=assistant)
        if reply is not None:
            await user_proxy.a_send(reply, assistant)

# Run the main function
asyncio.run(main())