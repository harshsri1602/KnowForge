import re
from nlp.entity.spacy_model import nlp


def label_entity(text: str) -> str:
    """
    Assign meaningful labels to entities
    """
    text_lower = text.lower()

    # 👤 Person names (simple heuristic)
    if text.istitle() and len(text.split()) == 1:
        return "PERSON"

    # ⚙️ Services
    if "service" in text_lower:
        return "SERVICE"

    # 🔗 APIs
    if "api" in text_lower:
        return "API"

    # 🧱 Systems
    if "system" in text_lower:
        return "SYSTEM"

    return "UNKNOWN"


def extract_entities(text: str):
    """
    Extract entities using:
    1. spaCy (baseline NLP)
    2. Rule-based heuristics (domain-specific)
    3. Custom labeling (PERSON, SERVICE, API, etc.)
    """

    entities = []

    # 🔹 1. spaCy extraction
    doc = nlp(text)
    for ent in doc.ents:
        entities.append({
            "text": ent.text.strip(),
            "label": label_entity(ent.text.strip())
        })

    # 🔹 2. Rule-based extraction

    patterns = [
        r"\b[A-Z][a-z]+\b",                 # Rahul, Ankit
        r"\b[A-Z][a-zA-Z]+\sservice\b",     # Lambda service
        r"\bAPI\s?[A-Z]\b",                 # API X
        r"\bService\s[A-Z]\b"               # Service A
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            cleaned = match.strip()
            entities.append({
                "text": cleaned,
                "label": label_entity(cleaned)
            })

    # 🔹 3. Fallback: Capitalized words
    words = text.split()
    for word in words:
        if word.istitle() and len(word) > 2:
            cleaned = word.strip()
            entities.append({
                "text": cleaned,
                "label": label_entity(cleaned)
            })

    # 🔹 4. Deduplicate (prefer better labels)
    unique = {}

    for e in entities:
        key = e["text"].lower()

        if key in unique:
            # prefer more specific label over UNKNOWN
            if unique[key]["label"] == "UNKNOWN" and e["label"] != "UNKNOWN":
                unique[key] = e
        else:
            unique[key] = e

    return list(unique.values())