import openai
import json
import re
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


def extract_json(text):
    """
    Extract and return the first valid JSON object from a string.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)
    return {}


def translate_to_spanish(data):
    """
    Translates values in a JSON object from English to Spanish using GPT-4o.
    """
    system_prompt = (
        "You are a translator. Translate only the **values** of this JSON object from English to Spanish. "
        "Keep the original keys and structure exactly as-is. "
        "Return ONLY valid JSON. No explanations, comments, or formatting like markdown."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(data)}
            ],
            temperature=0.3
        )

        raw_response = response.choices[0].message.content.strip()
        return extract_json(raw_response)

    except Exception as e:
        print(f"Translation error: {e}")
        return data
