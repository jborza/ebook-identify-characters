import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the system prompt and user message
system_prompt = "You are a helpful assistant that formats text into CSV with 'Speaker' and 'Text' columns according to specific rules."
user_prompt = """
Analyze the following text and output a CSV format with two columns: "Speaker" and "Text".

1. Spoken dialogue should be labeled with the character name in the "Speaker" column, and the spoken words in the "Text" column.
2. Narration (such as "said the girl" or scene descriptions) should be labeled as Narrated in the "Speaker" column, with the narration in the "Text" column.
3. If dialogue and narration are mixed in a sentence, separate them into two rows: one for dialogue, one for narration.
4. Wrap text in double quotes if it contains commas.
5. If consecutive sentences originate from the same speaker (whether a character or "Narrated"), concatenate them into one row instead of separate rows.


Here is the text:
“Joffrey likes your sister,” Jeyne whispered, proud as if she had something to do with it.
She was the daughter of Winterfell’s steward and Sansa’s dearest friend. “He told her she
was very beautiful.”
“He’s going to marry her,” little Beth said dreamily, hugging herself. “Then Sansa will be
queen of all the realm.”
Sansa had the grace to blush. She blushed prettily. She did everything prettily, Arya
thought with dull resentment. “Beth, you shouldn’t make up stories,” Sansa corrected
the younger girl, gently stroking her hair to take the harshness out of her words. She
looked at Arya. “What did you think of Prince Joff, sister? He’s very gallant, don’t you
think?”
“Jon says he looks like a girl,” Arya said.
Sansa sighed as she stitched. “Poor Jon,” she said. “He gets jealous because he’s a
bastard.”
“He’s our brother,” Arya said, much too loudly. Her voice cut through the afternoon
quiet of the tower room.
Septa Mordane raised her eyes. She had a bony face, sharp eyes, and a thin lipless mouth
made for frowning. It was frowning now. “What are you talking about, children?”
“Our half brother,” Sansa corrected, soft and precise. She smiled for the septa. “Arya and
I were remarking on how pleased we were to have the princess with us today,” she said.
Septa Mordane nodded. “Indeed. A great honor for us all.” Princess Myrcella smiled
uncertainly at the compliment. “Arya, why aren’t you at work?” the septa asked. She rose
to her feet, starched skirts rustling as she started across the room. “Let me see your
stitches.”
Arya wanted to scream. It was just like Sansa to go and attract the septa’s attention.
“Here,” she said, surrendering up her work.
The septa examined the fabric. “Arya, Arya, Arya,” she said. “This will not do. This will
not do at all.”
"""

# Call the API
response = client.chat.completions.create(
    model="gpt-4.1-mini",
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
