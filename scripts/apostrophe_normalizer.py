import polib, re, argparse

def normalize_apostrophes(text: str) -> str:
    text = re.sub("O'", "Oʻ", text)
    text = re.sub("o'", "oʻ", text)
    text = re.sub("G'", "Gʻ", text)
    text = re.sub("g'", "gʻ", text)
    text = re.sub("'", "ʼ", text)
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize apostrophes in a file.")
    parser.add_argument("--file", help="Path to the file to normalize.", required=True)
    parser.add_argument("--output", help="Path to save the normalized file. If not provided, the input file will be overwritten.", required=False)
    
    args = parser.parse_args()

    if args.file is None:
        print("Please provide a path to the .po file using --file argument.")
        exit(1)
    elif args.file.endswith('.po'):
        po = polib.pofile(args.file)
    
        # Define a regex pattern to match different apostrophe characters
        # apostrophe_pattern = re.compile(r"[’‘`]")
        
        
        # Iterate through each entry in the .po file
        for entry in po:
            if entry.msgstr:
                # Replace all variations of apostrophes with the standard single quote
                entry.msgstr = normalize_apostrophes(entry.msgstr)
                # xozir bu yerga '' gap sifatida kelsa 2 ta tutuq belgi boʻlib qolmasin
                # tayyor roʻyhat boʻlganida soʻzlarni search qilib replace qilardik manimcha
        
        # Save the changes back to the .po file
        if args.output:
            po.save(args.output)
            print(f"Apostrophes in '{args.file}' have been normalized and saved to '{args.output}'.")
        else:
            po.save(args.file)
            print(f"Apostrophes in '{args.file}' have been normalized.")
    else:
        # normalize apostrophes for each line of a file
        with open(args.file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        normalized_lines = [normalize_apostrophes(line) for line in lines]
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.writelines(normalized_lines)
            print(f"Apostrophes in '{args.file}' have been normalized and saved to '{args.output}'.")
        else:
            args.output = args.file
            with open(args.file, 'w', encoding='utf-8') as f:
                f.writelines(normalized_lines)
            print(f"Apostrophes in '{args.file}' have been normalized.")
           

        
