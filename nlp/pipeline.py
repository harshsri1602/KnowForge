from nlp.entity.extractor import extract_entities
from nlp.entity.llm_fallback import refine_with_llm
from nlp.relation.extractor import extract_relationships
from nlp.entity.cleaner import ensure_entities_from_relationships
import time

def run_nlp_pipeline(record):
    text = record["content"]

    entities = extract_entities(text)
    time.sleep(10)
    entities = refine_with_llm(text, entities)

    time.sleep(10)
    relationships = extract_relationships(text, entities)

    relationships = clean_relationships(relationships)
    
    entities = ensure_entities_from_relationships(entities, relationships)

    return {
        "entities": entities,
        "relationships": relationships
    }


def clean_relationships(relationships):
    unique = set()
    cleaned = []

    for r in relationships:
        key = tuple(r)
        if key not in unique and r[0] != r[2]:  # avoid self loops
            unique.add(key)
            cleaned.append(r)

    return cleaned