from nlp.relation.extractor import extract_relationships

def test_extract_relationships_mock(monkeypatch):
    def mock_llm(prompt):
        return [
            ["Rahul", "DEPLOYED", "Lambda service"]
        ]

    # Replace real LLM call
    monkeypatch.setattr(
        "nlp.relation.extractor.call_llm",
        mock_llm
    )

    text = "Rahul deployed Lambda service"
    entities = ["Rahul", "Lambda service"]

    relationships = extract_relationships(text, entities)

    assert relationships[0][1] == "DEPLOYED"