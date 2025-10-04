import chardet

def detect_decode(content: bytes) -> str:
    guess = chardet.detect(content)
    encoding = guess.get("encoding") or "cp1250"
    return content.decode(encoding, errors="replace")

def parse_unl(text: str):
    # pipe-delimited, trimming, NULL handling
    for line in text.splitlines():
        parts = [p.strip() for p in line.split("|")]
        parts = [None if p=="" or p=="\N" else p for p in parts]
        yield parts
