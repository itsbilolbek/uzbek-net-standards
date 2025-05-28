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
            words = re.findall(r"\b[\wʻʼ']+\b", entry.msgstr, re.UNICODE)
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
    else:
        print(f"No spelling issues found in '{args.po_file}'.")

