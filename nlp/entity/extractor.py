import re
from nlp.entity.spacy_model import nlp

def extract_entities(text: str):
    """
    Extract entities using:
    1. spaCy (baseline NLP)
    2. Rule-based heuristics (to fix domain gaps)

    Returns:
        List[Dict] -> [{"text": ..., "label": ...}]
    """

    entities = []

    # 🔹 1. spaCy extraction
    doc = nlp(text)
    for ent in doc.ents:
        entities.append({
            "text": ent.text.strip(),
            "label": ent.label_
        })

    # 🔹 2. Rule-based extraction (IMPORTANT)

    # Match patterns like:
    # - Rahul, Ankit (names)
    # - Lambda service
    # - API X
    patterns = [
        r"\b[A-Z][a-z]+\b",                 # Rahul, Ankit
        r"\b[A-Z][a-zA-Z]+\sservice\b",     # Lambda service
        r"\bAPI\s?[A-Z]\b",                 # API X
        r"\bService\s[A-Z]\b"               # Service A
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            entities.append({
                "text": match.strip(),
                "label": "CUSTOM"
            })

    # 🔹 3. Fallback: Capitalized words (last resort)
    words = text.split()
    for word in words:
        if word.istitle() and len(word) > 2:
            entities.append({
                "text": word.strip(),
                "label": "CUSTOM"
            })

    # 🔹 4. Deduplicate entities
    unique = {}
    for e in entities:
        key = e["text"]
        unique[key] = e

    return list(unique.values())