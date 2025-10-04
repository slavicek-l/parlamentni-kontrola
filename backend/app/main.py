from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.v1.router import api_router
from .logging_conf import setup_logging
from .middlewares import ETagMiddleware

setup_logging()
app = FastAPI(title="ParlamentníKontrola API", version="1.0.0")

app.include_router(api_router)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

app.add_middleware(ETagMiddleware)

@app.get("/health/live")
def live():
    return {"status":"ok"}

@app.get("/")
def root():
    return {"service":"ParlamentníKontrola", "env": settings.ENV}
