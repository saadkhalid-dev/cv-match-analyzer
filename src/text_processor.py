import re


def normalize_text(text: str) -> str:
    """
    Normalize text so CV and job-description content can be compared
    consistently.

    The function:
    - converts text to lowercase
    - replaces line breaks with spaces
    - removes unnecessary punctuation
    - collapses repeated whitespace
    """

    text = text.lower()
    text = text.replace("\n", " ")

    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()