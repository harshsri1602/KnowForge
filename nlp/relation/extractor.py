from nlp.relation.llm_client import call_llm
from nlp.relation.prompt import build_prompt

def extract_relationships(text, entities):
    prompt = build_prompt(text, entities)

    response = call_llm(prompt)

    return response