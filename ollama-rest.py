import os
import subprocess
from datetime import datetime
import requests
from ollama import chat
from ollama import ChatResponse

def query_ollama(model_name, prompt):
    """
    Queries the Ollama model with a given prompt and returns the response.

    Args:
        model_name (str): The name of the Ollama model to use (e.g., "llama2").
        prompt (str): The input prompt to send to the model.

    Returns:
        str: The response from the Ollama model.
    """
    try:
        # Run the Ollama CLI command
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt,
            text=True,
            capture_output=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print("Error querying Ollama model:", e.stderr)
        return None
    
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

#    Replaces reserved characters: \/":<>|*? with an underscore.    
def sanitize_path(path_str):
    reserved_chars = r'\/":<>|*?'
    translation_table = str.maketrans({char: '_' for char in reserved_chars})
    return path_str.translate(translation_table)

def process_chunks_with_api(directory, model_name):
    """
    Processes all text chunks in the specified directory and analyzes them with the Ollama API.

    Args:
        directory (str): Path to the directory containing the text chunks.
        model_name (str): The name of the Ollama model to use (e.g., "llama2").
    """
    print(f"Processing chunks with model: {model_name}")
    # Get all chunk files in the directory
    #chunk_files = sorted([f for f in os.listdir(directory) if f.startswith("chunk_") and f.endswith(".txt")])

    chunk_files = [book_file_path]

    for chunk_file in chunk_files:
        chunk_path = os.path.join(directory, chunk_file)

        # Read the content of the chunk file
        with open(chunk_path, 'r', encoding='utf-8') as file:
            chunk_content = file.read()

        # Prepare the prompt for Ollama
        prompt = f"""
Analyze the following text and output a CSV format with two columns: "Speaker" and "Text".

1. Spoken dialogue should be labeled with the character name in the "Speaker" column, and the spoken words in the "Text" column.
2. Narration (such as "said the girl" or scene descriptions) should be labeled as Narrated in the "Speaker" column, with the narration in the "Text" column.
3. Only the spoken dialogue should get the character name label
4. If consecutive sentences originate from the same speaker (whether a character or "Narrated"), concatenate them into one row instead of separate rows.
5. If dialogue and narration are mixed in a sentence, separate them into two rows: one for dialogue, one for narration.
    for example
    "Jeyne","Joffrey likes your sister," Jeyne whispered, proud as if she had something to do with it.

    should be 
    "Jeyne","Joffrey likes your sister,"
    "Narrated","Jeyne whispered, proud as if she had something to do with it."
    Here is the text:
        {chunk_content}
        """

        # Query Ollama with the prompt via API
        print(f"Processing {chunk_file}...")
        response = query_ollama_via_api(model_name, prompt)

        with open('query.txt', 'w', encoding='utf-8') as query_file:
            query_file.write(prompt)

        # Save the response to a results file
        if response:

            response_name = f"{chunk_file.replace('.txt', '_results.txt')}"
            response_name = append_timestamp(response_name)
            response_name = append_model(response_name, model_name)
            response_name = sanitize_path(response_name)

            results_path = os.path.join(directory, response_name)
            with open(results_path, 'w', encoding='utf-8') as results_file:
                results_file.write(response)

            print(f"Results saved to {results_path}")
        else:
            print(f"Failed to process {chunk_file}")

        # TODO remove the return statement to process all chunks        
        return

    

def append_timestamp(filename):
    # Get the current datetime and format it as 2023-10-01_12-00
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    base, extension = os.path.splitext(filename)
    return f"{base}_{current_time}{extension}"

def append_model(filename, model_name):
    # Append the model name to the filename
    base, extension = os.path.splitext(filename)
    return f"{base}_{model_name}{extension}"

def process_chunks(directory, model_name):
    """
    Processes all text chunks in the specified directory and analyzes them with Ollama.

    Args:
        directory (str): Path to the directory containing the text chunks.
        model_name (str): The name of the Ollama model to use (e.g., "llama2").
    """
    # Get all chunk files in the directory
    #chunk_files = sorted([f for f in os.listdir(directory) if f.startswith("chunk_") and f.endswith(".txt")])
    chunk_files = [book_file_path]

    for chunk_file in chunk_files:
        chunk_path = os.path.join(directory, chunk_file)

        # Read the content of the chunk file
        with open(chunk_path, 'r', encoding='utf-8') as file:
            chunk_content = file.read()

        # Prepare the prompt for Ollama
        prompt = f"""
        Analyze the following text and identify whether each sentence is narrated or spoken by a character.
        Provide the speaker's name if applicable:

        Prefix each sentence with "Narrated:" or "[Character Name]:".
        

        {chunk_content}
        """

        # Query Ollama with the prompt
        print(f"Processing {chunk_file}...")
        response = query_ollama(model_name, prompt)

        # Save the response to a results file
        # append current time to the file name
        # e.g., chunk_1_results_2023-10-01_12-00.txt
        response_name = f"{chunk_file.replace('.txt', '_results.txt')}"
        response_name = append_timestamp(response_name)
        response_name = append_model(response_name, model_name)

        results_path = os.path.join(directory, response_name)
        with open(results_path, 'w', encoding='utf-8') as results_file:
            results_file.write("Chunk File: " + chunk_file + "\n")
            results_file.write("Model: " + model_name + "\n")
            results_file.write(response)

        print(f"Results saved to {results_path}")

        return

book_file_path = "prompt-text.txt"

if __name__ == "__main__":
    # Example usage
    directory = "local_llms"  # Directory containing chunk files (e.g., chunk_1.txt, chunk_2.txt)
    #model_name = "llama3.2:1b"  # Replace with your desired model name (e.g., "llama2", "mistral")
    process_chunks_with_api(directory, "qwen3:8b")
    process_chunks_with_api(directory, "qwen2.5-coder:14b")
    process_chunks_with_api(directory, "llama3.2:latest")