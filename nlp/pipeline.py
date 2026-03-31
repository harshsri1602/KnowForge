from nlp.entity.extractor import extract_entities
from nlp.relation.extractor import extract_relationships
from nlp.entity.cleaner import clean_entities

def run_nlp_pipeline(text: str):
    entities = extract_entities(text)
    cleaned_entities = clean_entities(entities)
    relationships = extract_relationships(text, cleaned_entities)

    return {
        "entities": cleaned_entities,
        "relationships": relationships
    }