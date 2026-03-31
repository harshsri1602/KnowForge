from nlp.entity.extractor import extract_entities

def test_extract_entities_basic():
    text = "Rahul deployed Lambda for API X"

    entities = extract_entities(text)

    entity_texts = [e["text"] for e in entities]

    assert "Rahul" in entity_texts
    assert "Lambda" in entity_texts or "Lambda service" in entity_texts