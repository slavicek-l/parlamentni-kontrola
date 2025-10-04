import os, requests, zipfile, io, hashlib
from ..config import settings

def download_zip(relative_path: str) -> bytes:
    url = f"{settings.PSP_DATA_BASE}/{relative_path}"
    headers = {"User-Agent": settings.ETL_USER_AGENT}
    r = requests.get(url, headers=headers, timeout=60)
    r.raise_for_status()
    return r.content

def extract_zip(content: bytes, out_dir: str):
    with zipfile.ZipFile(io.BytesIO(content)) as z:
        z.extractall(out_dir)

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()
