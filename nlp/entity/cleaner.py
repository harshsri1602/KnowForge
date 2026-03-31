def clean_entities(entities):
    """
    Clean and normalize entities:
    - remove duplicates
    - remove generic words
    - merge similar entities
    """

    cleaned = {}

    for e in entities:
        text = e["text"]

        if text.lower() in ["service", "system"]:
            continue

        normalized = text.lower().strip()

        # prefer longer version (Lambda service > Lambda)
        if normalized in cleaned:
            if len(text) > len(cleaned[normalized]["text"]):
                cleaned[normalized] = e
        else:
            cleaned[normalized] = e

    return list(cleaned.values())