from dotenv import load_dotenv
import os
from anthropic import Anthropic

# Esempio su come migliorare un prompt

load_dotenv()
my_api_key = os.getenv("ANTHROPIC_API_KEY")


client = Anthropic(api_key=my_api_key)

MODEL_NAME = "claude-3-haiku-20240307"  # "claude-3-sonnet-20240229"
import re
import json

eval_data = [
    {"animal_statement": "The animal is a human.", "golden_answer": "2"},
    {"animal_statement": "The animal is a snake.", "golden_answer": "0"},
    {"animal_statement": "The fox lost a leg, but then magically grew back the leg he lost and a mysterious extra leg on top of that.", "golden_answer": "5"},
    {"animal_statement": "The animal is a dog.", "golden_answer": "4"},
    {"animal_statement": "The animal is a cat with two extra legs.", "golden_answer": "6"},
    {"animal_statement": "The animal is an elephant.", "golden_answer": "4"},
    {"animal_statement": "The animal is a bird.", "golden_answer": "2"},
    {"animal_statement": "The animal is a fish.", "golden_answer": "0"},
    {"animal_statement": "The animal is a spider with two extra legs", "golden_answer": "10"},
    {"animal_statement": "The animal is an octopus.", "golden_answer": "8"},
    {"animal_statement": "The animal is an octopus that lost two legs and then regrew three legs.", "golden_answer": "9"},
    {"animal_statement": "The animal is a two-headed, eight-legged mythical creature.", "golden_answer": "8"},
]


print("=====================================================================")
print("============================ TENTATIVO 1 ============================")
print("=====================================================================")
def build_input_prompt(animal_statement):
    user_content = f"""You will be provided a statement about an animal and your job is to determine how many legs that animal has.
    
    Here is the animal statement.
    <animal_statement>{animal_statement}</animal_statement>
    
    How many legs does the animal have? Please respond with a number"""

    messages = [{'role': 'user', 'content': user_content}]
    return messages


print(build_input_prompt(eval_data[0]['animal_statement']))

from anthropic import Anthropic
from dotenv import load_dotenv


def get_completion(messages):
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=200,
        messages=messages
    )
    return response.content[0].text

# full_prompt = build_input_prompt(eval_data[0]['animal_statement'])
# result = get_completion(full_prompt)
# print(result)

outputs = [get_completion(build_input_prompt(question['animal_statement'])) for question in eval_data]
print(outputs)

for output, question in zip(outputs, eval_data):
    print(f"Animal Statement: {question['animal_statement']}\nGolden Answer: {question['golden_answer']}\nOutput: {output}\n")


def grade_completion(output, golden_answer):
    return output == golden_answer

grades = [grade_completion(output, question['golden_answer']) for output, question in zip(outputs, eval_data)]
print(f"Score: {sum(grades)/len(grades)*100}%")

print("=====================================================================")
print("============================ TENTATIVO 2 ============================")
print("=====================================================================")
def build_input_prompt2(animal_statement):
    user_content = f"""You will be provided a statement about an animal and your job is to determine how many legs that animal has.
    
    Here is the animal statement.
    <animal_statement>{animal_statement}</animal_statement>
    
    How many legs does the animal have? Respond only with a numeric digit, like 2 or 6, and nothing else."""

    messages = [{'role': 'user', 'content': user_content}]
    return messages

outputs2 = [get_completion(build_input_prompt2(question['animal_statement'])) for question in eval_data]
print(outputs2)

for output, question in zip(outputs2, eval_data):
    print(f"Animal Statement: {question['animal_statement']}\nGolden Answer: {question['golden_answer']}\nOutput: {output}\n")

grades = [grade_completion(output, question['golden_answer']) for output, question in zip(outputs2, eval_data)]
print(f"Score: {sum(grades)/len(grades)*100}%")

print("=====================================================================")
print("============================ TENTATIVO 3 ============================")
print("=====================================================================")
def build_input_prompt3(animal_statement):
    user_content = f"""You will be provided a statement about an animal and your job is to determine how many legs that animal has.
    
    Here is the animal statement.
    <animal_statement>{animal_statement}</animal_statement>
    
    How many legs does the animal have? 
    Start by reasoning about the numbers of legs the animal has, thinking step by step inside of <thinking> tags.  
    Then, output your final answer inside of <answer> tags. 
    Inside the <answer> tags return just the number of legs as an integer and nothing else."""

    messages = [{'role': 'user', 'content': user_content}]
    return messages

outputs3 = [get_completion(build_input_prompt3(question['animal_statement'])) for question in eval_data]
for output, question in zip(outputs3, eval_data):
    print(f"Animal Statement: {question['animal_statement']}\nGolden Answer: {question['golden_answer']}\nOutput: {output}\n")

import re
def extract_answer(text):
    pattern = r'<answer>(.*?)</answer>'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None
    
extracted_outputs3 = [extract_answer(output) for output in outputs3]
print(extracted_outputs3)

grades3 = [grade_completion(output, question['golden_answer']) for output, question in zip(extracted_outputs3, eval_data)]
print(f"Score: {sum(grades3)/len(grades3)*100}%")