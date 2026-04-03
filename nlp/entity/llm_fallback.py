from nlp.relation.llm_client import call_llm


def refine_with_llm(text, entities):
    should_call_llm = False

    if not entities:
        should_call_llm = True

    elif len(entities) <= 1:
        should_call_llm = True

    elif any(e["label"] == "UNKNOWN" for e in entities):
        should_call_llm = True

    if not should_call_llm:
        return entities

    prompt = f"""
Extract entities and classify into:
PERSON, SERVICE, API, TECH

Rules:
- Technologies → TECH
- Humans → PERSON
- APIs → API
- Systems/services → SERVICE

Text:
{text}

Return STRICT JSON:
{{"entities": [{{"text": "...", "label": "..."}}]}}
"""

    try:
        llm_result = call_llm(prompt)
        llm_entities = llm_result.get("entities", [])

        if not entities:
            return llm_entities

        entity_map = {e["text"]: e for e in entities}

        for le in llm_entities:
            if le["text"] not in entity_map:
                entity_map[le["text"]] = le
            elif entity_map[le["text"]]["label"] == "UNKNOWN":
                entity_map[le["text"]] = le

        return list(entity_map.values())

    except Exception as e:
        print("LLM fallback failed:", e)
        return entities