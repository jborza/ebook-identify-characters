import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# read the text from a file
with open("literotica/welcome-back.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Define the system prompt and user message
system_prompt = "You are a helpful assistant that formats text into CSV with 'Speaker' and 'Text' columns according to specific rules."
user_prompt = f"""
Analyze the following text and output a CSV format with two columns: "Speaker" and "Text".

1. Spoken dialogue should be labeled with the character name in the "Speaker" column, and the spoken words in the "Text" column.
2. Narration (such as "said the girl" or scene descriptions) should be labeled as Narrated in the "Speaker" column, with the narration in the "Text" column.
3. Only the spoken dialogue should get the character name label
4. If dialogue and narration are mixed in a sentence, separate them into two rows: one for dialogue, one for narration. Don't forget about this.
    for example
    "Jeyne","Joffrey likes your sister," Jeyne whispered, proud as if she had something to do with it.

    should be 
    "Jeyne","Joffrey likes your sister,"
    "Narrated","Jeyne whispered, proud as if she had something to do with it."

Here is the text:
{text}
"""

# Call the API
response = client.chat.completions.create(
    #model="gpt-4.1-mini",
    #model="gpt-4.1-nano",
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    temperature=0
)

# Print the output
output = response.choices[0].message.content.strip()
print(output)

from datetime import datetime

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
with open(f'output_{current_time}.txt', 'w') as f:
    f.write(output)
