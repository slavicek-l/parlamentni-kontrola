# Rychlý start ParlamentníKontrola.cz

## Předpoklady
- Docker a Docker Compose
- Make (GNU Make)

## Spuštění (3 kroky)

1. **Stáhnout a rozbalit**:
```bash
unzip parlamentni-kontrola.zip
cd parlamentni-kontrola/
```

2. **Setup a build**:
```bash
make setup
```

3. **Spustit aplikaci**:
```bash
make up
```

Po spuštění:
- Aplikace běží na: http://localhost:8080
- API dokumentace: http://localhost:8080/docs
- Health check: http://localhost:8080/health

## Funkcionalita

✅ **Dashboard** s Top navrhovatelé chart
✅ **Profil poslance** s kartou Návrhy (donut chart, timeline)
✅ **API endpointy** pro poslance, hlasování, tisky, statistiky
✅ **ETL pipeline** pro import dat PSP ČR (idempotentní)
✅ **PostgreSQL** s migracemi a demo daty
✅ **Redis** pro cache a Celery
✅ **Celery** worker a beat scheduler
✅ **Nginx** reverse proxy
✅ **Testy** (pytest, cypress)
✅ **CI** (GitHub Actions)

## Užitečné příkazy

```bash
make test      # Spustí testy
make migrate   # Spustí migrace
make seed      # Nahraje demo data
make down      # Zastaví stack
```

## Akceptační kritéria - SPLNĚNO ✅

- [x] Jediný krok `make up` spustí celý systém
- [x] Backend publikuje API s OpenAPI dokumentací
- [x] Frontend zobrazuje dashboard s Top navrhovatelé chart
- [x] Profil poslance obsahuje kartu "Návrhy" s vizualizacemi
- [x] ETL zvládá idempotentní import a mapování navrhovatelů
- [x] Testy běží v CI a pokrývají klíčové části
- [x] Žádné manuální úpravy nejsou potřeba pro dev režim
