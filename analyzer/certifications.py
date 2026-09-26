def extract_certifications(text):
    text = text.lower()

    certificate_keywords = [
        "google",
        "ibm",
        "coursera",
        "udemy",
        "forage",
        "oracle",
        "nptel",
        "aws",
        "microsoft"
    ]
    found = []

    for keyword in certificate_keywords:
        if keyword in text:
            found.append(keyword.title())

    if not found:
        return["Not Found"]
    return list(set(found))