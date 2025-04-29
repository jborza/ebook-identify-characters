import csv
import soundfile as sf
from kokoro import KPipeline
import numpy as np
import os

#read an input csv file with the following columns:
#        "Speaker" and "Text".

output_dir = "output_wavs_literotica"

def load_numpy_kpipeline():
    import numpy as np

    return np, KPipeline

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

        generator = self.tts(
            text, voice=voice, speed=self.speed, split_pattern=split_pattern
        )
        audio_segments = []
        for gs, ps, audio in generator:
            # most likely we'll generate the speech in the single pass
            if audio is not None:
                audio_tensor = audio 
                audio_segments.append(audio_tensor)
        audio = np.concatenate(audio_segments)
        sf.write(output_path, audio, 24000, format=self.output_format)

def list_speakers(filename):
    speakers = set()
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            speakers.add(row["Speaker"])
    return speakers

def is_character_male(speaker):
    # Placeholder function to determine if a character
    if speaker == "I":
        return True
    elif 'Wife' in speaker or 'Daughter' in speaker or 'wife' in speaker or 'daughter' in speaker:
        return False
    elif 'Bill' in speaker or 'Jack ' in speaker or 'Man' in speaker or 'Son' in speaker:
        return True
    elif 'Mrs' in speaker or 'Miss' in speaker or 'Ms.' in speaker:
        return False
    elif 'Shirley' in speaker:
        return False
    elif 'Mr' in speaker or 'Sir' in speaker:
        return True
    elif 'Narrated' in speaker:
        return False
    elif 'Villagers' in speaker:   
        return True
    else:
        print(f"{speaker} is unknown")

def load_voices():
    with open("voices.txt", "r") as f:
        voices = [line.strip() for line in f]
    return voices

def assign_voice_to_speakers(speakers, voices):
    speakers_to_voices = {}
    # identify which characters are m/f
    for speaker in speakers:
        # assign voices to speakers
        is_male = is_character_male(speaker)
        # pick first voice from list of voices that matches the gender
        gender = 'm' if is_male else 'f'
        voice_found = next((s for s in voices if len(s) > 1 and s[1] == gender), None)
        # remove the voice from the list of voices
        if voice_found:
            voices.remove(voice_found)
            speakers_to_voices[speaker] = voice_found
        else:
            print(f"No voice found for {speaker}")
    return speakers_to_voices

if __name__ == "__main__":
    filename = "literotica/welcome-back-gpt4o_20250429_163747.txt"

    speakers = list_speakers(filename)
    print("Speakers:")
    for speaker in speakers:
        print(speaker)
    print(f"Total unique speakers: {len(speakers)}")
    # save the list of speakers to a file
    with open("speakers.txt", "w") as f:
        for speaker in speakers:
            f.write(f"{speaker}\n")

    # assign speakers to voices
    # figure out which characters are male, which female
    # load list of voices from voices.txt
    voices = load_voices()

    speakers_to_voices = assign_voice_to_speakers(speakers, voices)
    # save the list of speakers to a file
    with open("speakers_to_voices.txt", "w") as f:
        for speaker, voice in speakers_to_voices.items():
            f.write(f"{speaker}: {voice}\n")

    os.makedirs(output_dir, exist_ok=True)

    kokoro = KokoroTTS()

    # now do the TTS for each line in the csv file
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=1):
            speaker = row["Speaker"].strip()
            text = row["Text"].strip()
            voice = speakers_to_voices.get(speaker, None)
            if not voice:
                print(f"Warning: No voice mapping found for speaker '{speaker}'. Skipping...")
                continue
            print(f"Speaker: {speaker}, Text: {text}, Voice: {voice}")
            voice = speakers_to_voices.get(speaker, None)
            if not voice:
                print(f"Warning: No voice mapping found for speaker '{speaker}'. Skipping...")
                continue
            # Generate output WAV file name
            output_file = f"{output_dir}/{idx:03}.wav"

            # Generate speech and save to file
            kokoro.synthesize(text, voice, output_file)
            print(f"Generated speech for '{speaker}: {text}' -> {output_file}")