import re
import os

def main():
    input_file = "Harry Potter and the Sorcerer's - J.K. Rowling.txt"
    output_dir = "chapters"
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Split text on lines that start with "CHAPTER" followed by uppercase text for the chapter number.
    chapters = re.split(r'(?m)^(?=CHAPTER\s+[A-Z]+)', text)
    chapters = [ch for ch in chapters if ch.strip()]

    for i, chapter in enumerate(chapters, start=1):
        filename = os.path.join(output_dir, f"chapter-{i:02d}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(chapter)

    print(f"Split into {len(chapters)} chapters and saved in '{output_dir}' directory.")

if __name__ == "__main__":
    main()
