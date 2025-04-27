import os
import re

def split_text_by_sentences(input_file, output_dir, max_sentences=50):
    """
    Splits a text file into smaller chunks based on sentence count.

    Args:
        input_file (str): Path to the input file containing the chapter.
        output_dir (str): Directory to save the output chunks.
        max_sentences (int): Maximum number of sentences per chunk.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Use regex to split the text into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Group sentences into chunks
    chunks = []
    current_chunk = []
    for sentence in sentences:
        current_chunk.append(sentence)
        if len(current_chunk) >= max_sentences:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    # Add any remaining sentences as the last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    # Write each chunk to a separate file
    for idx, chunk in enumerate(chunks):
        chunk_file = os.path.join(output_dir, f'chunk_{idx + 1}.txt')
        with open(chunk_file, 'w', encoding='utf-8') as file:
            file.write(chunk)
        print(f"Chunk {idx + 1} saved to {chunk_file}")

if __name__ == "__main__":
    # Example usage
    input_file = "chapters\\chapter-04.txt"  # Replace with your chapter file
    output_dir = "chapter_04"  # Directory to save the chunks
    max_sentences = 50  # Adjust this for the desired number of sentences per chunk

    split_text_by_sentences(input_file, output_dir, max_sentences)