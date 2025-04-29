from ollama import chat
from ollama import ChatResponse
import requests
# Query a chatbot using Ollama's API to analyze text chunks and save the results.

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

# read an input file with the list of the characters
with open("characters.txt", "r") as f:
    characters = [line.strip() for line in f]

# create a prompt for chatbot

#model_name = 'llama3.2:1b'
model_name = 'llama3.2:latest'
#model_name = 'qwen3:8b'

prompt = f"""
    You are an expert in literature and cultural analysis. 
    Based on names and their typical cultural associations, 
    assign a likely gender (e.g., Male, Female, or Unknown) to each character in the following list. 
    If the gender cannot be determined based on the name alone, assign "Unknown".
    If the name starts with Mr., it's Male.
    If the name starts with Mrs., it's Female.
    For each character, just provide the assigned gender without more data.

    Don't forget any characters from the list.

    Characters:
"""

prompt += "\n".join([f"- {character}" for character in characters])

with open('characters_query.txt', 'w', encoding='utf-8') as query_file:
    query_file.write(prompt)
response = query_ollama_via_api(model_name, prompt)

if not response:
    print("No response from the model.")
    exit()

with open('characters_response.txt', 'w', encoding='utf-8') as results_file:
    results_file.write(response)