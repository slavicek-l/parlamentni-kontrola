# ParlamentníKontrola.cz

Monorepozitář pro transparentní vizualizaci hlasování poslanců, účasti a nově i počtu předložených návrhů (sněmovních tisků).

Hlavní vlastnosti:
- Backend: FastAPI, SQLAlchemy, Alembic, Celery, Redis
- ETL: ZIP download, UNL parser (Windows-1250 -> UTF-8), idempotentní import, upserty, audit
- DB: PostgreSQL 15+, indexy, materializované pohledy
- Frontend: React 18 + TS + Vite + MUI + Chart.js
- Infrastruktura: Docker Compose (db, redis, backend, worker, scheduler, nginx, frontend)
- CI: GitHub Actions (lint, testy, build)

## Rychlý start

1) make setup
2) make up
3) Otevři http://localhost:8080

Při startu:
- proběhne alembic upgrade head
- nahraje se demo dataset
- frontend i backend běží za reverse proxy
- API dokumentace: /docs

## Make cíle

- make setup — připraví .env a buildne kontejnery
- make up — spustí stack a inicializuje DB + demo data
- make migrate — spustí migrace
- make seed — nahraje demo dataset
- make test — spustí testy (pytest + cypress)
- make down — shodí stack včetně volume

## ENV proměnné (výběr)

- ENV: dev|prod
- CORS_ORIGINS: povolené originy
- API_AUTH_MODE: none|apikey|jwt
- API_KEYS: CSV klíčů pro apikey
- JWT_SECRET, JWT_ALG, JWT_ACCESS_TTL
- PSP_DATA_BASE: base URL pro otevřená data
- ETL_*: cesty a UA

## Bezpečnost

- Rate limit, CORS, sanitizace vstupů (ORM parametry, stránkování), ETag a cache headers
- Bezpečné hlavičky doporučeno přidat při prod nasazení (CSP, HSTS) v Nginx

## Observabilita

- /health/live
- Prometheus metriky v ETL (hooky připravené)
