# Exercise

# We've only just begun, so this exercise might feel a little underwhelming. It's always good to get some practice with the basics.

# Please do the following:
# 1. Create a new notebook or Python script.
# 2. Import the proper packages
# 3. Load your Anthropic API key
# 4. Ask Claude to tell you a joke and then print out the result (you can copy/paste the code above and tweak it)
from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")


client = Anthropic(api_key=my_api_key)

MODEL_NAME = "claude-3-haiku-20240307"


def get_completion(prompt, system_prompt=""):
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4000,
        temperature=0.0,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# Prompt
# PROMPT = "Who is the best basketball player of all time?"
PROMPT = "Who is the best basketball player of all time? Yes, there are differing opinions, but if you absolutely had to pick one player, who would it be?"

# Print Claude's response
print(get_completion(PROMPT))
