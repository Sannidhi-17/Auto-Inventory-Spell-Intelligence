import re

def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # Lowercase
    text = text.lower()

    # Remove special characters (keep letters, numbers, spaces)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text