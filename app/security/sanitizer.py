import re

FORBIDDEN_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"disregard\s+above",
    r"override\s+system",
    r"you\s+are\s+chatgpt",
    r"system\s+prompt",
    r"follow\s+these\s+instructions\s+instead"
]

def sanitize_text(text: str) -> str:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    clean_sentences = []

    for sentence in sentences:
        lower = sentence.lower()
        if any(re.search(pattern, lower) for pattern in FORBIDDEN_PATTERNS):
            continue  # remove malicious sentence only
        clean_sentences.append(sentence)

    return " ".join(clean_sentences).strip()