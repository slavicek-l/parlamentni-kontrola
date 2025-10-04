from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, StreamingResponse
import hashlib
import anyio

class ETagMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Pro streamované odpovědi ETag nepočítat (nebo je materializovat opatrně)
        if isinstance(response, StreamingResponse):
            return response

        # Získat kompletní body bezpečně
        body = b""
        if hasattr(response, "body"):
            # Starlette Response má .body (bytes) po vytvoření
            body = response.body or b""
        else:
            # Fallback: přečíst iterator asynchronně
            collected = bytearray()
            async for chunk in response.body_iterator:
                collected.extend(chunk)
            body = bytes(collected)

        # Spočítat slabý ETag ze SHA256 + délky
        etag = 'W/"%d-%s"' % (len(body), hashlib.sha256(body).hexdigest()[:8])
        response.headers["ETag"] = etag

        # Vrátit novou Response s již materializovaným tělem a původními hlavičkami/kódem/MIME
        return Response(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
            background=response.background,
        )
