import spacy
import re
from typing import Dict, Any, Optional, List

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading 'en_core_web_sm'...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
    'python', 'java', 'c++', 'javascript', 'sql', 'react', 'docker', 'kubernetes', 'aws',
    'azure', 'gcp', 'machine learning', 'deep learning', 'nlp', 'data analysis',
    'project management', 'agile', 'scrum', 'leadership'
]

def extract_name(doc: spacy.tokens.Doc) -> Optional[str]:
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()
    return None

def extract_email(text: str) -> Optional[str]:
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group(0) if match else None

def extract_skills(text: str) -> List[str]:
    found_skills = set()
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.add(skill.title())
    return sorted(list(found_skills))

def extract_entities(raw_text: str) -> Dict[str, Any]:
    doc = nlp(raw_text)
    return {
        "name": extract_name(doc),
        "email": extract_email(raw_text),
        "skills": [{"name": skill} for skill in extract_skills(raw_text)],
    }