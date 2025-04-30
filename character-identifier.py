import re
import requests
from ollama import chat
from ollama import ChatResponse
# read an entire chapter
# separate the text into paragraphs

def query_ollama_via_api(model_name, prompt, base_url="http://localhost:11434/api/chat"):
    """
    Queries the Ollama REST API with a given prompt and returns the response.

    Args:
        model_name (str): The name of the Ollama model to use (e.g., "llama2").
        prompt (str): The input prompt to send to the model.
        base_url (str): The base URL of the Ollama REST API (default is localhost on port 11434).

    Returns:
        str: The response from the Ollama model.
    """
    try:
        # Prepare the payload
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }

        # Send the POST request to the Ollama API
        response: ChatResponse = chat(model=model_name, messages=[
        {
            'role': 'user',
            'content': prompt,
        },
        ])
        # Raise an error if the request failed
        #response.raise_for_status()

        # Return the response content
        return response['message']['content']
    except requests.exceptions.RequestException as e:
        print("Error querying Ollama API:", e)
        return None


# process each paragraph - that will be the input to the model

chapter_name = 'chapter-hp.txt'
with open(chapter_name, 'r', encoding='utf-8') as file:
    chapter_text = file.read()
    paragraphs = chapter_text.split('\n\n')  # Split by double newlines to get paragraphs

# Remove any leading/trailing whitespace from each paragraph
paragraphs = [para.strip() for para in paragraphs if para.strip()]  # Filter out empty paragraphs

def preprocess(paragraph):
    # separate sentences into new lines
    # in case of speech, separate the speech from the narration
    # speech is between “ and ”
    speech_pattern = r'“[^”]*”'
    # Replace each speech with itself on a new line
    def replacer(match):
        return '\n' + match.group(0) + '\n'
    result = re.sub(speech_pattern, replacer, paragraph)
    # Remove consecutive newlines for tidiness
    result = re.sub(r'\n+', '\n', result)
    return result.strip()

def no_dialogue(paragraph):
    # Check if there is any dialogue in the paragraph
    # Dialogue is defined as text between “ and ”
    return not bool(re.search(r'[“”]', paragraph))
    #return not bool(re.search(r'“^”]*”', paragraph))

results = []

for paragraph in paragraphs:
    text = preprocess(paragraph)
    if no_dialogue(text):
        # the entire paragraph is narration, so we can just return it as is
        results.append(('Narrated', text))
        continue
    # Prepare the prompt for the model
    prompt = f"""
    You're a helpful assistant that formats text into CSV with 'Speaker' and 'Text' columns according to specific rules.
    Analyze the following text and output a CSV format with two columns: "Speaker" and "Text".
    Don't output anything else.

    1. Spoken dialogue should be labeled with the character name in the "Speaker" column, and the spoken words in the "Text" column.
    2. Narration (such as “said the girl” or scene descriptions) should be labeled as Narrated in the "Speaker" column, with the narration in the "Text" column.

    Text:
    {text}
    """
    #model_name = 'llama3.2:1b'
    model_name = 'qwen3:1.7b'
    # Call the API
    response = query_ollama_via_api(model_name, prompt)
    print(response)