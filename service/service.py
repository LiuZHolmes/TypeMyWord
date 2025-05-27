import unicodedata

def normalize_input(input: str) -> str:
    return unicodedata.normalize('NFKC', input)

