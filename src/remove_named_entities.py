import sys
import os
import spacy
from ignore_entities import IGNORED_NAMED_ENTITY
from ignore_entities import COPYRIGHT_PHRASES
from legalese import common_license_words

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

def remove_named_entities(text):
    """
    Remove all named entities from the given text.
    """
    
    lower_text = text.lower()
    if any(phrase in lower_text for phrase in COPYRIGHT_PHRASES):
        print("[SKIPPED] File contains copyright statement.")
        return text 


    doc = nlp(text)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
      
    
    all_entities=[]
    for ent in doc.ents:
        if ((ent.label_ == "PERSON" or ent.label_ == "ORG" or ent.label_== "GPE") and ent.text not in IGNORED_NAMED_ENTITY
        and ent.text.lower() not in common_license_words):
            all_entities.append((ent.text,ent.label_))

    print(all_entities)    
    
    new_text = text
    # Remove PERSON entities starting from the end to avoid messing up offsets
    for ent in sorted(doc.ents, key=lambda x: x.start_char, reverse=True):
        if ((ent.label_ == "PERSON" or ent.label_ == "ORG" or ent.label_== "GPE") and ent.text not in IGNORED_NAMED_ENTITY
        and ent.text.lower() not in common_license_words):
            new_text = new_text[:ent.start_char] + new_text[ent.end_char:]
    
    return new_text


def process_file(file_path):
    """Process a single file and remove PERSON entities."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    updated_content = remove_named_entities(content)

    if updated_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"[TOOL] Cleaned PERSON entities in: {file_path}")

def run_tool(target_path):
    """Process a file or all files in a folder recursively."""
    if os.path.isfile(target_path):
        process_file(target_path)
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path):
                    process_file(file_path)
    else:
        print("[TOOL] Path does not exist!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/remove_named_entities.py /path/to/file-or-folder")
    else:
        run_tool(sys.argv[1])

