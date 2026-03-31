from nlp.pipeline import run_nlp_pipeline

def test_full_pipeline(monkeypatch):
    def mock_llm(prompt):
        return [
            ["Rahul", "DEPLOYED", "Lambda service"],
            ["Lambda service", "DEPENDS_ON", "API X"]
        ]

    monkeypatch.setattr(
        "nlp.relation.extractor.call_llm",
        mock_llm
    )

    text = "Rahul deployed Lambda service for API X"

    result = run_nlp_pipeline(text)

    assert "entities" in result
    assert "relationships" in result

    assert len(result["relationships"]) == 2