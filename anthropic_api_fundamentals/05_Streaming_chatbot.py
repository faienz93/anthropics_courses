# Build a simple multi-turn command-line chatbot script. The messages format lends itself to building chat-based applications.  To build a chat-bot with Claude, it's as simple as:


# 1. Keep a list to store the conversation history
# 2. Ask a user for a message using `input()` and add the user input to the messages list
# 3. Send the message history to Claude
# 4. Print out Claude's response to the user
# 5. Add Claude's assistant response to the history
# 6. Go back to step 2 and repeat! (use a loop and provide a way for users to quit!)


## Exercise

# Write a simple Claude chatbot that uses streaming. The following gif illustrates how it should work.  Please note that the color-coding of the output is completely optional and mostly helps to make the gif readable/watchable:

# ![streaming_chat_exercise.gif](attachment:streaming_chat_exercise.gif)

from dotenv import load_dotenv
from anthropic import Anthropic

# load environment variable
load_dotenv()

# automatically looks for an "ANTHROPIC_API_KEY" environment variable
client = Anthropic()
conversation = []
GREEN = "\033[32m"
BLUE = "\033[34m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_with_statistics(stream):
    final_message = []
    for event in stream:
        if event.type == "message_start":
            input_tokens = event.message.usage.input_tokens
            print("MESSAGE START EVENT", flush=True)
            print(f"Input tokens used: {input_tokens}", flush=True)
            print("========================")
        elif event.type == "content_block_delta":
            print(event.delta.text, flush=True, end="")
            final_message.append(event.delta.text)
        elif event.type == "message_delta":
            output_tokens = event.usage.output_tokens
            print("\n========================", flush=True)
            print("MESSAGE DELTA EVENT", flush=True)
            print(f"Output tokens used: {output_tokens}", flush=True)

    result_space = "".join(final_message)
    return result_space


def print_without_statistics(stream):
    final_message = []
    for event in stream:
        if event.type == "content_block_delta":
            print(f"{GREEN}{BOLD}{event.delta.text}", flush=True, end="")
            final_message.append(event.delta.text)

    # print(final_message)
    result_space = "".join(final_message)
    return result_space


def chatbot():
    stream = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=conversation,
        stream=True,
    )
    result = print_without_statistics(stream)
    claudeResponse = {
        "role": "assistant",
        "content": result,
    }
    conversation.append(claudeResponse)
    print()


def main():

    quit = "quit"
    print("Welcome to the Claude Chatbot!")
    print(f"Type '{quit}' to exit the chat.")
    while True:
        print(f"{BLUE}You:{RESET} ", end="", flush=True)
        userInput = input()
        if userInput == f"{quit}":
            break
        if userInput:
            userQuestion = {
                "role": "user",
                "content": userInput,
            }
            conversation.append(userQuestion)
            chatbot()
        # print(f"Hello, {userInput}")
    print("!! Grazie per aver usato Claude !!")


if __name__ == "__main__":
    main()
