import json
import re


def strip_markdown_fences(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def parse_llm_json_array(content: str) -> list:
    cleaned = strip_markdown_fences(content)
    data = json.loads(cleaned)
    if not isinstance(data, list):
        raise ValueError("LLM response is not a JSON array")
    return data
