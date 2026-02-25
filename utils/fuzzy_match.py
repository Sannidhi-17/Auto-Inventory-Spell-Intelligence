from rapidfuzz import process, fuzz
import pandas as pd
from utils.preprocessing import normalize_text

def load_master_parts():
    df = pd.read_csv("master_parts.csv")
    return df["part_name"].astype(str).tolist()

def fuzzy_match(input_text):
    parts = load_master_parts()

    normalized_input = normalize_text(input_text)

    # create normalize mapping
    normalized_parts = {
        normalize_text(part): part for part in parts
    }

    result = process.extractOne(normalized_input, 
                    list(normalized_parts.keys()), 
                    scorer=fuzz.token_sort_ratio
                    )

    if result:
        normalize_match, score, _ = result
        original_match = normalized_parts[normalize_match]
        return original_match, score
    return None, 0