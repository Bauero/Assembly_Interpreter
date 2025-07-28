import os
from spellchecker import SpellChecker

def find_misspelled_words_in_file(file_path):
    # Initialize the spell checker
    spell = SpellChecker()
    
    # Read the file content with error handling for encoding issues
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            content = file.read()
    
    # Split the content into words
    words = content.split()
    
    # Find misspelled words
    misspelled_words = spell.unknown(words)
    
    return misspelled_words

def find_misspelled_words_in_directory(directory_path):
    misspelled_words = {}
    
    # Walk through the directory
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):  # Check only Python files
                file_path = os.path.join(root, file)
                misspelled_words[file_path] = find_misspelled_words_in_file(file_path)
    
    return misspelled_words

# Example usage
directory_path = './program_code'
misspelled_words = find_misspelled_words_in_directory(directory_path)

misspelled = []

for file_path, words in misspelled_words.items():
    if words:
        words = list(filter(lambda w: w.isalpha(), words))
        misspelled.extend(words)

output = "\n".join(sorted(set(misspelled)))

print(output)