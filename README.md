# named-entity-utils

A Python utility for removing named entity from text file.

This tool uses `spaCy` for Named Entity Recognition (NER) to detect entities like PERSON, ORG, and GPE.

---

## Features
- Remove PERSON, ORG, and GPE named entities from text.
- Ignore named entities which are in legalese.py
- Skip files containing copyright statements.

---

# Installation

Clone the repository and set up a virtual environment:

```
git clone https://github.com/alok1304/named-entity-utils.git
cd named-entity-utils
```
Create and activate virtual environment
```
python -m venv venv
```
On Linux/macOS
```
source venv/bin/activate
```
On Windows (PowerShell)
```
.\venv\Scripts\Activate.ps1
```

Install dependencies
```
pip install -r requirements.txt
```
        
Running Tests
Run tests using pytest:
```
python -m pytest -v tests/
```

# Usages 
After cloning this repository, you can mark extra phrases in any file or folder by running:
```
py src/remove_named_entities.py /path/to/file-or-folder
```
# Example
```
py named-entity-utils/src/remove_named_entities.py src/licensedcode/data/rules
```

