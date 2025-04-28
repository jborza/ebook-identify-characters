import csv

#read an input csv file with the following columns:
#        "Speaker" and "Text".
# list all unique speakers in the file and print them to the console.

def list_speakers(filename):
    speakers = set()
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            speakers.add(row["Speaker"])
    return speakers

def is_character_male(speaker):
    # Placeholder function to determine if a character
    if 'Bill' in speaker or 'Jack ' in speaker or 'Man' in speaker or 'Son' in speaker:
        return True
    elif 'Mrs' in speaker or 'Miss' in speaker or 'Ms.' in speaker:
        return False
    elif 'Shirley' in speaker:
        return False
    elif 'Mr' in speaker or 'Sir' in speaker:
        return True
    elif 'Narrated' in speaker or 'Villagers' in speaker:   
        return True
    else:
        print(f"{speaker} is unknown")

if __name__ == "__main__":
    filename = "books/lottery-gpt4o-output_20250428_180407.txt"
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
    with open("voices.txt", "r") as f:
        voices = [line.strip() for line in f]
    print("Voices:")
    for voice in voices:
        print(voice)
    print(f"Total voices: {len(voices)}")
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
    # save the list of speakers to a file
    with open("speakers_to_voices.txt", "w") as f:
        for speaker, voice in speakers_to_voices.items():
            f.write(f"{speaker}: {voice}\n")