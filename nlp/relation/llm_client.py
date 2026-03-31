import os
import json
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def call_llm(prompt: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "temperature": 0
        }
    )

    text = response.text.strip()

    # Try parsing JSON directly
    try:
        return json.loads(text)
    except:
        return extract_json_from_text(text)


def extract_json_from_text(text: str):
    """
    Extract JSON array from messy LLM output
    """
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass
    return []