import os
import json
import tempfile  # <-- Added for temporary file creation
from dotenv import load_dotenv  # <-- Added for dotenv
import autogen  # Assuming that this import works in your environment

# Load environment variables from .env file
load_dotenv()

# Read API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")

# Prepare the configuration list
env_var = [
    {
        'model': 'gpt-4',
        'api_key': api_key
    }
    # Add more configurations if needed
]

# Create a temporary file
with tempfile.NamedTemporaryFile(mode='w+', delete=True) as temp:
    env_var_json = json.dumps(env_var)
    temp.write(env_var_json)
    temp.flush()

    # Create the configuration list
    config_list = autogen.config_list_from_json(
        env_or_file=temp.name,
        filter_dict={
            "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
        }
    )

# Create an AssistantAgent named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "seed": 42,  # Seed for caching and reproducibility
        "config_list": config_list,  # A list of OpenAI API configurations
        "temperature": 0,  # Temperature for sampling
    }
)

# Create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",  # was NEVER before
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # Set to True or image name like "python:3" to use Docker
    },
)

# The assistant receives a message from the user_proxy, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message="""What date is today? Compare the year-to-date gain for META and TESLA.""",
)
