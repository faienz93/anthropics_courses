from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=my_api_key)
MODEL_NAME = "claude-3-haiku-20240307"  # "claude-3-sonnet-20240229"

print("=================================================================")
print("======================== TOOL AUTO ==============================")
print("=================================================================")
# When working with the `tool_choice` parameter, we have three possible options: 

# * `auto` allows Claude to decide whether to call any provided tools or not.
# * `any` tells Claude that it must use one of the provided tools, but doesn't force a particular tool.
# * `tool` allows us to force Claude to always use a particular tool.

def web_search(topic):
    print(f"pretending to search the web for {topic}")

web_search_tool = {
    "name": "web_search",
    "description": "A tool to retrieve up to date information on a given topic by searching the web",
    "input_schema": {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "The topic to search the web for"
            },
        },
        "required": ["topic"]
    }
}

from datetime import date

def chat_with_web_search(user_query):
    messages = [{"role": "user", "content": user_query}]

    system_prompt=f"""
    Answer as many questions as you can using your existing knowledge.  
    Only search the web for queries that you can not confidently answer.
    Today's date is {date.today().strftime("%B %d %Y")}
    If you think a user's question involves something in the future that hasn't happened yet, use the search tool.
    """

    response = client.messages.create(
        system=system_prompt,
        model=MODEL_NAME,
        messages=messages,
        max_tokens=1000,
        tool_choice={"type": "auto"}, # <-- We also set `tool_choice` to `auto`:
        tools=[web_search_tool]
    )
    last_content_block = response.content[-1]
    if last_content_block.type == "text":
        print("Claude did NOT call a tool")
        print(f"Assistant: {last_content_block.text}")
    elif last_content_block.type == "tool_use":
        print("Claude wants to use a tool")
        print(last_content_block)


chat_with_web_search("What color is the sky?")
chat_with_web_search("Who won the 2024 Miami Grand Prix?")



print("=================================================================")
print("======================== TYPE TOOL ==============================")
print("=================================================================")

tools = [
    {
        "name": "print_sentiment_scores",
        "description": "Prints the sentiment scores of a given tweet or piece of text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "positive_score": {"type": "number", "description": "The positive sentiment score, ranging from 0.0 to 1.0."},
                "negative_score": {"type": "number", "description": "The negative sentiment score, ranging from 0.0 to 1.0."},
                "neutral_score": {"type": "number", "description": "The neutral sentiment score, ranging from 0.0 to 1.0."}
            },
            "required": ["positive_score", "negative_score", "neutral_score"]
        }
    },
    {
        "name": "calculator",
        "description": "Adds two number",
        "input_schema": {
            "type": "object",
            "properties": {
                "num1": {"type": "number", "description": "first number to add"},
                "num2": {"type": "number", "description": "second number to add"},
            },
            "required": ["num1", "num2"]
        }
    }
]

def analyze_tweet_sentiment(query):

    prompt = f"""
    Analyze the sentiment in the following tweet: 
    <tweet>{query}</tweet>
    """
    
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        tools=tools,
        # tool_choice={"type": "auto"},
        tool_choice={"type": "tool", "name": "print_sentiment_scores"},  # So let's force Claude to **always** use the `print_sentiment_scores` tool by updating `tool_choice`:
        messages=[{"role": "user", "content": prompt}]
    )
    print(response)

analyze_tweet_sentiment("Holy cow, I just made the most incredible meal!")
analyze_tweet_sentiment("Holy cow, I just made the most incredible meal!")




print("=================================================================")
print("======================== TOOL ANY ==============================")
print("=================================================================")
# ## Any

# The final option for `tool_choice` is `any`, which allows us to tell Claude, "You must call a tool, but you can pick which one."  Imagine we want to create a SMS chatbot using Claude.  The only way for this chatbot to actually "communicate" with a user is via SMS text message. 
def send_text_to_user(text):
    # Sends a text to the user
    # We'll just print out the text to keep things simple:
    print(f"TEXT MESSAGE SENT: {text}")

def get_customer_info(username):
    return {
        "username": username,
        "email": f"{username}@email.com",
        "purchases": [
            {"id": 1, "product": "computer mouse"},
            {"id": 2, "product": "screen protector"},
            {"id": 3, "product": "usb charging cable"},
        ]
    }

tools = [
    {
        "name": "send_text_to_user",
        "description": "Sends a text message to a user",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The piece of text to be sent to the user via text message"},
            },
            "required": ["text"]
        }
    },
    {
        "name": "get_customer_info",
        "description": "gets information on a customer based on the customer's username.  Response includes email, username, and previous purchases. Only call this tool once a user has provided you with their username",
        "input_schema": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "The username of the user in question. "},
            },
            "required": ["username"]
        }
    },
]

system_prompt = """
All your communication with a user is done via text message.
Only call tools when you have enough information to accurately call them.  
Do not call the get_customer_info tool until a user has provided you with their username. This is important.
If you do not know a user's username, simply ask a user for their username.
"""

def sms_chatbot(user_message):
    messages = [{"role": "user", "content":user_message}]

    response = client.messages.create(
        system=system_prompt,
        model=MODEL_NAME,
        max_tokens=4096,
        tools=tools,
        tool_choice={"type": "any"},
        messages=messages
    )
    if response.stop_reason == "tool_use":
        last_content_block = response.content[-1]
        if last_content_block.type == 'tool_use':
            tool_name = last_content_block.name
            tool_inputs = last_content_block.input
            print(f"=======Claude Wants To Call The {tool_name} Tool=======")
            if tool_name == "send_text_to_user":
                send_text_to_user(tool_inputs["text"])
            elif tool_name == "get_customer_info":
                print(get_customer_info(tool_inputs["username"]))
            else:
                print("Oh dear, that tool doesn't exist!")
            
    else:
        print("No tool was called. This shouldn't happen!")
    
sms_chatbot("Hey there! How are you?")
sms_chatbot("I need help looking up an order")
sms_chatbot("I need help looking up an order.  My username is jenny76")
sms_chatbot("askdj aksjdh asjkdbhas kjdhas 1+1 ajsdh")