from dotenv import load_dotenv
from anthropic import Anthropic

# load environment variable
load_dotenv()

# automatically looks for an "ANTHROPIC_API_KEY" environment variable
client = Anthropic()


def translate(word, language):
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"Translate ${word} to {language}. Respond with a single word",
            }
        ],
    )
    print(response.content[0].text)


# Build a simple multi-turn command-line chatbot script. The messages format lends itself to building chat-based applications.  To build a chat-bot with Claude, it's as simple as:


# 1. Keep a list to store the conversation history
# 2. Ask a user for a message using `input()` and add the user input to the messages list
# 3. Send the message history to Claude
# 4. Print out Claude's response to the user
# 5. Add Claude's assistant response to the history
# 6. Go back to step 2 and repeat! (use a loop and provide a way for users to quit!)
def main():
    print("Start Conversation Claude")
    print("Digita un Nome o premi 'q' per uscire")
    while True:
        userInput = input("Please enter your name: ")
        if userInput == "q":
            break
        print(f"Hello, {userInput}")
    print("!! Grazie per aver usato Claude !!")


if __name__ == "__main__":
    main()
