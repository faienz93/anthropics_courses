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
    # additional_info = "It'is importart answer in Italian arguing in Italian and not resume in Italian."
    additional_info = "Trasnlate in Italian before response"
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4000,
        temperature=0.0,
        system=f"{system_prompt}. {additional_info}",
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# -------
# Prompt
# PROMPT = "In one sentence, what do you think about skateboarding?"

# # Print Claude's response
# print(get_completion(PROMPT))

# --------
# System prompt
# SYSTEM_PROMPT = "You are a cat."

# # Prompt
# PROMPT = "In one sentence, what do you think about skateboarding?"

# # Print Claude's response
# print(get_completion(PROMPT, SYSTEM_PROMPT))

# SYSTEM_PROMPT = "You are a logic bot designed to answer complex logic problems."
# PROMPT = "Jack is looking at Anne. Anne is looking at George. Jack is married, George is not, and we don't know if Anne is married. Is a married person looking at an unmarried person?"

# # Print Claude's response
# print(get_completion(PROMPT))

# -------
SYSTEM_PROMPT = ""

# Prompt
PROMPT = """Is this equation solved correctly below?

2x - 3 = 9
2x = 6
x = 3"""

# Get Claude's response
response = get_completion(PROMPT, SYSTEM_PROMPT)


# Function to grade exercise correctness
def grade_exercise(text):
    if "incorrect" in text or "not correct" in text.lower():
        return True
    else:
        return False


# Print Claude's response and the corresponding grade
print(response)
print("\n--------------------------- GRADING ---------------------------")
print("This exercise has been correctly solved:", grade_exercise(response))
