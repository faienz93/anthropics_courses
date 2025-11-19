# ### Your task

# Your task is to use Claude to do the following:
# * Transcribe the text in each of the 5 research paper images
# * Combine the text from each image into one large transcription
# * Provide the entire transription to Claude and ask for a non-technical summary of the entire paper.

# An example output might look something like this:

# >This paper explores a new type of attack on large language models (LLMs) like ChatGPT, called "Many-shot Jailbreaking" (MSJ). As LLMs have recently gained the ability to process much longer inputs, this attack takes advantage of that by showing the AI hundreds of examples of harmful or undesirable behavior. The researchers found that this method becomes increasingly effective as more examples are given, following a predictable pattern.

# >The study tested MSJ on several popular AI models and found it could make them produce harmful content they were originally designed to avoid. This includes things like violent or sexual content, deception, and discrimination. The researchers also discovered that larger AI models tend to be more susceptible to this type of attack, which is concerning as AI technology continues to advance.

# >The paper also looked at potential ways to defend against MSJ attacks. They found that current methods of training AI to be safe and ethical (like supervised learning and reinforcement learning) can help somewhat, but don't fully solve the problem. The researchers suggest that new approaches may be needed to make AI models truly resistant to these kinds of attacks. They emphasize the importance of continued research in this area to ensure AI systems remain safe and reliable as they become more powerful and widely used.

# To get the best results, we advise asking Claude to summarize each page in a separate request rather than providing all 5 images and asking for a single transcription of the entire paper.

from dotenv import load_dotenv
from anthropic import Anthropic

# load environment variable
load_dotenv()
# automatically looks for an "ANTHROPIC_API_KEY" environment variable
client = Anthropic()
conversation = []

import base64
import httpx

import base64
import mimetypes

research_paper_pages = [
    "./images/research_paper/page1.png",
    "./images/research_paper/page2.png",
    "./images/research_paper/page3.png",
    "./images/research_paper/page4.png",
    "./images/research_paper/page5.png",
]

# used_model = "claude-3-haiku-20240307"
used_model = "claude-3-5-sonnet-20240620"


# This wasn't a problem with Claude 3.5 Sonnet, but when working with other models it can be helpful to label each image with a text content block.
# Even something as simple as labeling the images as "Image 1", "Image 2", etc. can make a large difference.
def create_image_message(image_path):
    # Open the image file in "read binary" mode
    with open(image_path, "rb") as image_file:
        # Read the contents of the image as a bytes object
        binary_data = image_file.read()

    # Encode the binary data using Base64 encoding
    base64_encoded_data = base64.b64encode(binary_data)

    # Decode base64_encoded_data from bytes to a string
    base64_string = base64_encoded_data.decode("utf-8")

    # Get the MIME type of the image based on its file extension
    mime_type, _ = mimetypes.guess_type(image_path)

    # Create the image block
    # In questo caso sarà descritta l'immagine senza altri messaggi
    image_block = {
        "type": "image",
        "source": {"type": "base64", "media_type": mime_type, "data": base64_string},
    }

    return image_block


def get_image_dict_from_url(image_url):
    # Send a GET request to the image URL and retrieve the content
    response = httpx.get(image_url)
    image_content = response.content

    # Determine the media type of the image based on the URL extension
    # This is not a foolproof approach, but it generally works
    image_extension = image_url.split(".")[-1].lower()
    if image_extension == "jpg" or image_extension == "jpeg":
        image_media_type = "image/jpeg"
    elif image_extension == "png":
        image_media_type = "image/png"
    elif image_extension == "gif":
        image_media_type = "image/gif"
    else:
        raise ValueError("Unsupported image format")

    # Encode the image content using base64
    image_data = base64.b64encode(image_content).decode("utf-8")

    # Create the dictionary in the proper image block shape:
    image_dict = {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": image_media_type,
            "data": image_data,
        },
    }

    return image_dict


def generate_transcription(image_path):

    messages = [
        {
            "role": "user",
            "content": [
                create_image_message(image_path),
                {
                    "type": "text",
                    "text": "Transcribe the text in each of the paper image.",
                },
            ],
        },
    ]

    response = client.messages.create(
        model=used_model, max_tokens=2048, messages=messages
    )
    print(response.content[0].text)
    user_question = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": f"Image named {image_path}",
            },
        ],
    }
    assistant_response = {
        "role": "assistant",
        "content": [{"type": "text", "text": response.content[0].text}],
    }
    response = {"role": "assistant", "content": {response.content[0].text}}
    conversation.append(user_question)
    conversation.append(assistant_response)


if __name__ == "__main__":
    for document_image in research_paper_pages:
        print()
        print(document_image)
        print()
        generate_transcription(document_image)

    print()
    # print(conversation)
    print("Results")
    response = client.messages.create(
        model=used_model,
        system="Combine the text from each image into one large transcription. Then, summarize for a non-technical summary of the entire paper in Italian.",
        max_tokens=2048,
        messages=conversation,
    )

    # print(response)
    print(response.content[0].text)
