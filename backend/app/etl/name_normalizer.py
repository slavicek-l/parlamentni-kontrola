import re
from slugify import slugify

def normalize_name(full_name: str) -> str:
    s = re.sub(r"\s+", " ", full_name.strip())
    return slugify(s, lowercase=True, separator=" ")
