def build_prompt(text, entities):
    return f"""
You are an information extraction system.

Your task is to extract relationships between entities from the given text.

RULES:
- Only use the provided entities.
- Do NOT invent new entities.
- Output MUST be valid JSON.
- Each relationship must be in the format:
  ["source", "RELATION", "target"]

RELATION TYPES:
- OWNS
- WORKS_ON
- DEPENDS_ON
- CREATED
- DEPLOYED
- MAINTAINS

TEXT:
\"\"\"
{text}
\"\"\"

ENTITIES:
{entities}

OUTPUT FORMAT:
[
  ["entity1", "RELATION", "entity2"]
]

EXAMPLE:
TEXT:
"Rahul deployed Lambda service for API X"

ENTITIES:
["Rahul", "Lambda service", "API X"]

OUTPUT:
[
  ["Rahul", "DEPLOYED", "Lambda service"],
  ["Lambda service", "DEPENDS_ON", "API X"]
]

Now extract relationships for the given input.
"""