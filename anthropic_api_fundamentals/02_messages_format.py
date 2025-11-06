from dotenv import load_dotenv
from anthropic import Anthropic

#load environment variable
load_dotenv()

#automatically looks for an "ANTHROPIC_API_KEY" environment variable
client = Anthropic()

def translate(word, language):
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": f"Translate ${word} to {language}. Respond with a single word"}
        ]
    )
    print(response.content[0].text)

translate("hello", "Spanish")
# 'The word "hello" translated into Spanish is: Hola'

translate("chicken", "Italian")
# 'The Italian word for "chicken" is: pollo'