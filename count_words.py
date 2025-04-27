#!/usr/bin/env python3
import argparse

def count_words(filename):
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return 0
    # Split the text into words using default whitespace splitting.
    words = text.split()
    return len(words)

def main():
    parser = argparse.ArgumentParser(description='Count the number of words in a text file.')
    parser.add_argument('file', help='Path to the text file')
    args = parser.parse_args()
    
    word_count = count_words(args.file)
    print(f"Word count: {word_count}")

if __name__ == '__main__':
    main()
