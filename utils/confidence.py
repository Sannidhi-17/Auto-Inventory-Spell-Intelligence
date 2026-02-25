def decide_tier(fuzzy_score):
    if fuzzy_score >= 85:
        return "ACCEPT"
    elif 20 <= fuzzy_score <85:
        return "GENAI"
    else:
        return "MANUAL"