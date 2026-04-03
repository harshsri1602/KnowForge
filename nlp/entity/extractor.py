import re
from rapidfuzz import fuzz
from nlp.entity.spacy_model import nlp

TECH = {
    "aws", "azure", "gcp", "lambda", "ec2", "s3",
    "docker", "kubernetes", "terraform", "ansible",
    "kafka", "rabbitmq",
    "redis", "postgres", "mongodb", "mysql", "dynamodb",
    "airflow", "spark", "hadoop",
    "django", "flask", "fastapi", "express", "spring",
    "react", "nextjs", "vue", "angular",
    "graphql", "rest", "grpc",
    "git", "github", "gitlab",
    "oauth", "iam", "jwt"
}

def is_tech_fuzzy(text):
    for tech in TECH:
        if fuzz.partial_ratio(text.lower(), tech) > 85:
            return True
    return False


def classify_entity(text: str):
    t = text.lower()

    if any(k == t or k in t for k in TECH):
        return "TECH"

    if is_tech_fuzzy(t):
        return "TECH"

    if "api" in t:
        return "API"

    if any(k in t for k in ["service", "system", "pipeline"]):
        return "SERVICE"

    if re.match(r"^[A-Z][a-z]+$", text):
        return "PERSON"

    return "UNKNOWN"


def extract_entities(text: str):
    entities = []
    doc = nlp(text)

    for ent in doc.ents:
        label = classify_entity(ent.text)

        entities.append({
            "text": ent.text.strip(),
            "label": label
        })

    patterns = [
        (r"\bService\s[A-Z]\b", "SERVICE"),
        (r"\bAPI\s?[A-Z]\b", "API"),
        (r"\b[A-Z][a-zA-Z]+\sservice\b", "SERVICE"),
    ]

    for pattern, label in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            entities.append({
                "text": match.strip(),
                "label": label
            })

    unique = {}
    for e in entities:
        key = e["text"]
        if key not in unique or unique[key]["label"] == "UNKNOWN":
            unique[key] = e

    return list(unique.values())