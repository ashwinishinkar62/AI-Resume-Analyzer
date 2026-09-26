import re

def extract_experience(text):
    pattern = r'(\d+)\s*(year|years|yr|yrs|month|months)'

    matches = re.findall(pattern, text.lower())

    if matches:
        return matches
    return "Fresher"