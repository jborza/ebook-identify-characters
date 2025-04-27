import subprocess

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

if __name__ == "__main__":
    # Example usage
    model_name = "llama2"  # Replace with the installed model name (e.g., "llama2", "mistral", etc.)
    prompt = """
    Analyze the following text and identify whether each sentence is narrated or spoken by a character. 
    Provide the speaker's name if applicable:
    
    He waved his wand, but nothing happened. Scabbers stayed gray and fast asleep.

    “Are you sure that’s a real spell?” said the girl. “Well, it’s not very good, is it? I’ve 
    tried a few simple spells just for practice and it’s all worked for me. Nobody in my 
    family’s magic at all, it was ever such a surprise when I got my letter, but I was ever 
    so pleased, of course, I mean, it’s the very best school of witchcraft there is, I’ve 
    heard — I’ve learned all our course books by heart, of course, I just hope it will be 
    enough — I’m Hermione Granger, by the way, who are you?”

    She said all this very fast.

Harry looked at Ron, and was relieved to see by his stunned face that he hadn’t learned all the course books by heart either.

“I’m Ron Weasley,” Ron muttered.

“Harry Potter,” said Harry.

“Are you really?” said Hermione. “I know all about you, of course — I got a few extra books for background reading, and you’re in Modern Magical History and The Rise and Fall of the Dark Arts and Great Wizarding Events of the Twentieth Century.”

“Am I?” said Harry, feeling dazed.


“Goodness, didn’t you know, I’d have found out everything I could if it was me,” said Hermione. “Do either of you know what House you’ll be in? I’ve been asking around, and I hope I’m in Gryffindor, it sounds by far the best; I hear Dumbledore himself was in it, but I suppose Ravenclaw wouldn’t be too bad. . . . Anyway, we’d better go and look for Neville’s toad. You two had better change, you know, I expect we’ll be there soon.”

And she left, taking the toadless boy with her.
    """
    
    response = query_ollama(model_name, prompt)
    print("Ollama Response:")
    print(response)