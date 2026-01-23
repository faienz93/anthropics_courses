from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=my_api_key)
MODEL_NAME = "claude-3-haiku-20240307"  # "claude-3-sonnet-20240229"


# In questa lezione, cercheremo di "ingannare" Claude parlando di uno strumento particolare, ma in realtà non avremo bisogno di chiamare la funzione sottostante dello strumento. 
# Utilizziamo lo strumento come un modo per forzare una struttura di risposta specifica, come mostrato in questo diagramma:


import wikipedia

#tool definition
tools = [
    {
        "name": "print_article_classification",
        "description": "Prints the classification results.",
        "input_schema": {
            "type": "object",
            "properties": {
                "subject": {
                    "type": "string",
                    "description": "The overall subject of the article",
                },
                "summary": {
                    "type": "string",
                    "description": "A paragaph summary of the article"
                },
                "keywords": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "List of keywords and topics in the article"
                    }
                },
                "categories": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "The category name."},
                            "score": {"type": "number", "description": "The classification score for the category, ranging from 0.0 to 1.0."}
                        },
                        "required": ["name", "score"]
                    }
                }
            },
            "required": ["subject","summary", "keywords", "categories"]
        }
    }
]

import json
#The function that generates the json for a given article subject
def generate_json_for_article(subject):
    page = wikipedia.page(subject, auto_suggest=True)
    query = f"""
    <document>
    {page.content}
    </document>

    Use the print_article_classification tool. Example categories are Politics, Sports, Technology, Entertainment, Business.
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        tools=tools,
        messages=[{"role": "user", "content": query}]
    )

    json_classification = None
    for content in response.content:
        if content.type == "tool_use" and content.name == "print_article_classification":
            json_classification = content.input
            break

    if json_classification:
        print("Text Classification (JSON):")
        print(json.dumps(json_classification, indent=2))
    else:
        print("No text classification found in the response.")

generate_json_for_article("Jeff Goldblum")

######################
# Output
######################
# Text Classification (JSON):
# {
#   "subject": "Jeff Goldblum - American actor and musician",
#   "summary": "This article provides a detailed biography of American actor and musician Jeff Goldblum, covering his early life, career highlights, personal life, and legacy. It discusses his breakout roles in films like Jurassic Park and Independence Day, his work in Wes Anderson films, his jazz music career, and more.",
#   "keywords": [
#     "Jeff Goldblum",
#     "actor",
#     "musician",
#     "Jurassic Park",
#     "Independence Day",
#     "Wes Anderson",
#     "jazz",
#     "biography"
#   ],
#   "categories": [
#     {
#       "name": "Entertainment",
#       "score": 0.9
#     }
#   ]
# }

def translate(sentence):
    page = wikipedia.page(sentence, auto_suggest=True)
    query = f"""
    <document>
    {page.content}
    </document>

    Use the print_article_classification tool. Example categories are Politics, Sports, Technology, Entertainment, Business.
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        tools=tools,
        messages=[{"role": "user", "content": query}]
    )

    json_classification = None
    for content in response.content:
        if content.type == "tool_use" and content.name == "print_article_classification":
            json_classification = content.input
            break

    if json_classification:
        print("Text Classification (JSON):")
        print(json.dumps(json_classification, indent=2))
    else:
        print("No text classification found in the response.")
translate("how much does this cost")