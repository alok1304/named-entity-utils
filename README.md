# named-entity-utils

A Python utility for removing named entity from text file.
This tool uses `spaCy` for Named Entity Recognition (NER) to detect entities like PERSON, ORG, and GPE.

---

## Features
- Remove PERSON, ORG, and GPE named entities from text.
- Ignore named entities which are in legalese.py.
- Ignore some name entities which is not an actual named entity.
- Also Igone name entities if they inside required-phrases.
- We can also get the duplicates rules files in json form.
- This is used add `extra-phrase` in rules.
- Also We do not remove named entity from rules if they have copyrights statements.

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
After cloning this repository, you can remove named entity in any file or folder by running:
```
py -m cli /path/to/file-or-folder -l (license-expression)
```
eg:
```
py -m cli src/licensedcode/data/rules/ -l bsd-new
```
Also this `--license-expression` or `l` is required

## Get Duplicate Rules in json form
```
py -m find_duplicates src/licensedcode/data/rules/ -o results.json
```

### For Converting CRLF to LF for Windows
Run this in terminal:
```
Get-ChildItem -Path "src/licensedcode/data/rules/*.RULE" | ForEach-Object { $rawContent = Get-Content -Path $_.FullName -Raw; $rawContent -replace "\r`n", "`n" | Set-Content -NoNewline -Path $_.FullName }
```
This convert rules CRLF to LF because removing named-entity from rules that changes LF to CRLF.


