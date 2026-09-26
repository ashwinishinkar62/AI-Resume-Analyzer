def extract_education(text):
    text = text.lower()

    education_keywords = [
        "b.e",
        "be",
        "b.tech",
        "btech",
        "m.e",
        "m.tech",
        "mtech",
        "bca",
        "mca",
        "b.sc",
        "bsc",
        "diploma",
        "engineering"
    ]
    found = []

    for keyword in education_keywords:
        if keyword in text:
            found.append(keyword.upper())
    if not found:
        return["Not Found"]
    return list(set(found))