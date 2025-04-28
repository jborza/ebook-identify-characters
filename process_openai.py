import openai
import re
from dotenv import load_dotenv
import os

load_dotenv()
# Set up your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt4o_process_chunk(chunk):
    """
    Sends a chunk of text to GPT-4o for tagging as Narrated or Dialogue using the ChatCompletion API.
    """
    system_message = (
        "You are a helpful assistant that processes text to identify narration vs. dialogue and attributes dialogue to characters. "
        "For each sentence, prefix it with 'Narrated:' or '[Character Name]:', depending on whether it is narration or dialogue. "
        "If the speaker is unknown, use '[Unknown]:'."
    )
    user_message = f"Analyze the following text:\n\n{chunk}"
    
    try:
        client = openai.OpenAI()  # New client-based interface
        response = client.chat.completions.create(
            model="gpt-4o",  # or "gpt-4", "gpt-4-turbo"
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            max_tokens=2000,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error processing chunk: {e}")
        return None
        print(f"Error processing chunk: {e}")
        return None
    
def process_book(file_path):
    """
    Reads the book text, processes it chunk by chunk using GPT-4o, and saves the output.
    """
    # Read the book text
    with open(file_path, "r", encoding="utf-8") as file:
        book_text = file.read()

    # Split the text into manageable chunks (e.g., paragraphs)
    chunks = re.split(r'\n\s*\n', book_text)  # Split by blank lines

    # processed_chunks = []
    # for i, chunk in enumerate(chunks):
    #     print(f"Processing chunk {i + 1} of {len(chunks)}...")
    #     processed_chunk = gpt4o_process_chunk(chunk)
    #     if processed_chunk:
    #         processed_chunks.append(processed_chunk)

    chunk = book_text
    processed_chunks = [gpt4o_process_chunk(chunk)]

    # Combine all processed chunks
    processed_text = "\n\n".join(processed_chunks)

    # Save the processed text to a new file
    output_file = file_path.replace(".txt", "_processed.txt")
    with open(output_file, "w", encoding="utf-8") as output:
        output.write(processed_text)

    print(f"Processing complete! Output saved to '{output_file}'.")

if __name__ == "__main__":
    # Specify the path to your book file
    book_file_path = "sample_hut.txt"

    # Process the book
    process_book(book_file_path)