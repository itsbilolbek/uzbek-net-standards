import polib 
import re
from spylls.hunspell import Dictionary
import argparse


def load_dictionary():
    uzbek_dictionary = Dictionary.from_system("uz_UZ")

    if uzbek_dictionary is None:
        uzbek_dictionary = Dictionary.from_files("uz_UZ")

    if uzbek_dictionary is None:
        raise RuntimeError("Unable to load the Uzbek dictionary.")
    
    return uzbek_dictionary


def check_spelling(po_file_path, uzbek_dictionary):
    issues = []

    po = polib.pofile(po_file_path)
    
    for entry in po:
        if entry.msgstr:
            # Regex expression to match words, including those with apostrophes
            # (?<![%$]) - negative lookbehind to ensure the word does not start with % or $, for example: "%s" or "$1"
            # \b[\wʻʼ']+(?:-[\wʻʼ']+)*\b - matches words with optional hyphens and apostrophes
            pattern = re.compile(r"(?<![%$])\b[\wʻʼ']+(?:-[\wʻʼ']+)*\b", re.UNICODE)

            words = re.findall(pattern, entry.msgstr)
            for word in words:
                if not uzbek_dictionary.lookup(word):
                    suggestions = ", ".join(list(uzbek_dictionary.suggest(word)))
                    issues.append(f"Spelling issue in '{entry.msgid}': '{word}' is misspelled. Suggestions: {suggestions}")

    return issues


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check spelling in a .po file.")
    parser.add_argument("po_file", help="Path to the .po file to normalize.")
    
    args = parser.parse_args()
    
    uzbek_dictionary = load_dictionary()
    
    issues = check_spelling(args.po_file, uzbek_dictionary)
    
    if issues:
        print(f"Spelling issues found in '{args.po_file}':")
        for issue in issues:
            print(issue)
            print()
    else:
        print(f"No spelling issues found in '{args.po_file}'.")

