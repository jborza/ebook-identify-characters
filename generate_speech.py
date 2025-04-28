import os
import csv
import soundfile as sf
from kokoro import KPipeline
import numpy as np

def load_numpy_kpipeline():
    import numpy as np

    return np, KPipeline

# Import your Kokoro TTS setup
class KokoroTTS:
    def __init__(self, lang_code="a", speed=1.0, output_format="WAV", device="cpu"):
        # lang code: {'a': 'American English', 'b': 'British English', 'e': 'es', 'f': 'fr-fr', 'h': 'hi', 'i': 'it', 'p': 'pt-br', 'j': 'Japanese', 'z': 'Mandarin Chinese'}
        self.lang_code = lang_code
        self.speed = speed
        self.output_format = output_format
        self.device = device
        self.KPipeline = KPipeline
        self.tts = self.KPipeline(
            lang_code=self.lang_code, repo_id="hexgrad/Kokoro-82M", device=self.device
        )

    def synthesize(self, text, voice, output_path, split_pattern=None):
        """
        Generate speech from text and save it as a WAV file.

        :param text: The text to be synthesized.
        :param voice: The voice model to use for synthesis.
        :param output_path: Path to save the WAV file.
        :param split_pattern: Optional pattern to split text into smaller chunks.
        """

        # TODO cache voices
        generator = self.tts(
            text, voice=voice, speed=self.speed, split_pattern=split_pattern
        )
        audio_segments = []
        for gs, ps, audio in generator:
            if audio is not None:
                    # Only convert if it's a numpy array, not if already tensor
                    audio_tensor = audio 

                    audio_segments.append(audio_tensor)
        audio = np.concatenate(audio_segments)
        
        sf.write(output_path, audio, 24000, format=self.output_format)


def process_csv_and_generate_speech(input_csv, voice_mapping, output_dir):
    """
    Process the input CSV file, synthesize speech for each line, and save as WAV files.

    :param input_csv: Path to the input CSV file.
    :param voice_mapping: Dictionary mapping speakers to voice models.
    :param output_dir: Directory to save the output WAV files.
    """
    kokoro = KokoroTTS()  # Initialize Kokoro TTS
    with open(input_csv, "r", encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=1):
            speaker = row["Speaker"].strip()
            text = row["Text"].strip()

            # Get the voice for the speaker
            # TODO does caching work here?
            voice = voice_mapping.get(speaker, None)
            if not voice:
                print(f"Warning: No voice mapping found for speaker '{speaker}'. Skipping...")
                continue

            # Generate output WAV file name
            output_file = f"{output_dir}/{idx}.wav"

            # Generate speech and save to file
            kokoro.synthesize(text, voice, output_file)
            print(f"Generated speech for '{speaker}: {text}' -> {output_file}")


if __name__ == "__main__":
    # Input CSV file path
    input_csv = "dialogues.csv"

    # Output directory for WAV files
    output_dir = "output_wavs"
    # make sure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Speaker-to-voice mappings
    voice_mapping = {
        "Arya": "af_bella",
        "Sansa": "af_sky",
        "Narrated": "am_michael",
    }

    # Process the CSV and generate speech
    process_csv_and_generate_speech(input_csv, voice_mapping, output_dir)