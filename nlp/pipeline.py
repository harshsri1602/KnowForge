from nlp.entity.extractor import extract_entities
from nlp.relation.extractor import extract_relationships

def run_nlp_pipeline(text: str):
    entities = extract_entities(text)
    relationships = extract_relationships(text, entities)

    return {
        "entities": entities,
        "relationships": relationships
    }