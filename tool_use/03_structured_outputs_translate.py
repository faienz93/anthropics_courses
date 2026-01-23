from dotenv import load_dotenv
import os
from anthropic import Anthropic
import json
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
        "name": "print_translation",
        "description": "Translate the result.",
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


# tools2 = [
#     {
#         "name": "print_translation",
#         "description": "Translate the result.",
#         "input_schema": {
#             "type": "object",
#             "properties": {
#                 "languages": {
#                     "type": "string",
#                     "description": "The language name.",
#                 },
#                 "translate": {
#                     "type": "string",
#                     "description": "The translation for the languages from this: english, spanish, french, japanese, arabic, italian"
#                 }
#             },
#             "required": ["languages", "translate"]
#         }
#     }
# ]

tools = [
    {
        "name": "print_translation",
        "description": "Translate the result.",
        "input_schema": {
            "type": "object",
            "properties": {
                "languages": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "language": {"type": "string", "description": "The language name."},
                            "translate": {"type": "string", "description": "The translation for the languages from this: english, spanish, french, japanese, arabic, italian"}
                        },
                        "required": ["name", "score"]
                    }
                }
            },
            "required": ["languages"]
        }
    }
]

def translate(sentence):
    query = f"""
    <sentence>
    {sentence}
    </sentence>

    Only use the print_translation tool. Example languages are english, spanish, french, japanese, arabic, italian.
    """

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        tools=tools,
        messages=[{"role": "user", "content": query}]
    )

    translations_from_claude = None
    for content in response.content:
        if content.type == "tool_use" and content.name == "print_translation":
            translations_from_claude = content.input
            break

    if translations_from_claude:
        print("Text Translate (JSON):")
        # print(translations_from_claude)
        formatted_data = {item['language']: item['translate'] for item in translations_from_claude['languages']}
        print(json.dumps(formatted_data, ensure_ascii=False, indent=2))
    else:
        print("No trasnalte found in the response.")

translate("how much does this cost")

# {
#   "english": "how much does this cost",
#   "spanish": "¿cuánto cuesta esto?",
#   "french": "combien ça coûte?",
#   "japanese": "これはいくらですか",
#   "arabic": "كم تكلفة هذا؟"
# }