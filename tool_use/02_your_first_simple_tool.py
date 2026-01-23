from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=my_api_key)
MODEL_NAME = "claude-3-haiku-20240307"  # "claude-3-sonnet-20240229"


def calculator(operation, operand1, operand2):
    if operation == "add":
        return operand1 + operand2
    elif operation == "subtract":
        return operand1 - operand2
    elif operation == "multiply":
        return operand1 * operand2
    elif operation == "divide":
        if operand2 == 0:
            raise ValueError("Cannot divide by zero.")
        return operand1 / operand2
    else:
        raise ValueError(f"Unsupported operation: {operation}")



calculator_tool = {
    "name": "calculator",
    "description": "A simple calculator that performs basic arithmetic operations.",
    "input_schema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
                "description": "The arithmetic operation to perform.",
            },
            "operand1": {"type": "number", "description": "The first operand."},
            "operand2": {"type": "number", "description": "The second operand."},
        },
        "required": ["operation", "operand1", "operand2"],
    },
}


def prompt_claude(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=MODEL_NAME,
        system="You have access to tools, but only use them when necessary. If a tool is not required, respond as normal",
        messages=messages,
        max_tokens=500,
        tools=[calculator_tool],
    )
    print(response)
    # Message(id='msg_018GDAQZd1YHjBj8trtsJiTF',
    #   content=[
    #       TextBlock(citations=None, text="Okay, let's calculate how many chickens you have left.", type='text'),
    #       ToolUseBlock
    #       (
    #           id='toolu_01RwhSoStZ8WVMSVSg74xgpG',
    #           input={'operand1': 23, 'operand2': 2, 'operation': 'subtract'},
    #           name='calculator',
    #           type='tool_use'
    #       )],
    #   model='claude-3-haiku-20240307',
    #   role='assistant',
    #   stop_reason='tool_use',
    #   stop_sequence=None,
    #   type='message',
    #   usage=Usage(cache_creation=CacheCreation(ephemeral_1h_input_tokens=0, ephemeral_5m_input_tokens=0), cache_creation_input_tokens=0, cache_read_input_tokens=0, input_tokens=446, output_tokens=104, server_tool_use=None, service_tier='standard'))
    #
    # print(response.stop_reason)
    # 'tool_use'
    # response.content
    # [ToolUseBlock(id='toolu_015wQ7Wipo589yT9B3YTwjF1', input={'operand1': 1984135, 'operand2': 9343116, 'operation': 'multiply'}, name='calculator', type='tool_use')]
    if response.stop_reason == "tool_use":
        tool_use = response.content[-1]
        tool_name = tool_use.name
        tool_input = tool_use.input

        if tool_name == "calculator":
            print("Claude wants to use the calculator tool")
            operation = tool_input["operation"]
            operand1 = tool_input["operand1"]
            operand2 = tool_input["operand2"]

            try:
                result = calculator(operation, operand1, operand2)
                print("Calculation result is:", result)
            except ValueError as e:
                print(f"Error: {str(e)}")

    elif response.stop_reason == "end_turn":
        print("Claude didn't want to use a tool")
        print("Claude responded with:")
        print(response.content[0].text)


# prompt_claude("I had 23 chickens but 2 flew away.  How many are left?")
# prompt_claude("What is 201 times 2")
# prompt_claude("Write me a haiku about the ocean")


# search_product_tool = {
#     "name": "search_product",
#     "description": "Search for a product by name or keyword and return its current price and availability.",
#     "input_schema": {
#         "type": "object",
#         "properties": {
#             "query": {
#                 "type": "string",
#                 "description": "The product name or search keyword, e.g. 'iPhone 13 Pro' or 'wireless headphones'",
#             },
#             "category": {
#                 "type": "string",
#                 "enum": ["electronics", "clothing", "home", "toys", "sports"],
#                 "description": "The product category to narrow down the search results",
#             },
#             "max_price": {
#                 "type": "number",
#                 "description": "The maximum price of the product, used to filter the search results",
#             },
#         },
#         "required": ["query"],
#     },
# }

# sender_email_tool = {
#   "name": "send_email",
#   "description": "Sends an email to the specified recipient with the given subject and body.",
#   "input_schema": {
#     "type": "object",
#     "properties": {
#       "to": {
#         "type": "string",
#         "description": "The email address of the recipient"
#       },
#       "subject": {
#         "type": "string",
#         "description": "The subject line of the email"
#       },
#       "body": {
#         "type": "string",
#         "description": "The content of the email message"
#       }
#     },
#     "required": ["to", "subject", "body"]
#   }
# }