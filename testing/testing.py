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

assistant = autogen.AssistantAgent(
    name="assistant ONE",
    llm_config={
        "request_timeout": 600,
        "seed": 42,
        "config_list": config_list,
        "temperature": 0,
    },
)

user_proxy = autogen.UserProxyAgent(
    name="Alex",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)  

assistant_two = autogen.AssistantAgent(
    name="Assistant TWO",
    llm_config={
        "request_timeout": 600,
        "seed": 42,
        "config_list": config_list, 
        "temperature": 0,
    },
)

user_proxy.initiate_chat(
    assistant,
    message="""What date is today?""",
)

user_proxy.initiate_chat(
    assistant_two,
    message="""Compare the year-to-date gain for MSFT and TESLA.""",
)