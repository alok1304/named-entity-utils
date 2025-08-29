import os
from pathlib import Path
import spacy
from licensedcode.frontmatter import load_frontmatter, dumps_frontmatter
from ignore_entities import IGNORED_NAMED_ENTITY
from licensedcode.legalese import common_license_words

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def remove_named_entities(text):
    """Remove PERSON, ORG, GPE entities from text unless kept or in LEGAL_TERMS."""
    doc = nlp(text)

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


def process_file(filepath, output=None, license_expression=None):
    """Process a single file while preserving metadata and trailing newlines."""
    content, metadata = load_frontmatter(filepath)


    core_content = content.rstrip()

    trailing_whitespace = content[len(core_content):]

    processed_content = core_content
    
    license_exp = metadata.get("license_expression")

    if license_expression and license_exp == license_expression:
        processed_content = remove_named_entities(core_content)


    recombined_text = dumps_frontmatter(processed_content.lstrip("\n"), metadata)

    final_text_to_write = recombined_text + trailing_whitespace

    out_path = Path(output) if output else filepath
    os.makedirs(out_path.parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(final_text_to_write)


def process_path(path, output=None, license_expression=None):
    """Process file or directory."""
    path = Path(path)
    if path.is_file():
        out_path = Path(output) if output else path
        process_file(path, output=out_path, license_expression=license_expression)
    elif path.is_dir():
        for root, _, files in os.walk(path):
            for file in files:
                fpath = Path(root) / file
                out_path = Path(output) / fpath.relative_to(path) if output else fpath
                process_file(fpath, output=out_path, license_expression=license_expression)
