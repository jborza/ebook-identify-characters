import re
# read an entire chapter
# separate the text into paragraphs

# process each paragraph - that will be the input to the model

chapter_name = 'chapter-daenerys.txt'
with open(chapter_name, 'r') as file:
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
    result = re.sub(speech_pattern, replacer, text)
    # Remove consecutive newlines for tidiness
    result = re.sub(r'\n+', '\n', result)
    return result.strip()


for paragraph in paragraphs:
    text = preprocess(paragraph)
    # Prepare the prompt for the model
    prompt = f"""
    Analyze the following text and output a CSV format with two columns: "Speaker" and "Text".

    1. Spoken dialogue should be labeled with the character name in the "Speaker" column, and the spoken words in the "Text" column.
    2. Narration (such as “said the girl” or scene descriptions) should be labeled as Narrated in the "Speaker" column, with the narration in the "Text" column.

    Text:
    {paragraph}
    """