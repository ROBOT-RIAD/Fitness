import json
import openai


def translate_to_english(data):
    """Translate only values of JSON fields to English using OpenAI, keeping keys unchanged."""
    prompt = f"""
    Translate the following JSON data from Spanish to English, but DO NOT translate the keys — only the values.


    Keep the field names (keys) exactly the same. Return only the translated values in English using the same JSON structure.


    JSON to translate:
    {json.dumps(data, indent=2)}


    Return raw JSON with translated values and same keys.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        raise Exception(f"Translation to English failed: {str(e)}")
   



def translate_to_spanish(data):
    """Translate only values of JSON fields to Spanish using OpenAI, keeping keys unchanged."""
    prompt = f"""
    Translate the following JSON data from English to Spanish, but DO NOT translate the keys — only the values.


    Keep the field names (keys) exactly the same. Return only the translated values in Spanish using the same JSON structure.


    JSON to translate:
    {json.dumps(data, indent=2)}


    Return raw JSON with translated values and same keys.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        raise Exception(f"Translation to Spanish failed: {str(e)}")
