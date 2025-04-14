import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


def clean_cv_text(text: str, remove_stopwords: bool = False) -> str:
    # 1. Normalize whitespace and remove repeated newlines
    text = re.sub(r"\s+", " ", text)  # collapse all whitespace
    text = re.sub(r"\n+", "\n", text)  # remove extra newlines
    text = re.sub(r"(?i)(page|pg)[\s:]*\d+", "", text)  # remove "Page 1", "pg 2" etc.

    # 2. Remove non-printable characters
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # 3. Lowercase (optional based on your prompt design)
    text = text.lower()

    # 4. Tokenization (optional, for advanced cleaning)
    if remove_stopwords:
        words = word_tokenize(text)
        filtered_words = [
            word for word in words if word.lower() not in stopwords.words("english")
        ]
        text = " ".join(filtered_words)

    return text.strip()
