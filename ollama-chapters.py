import os
import subprocess
from datetime import datetime

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
    

def append_timestamp(filename):
    # Get the current datetime and format it as 2023-10-01_12-00
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    base, extension = os.path.splitext(filename)
    return f"{base}_{current_time}{extension}"

def process_chunks(directory, model_name):
    """
    Processes all text chunks in the specified directory and analyzes them with Ollama.

    Args:
        directory (str): Path to the directory containing the text chunks.
        model_name (str): The name of the Ollama model to use (e.g., "llama2").
    """
    # Get all chunk files in the directory
    chunk_files = sorted([f for f in os.listdir(directory) if f.startswith("chunk_") and f.endswith(".txt")])

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

        results_path = os.path.join(directory, response_name)
        with open(results_path, 'w', encoding='utf-8') as results_file:
            results_file.write("Chunk File: " + chunk_file + "\n")
            results_file.write("Model: " + model_name + "\n")
            results_file.write(response)

        print(f"Results saved to {results_path}")

        return

if __name__ == "__main__":
    # Example usage
    directory = "chapter_03"  # Directory containing chunk files (e.g., chunk_1.txt, chunk_2.txt)
    model_name = "qwen2.5:latest"  # Replace with your desired model name (e.g., "llama2", "mistral")

    process_chunks(directory, model_name)