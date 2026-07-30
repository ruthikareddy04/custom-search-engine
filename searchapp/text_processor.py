import re
from collections import Counter


def process_text(text):

    text = text.lower()

    # Keep words with numbers like w3schools
    words = re.findall(r'\b[a-z0-9]+\b', text)

    stop_words = {
        "the",
        "is",
        "and",
        "a",
        "of",
        "to",
        "in",
        "for",
        "on",
        "with",
        "this",
        "that"
    }

    words = [
        word for word in words
        if word not in stop_words
    ]

    return Counter(words)