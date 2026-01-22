from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=my_api_key)
MODEL_NAME = "claude-3-haiku-20240307"  # "claude-3-sonnet-20240229"

########################
####### EXERCISE #######
########################

import wikipedia

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

generate_wikipedia_reading_list_tool = {
    "name": "generate_wikipedia_reading_list",
    "description": "Search for the wikipedia link and return a list of article and topic",
    "input_schema": {
        "type": "object",
        "properties": {
            "research_topic": {
                "type": "string",
                "description": "The name of the topic, e.g. 'The history of Hawaii' or 'Pirates across the world'",
            },
            "article_titles": {
                "type": "string",
                # "enum": ["electronics", "clothing", "home", "toys", "sports"],
                "description": "The list of the article title",
            },
        },
        "required": ["research_topic", "article_titles"],
    },
}


def generate_wikipedia_reading_list(research_topic, article_titles):
    print("----------------------")
    print(research_topic)
    print(article_titles)
    wikipedia_articles = []
    for t in article_titles:
        results = wikipedia.search(t)
        try:
            page = wikipedia.page(results[0])
            title = page.title
            url = page.url
            wikipedia_articles.append({"title": title, "url": url})
        except:
            continue
    add_to_research_reading_file(wikipedia_articles, research_topic)


def add_to_research_reading_file(articles, topic):
    with open("output/research_reading.md", "a", encoding="utf-8") as file:
        file.write(f"## {topic} \n")
        for article in articles:
            title = article["title"]
            url = article["url"]
            file.write(f"* [{title}]({url}) \n")
        file.write(f"\n\n")


# L'idea è che Claude "chiami" `generate_wikipedia_reading_list` con un elenco di potenziali titoli di articoli che potrebbero essere reali o meno.
# Claude potrebbe passare il seguente elenco di titoli di articoli, alcuni dei quali sono articoli reali di Wikipedia e altri no:
def get_research_help(topic, num_articles=3):
    messages = [
        {
            "role": "user",
            "content": f"Generate a list of ${num_articles} articles from Wikipedia for this topic:  ${topic}",
        }
    ]
    response = client.messages.create(
        model=MODEL_NAME,
        system="You have access to tools, but only use them when necessary. If a tool is not required, respond as normal",
        messages=messages,
        max_tokens=500,
        tools=[generate_wikipedia_reading_list_tool],
    )
    # print(response)
    print(response.content)
    if response.stop_reason == "tool_use":
        tool_use = response.content[-1]
        print("Tool use ", tool_use)
        tool_name = tool_use.name
        print("Tool name ", tool_name)
        tool_input = tool_use.input
        print("Tool input ", tool_input)

        if tool_name == "generate_wikipedia_reading_list":
            print("Claude wants to use the generate_wikipedia_reading_list tool")
            research_topic = tool_input["research_topic"]
            print(research_topic)
            article_titles = tool_input["article_titles"]
            print(article_titles)
            try:
                result = generate_wikipedia_reading_list(research_topic, article_titles)
                print("Result is:", result)
            except ValueError as e:
                print(f"Error: {str(e)}")

    elif response.stop_reason == "end_turn":
        print("Claude didn't want to use a tool")
        print("Claude responded with:")
        print(response.content[0].text)


# get_research_help("Pirates Across The World", 7)
# get_research_help("History of Hawaii", 3)
# get_research_help("are animals conscious?", 3)

get_research_help("Pirates Across The World", 1)

# Tool input  {'research_topic': 'Pirates Across The World', 'article_titles': '["History of Piracy", "Pirate ships", "Famous Pirate Captains", "Golden Age of Piracy", "Pirate Code", "Pirate Treasure and Loot", "Pirate Myths and Legends", "Piracy in the Caribbean"]'}
# generate_wikipedia_reading_list(
#     "Pirates Across The World",
#     [
#         "History of Piracy",
#         "Pirate ships",
#         "Famous Pirate Captains",
#         "Golden Age of Piracy",
#         "Pirate Code",
#         "Pirate Treasure and Loot",
#         "Pirate Myths and Legends",
#         "Piracy in the Caribbean",
#     ],
# )
