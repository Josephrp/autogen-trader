import autogen

config_list = autogen.config_list_from_dotenv(
    dotenv_file_path='.env',
    filter_dict={
        "model": {
            "gpt-4",
            "gpt-3.5-turbo",
        }
    }
)


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
    llm_config={
        "request_timeout": 600,
        "seed": 42,
        "config_list": config_list,
        "temperature": 0,
    },
)
pm = autogen.AssistantAgent(
    name="Trader",
    system_message="based on latest earnings data for MSFT and TESLA, decide which stock is a buy, sell, or wait.",
        llm_config={
        "request_timeout": 600,
        "seed": 42,
        "config_list": config_list,
        "temperature": 0,
    },
)


groupchat = autogen.GroupChat(agents=[user_proxy, researcher, pm], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat)

user_proxy.initiate_chat(manager, message="Get today's date. Compare the year-to-date gain for MSFT and TESLA.")
# type exit to terminate the chat