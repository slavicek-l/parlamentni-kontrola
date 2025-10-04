from sqlalchemy import text
from sqlalchemy.orm import Session

MVIEW_DEFS = {
    "mv_navrhy_summary": """
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_navrhy_summary AS
        SELECT tp.id_poslanec,
               DATE_TRUNC('month', COALESCE(t.datum_rozsahu_od, CURRENT_DATE)) AS bucket,
               SUM(CASE WHEN tp.role='navrhovatel' THEN 1 ELSE 0 END) AS navrhovatel_count,
               SUM(CASE WHEN tp.role='spolu-navrhovatel' THEN 1 ELSE 0 END) AS spolu_count,
               COUNT(*) as total
        FROM tisky_poslanci tp
        JOIN tisky t ON t.id_tisk = tp.id_tisk
        GROUP BY tp.id_poslanec, DATE_TRUNC('month', COALESCE(t.datum_rozsahu_od, CURRENT_DATE));
    """,
    "mv_ucast": """
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_ucast AS
        SELECT hp.id_poslanec,
               DATE_TRUNC('month', h.datum) AS bucket,
               SUM(CASE WHEN hp.vysledek='NP' THEN 1 ELSE 0 END) AS nepritomen,
               SUM(CASE WHEN hp.vysledek IN ('A','N','C','F','OML') THEN 1 ELSE 0 END) AS pritomen,
               COUNT(*) AS total
        FROM hlasovani_poslancu hp
        JOIN hlasovani h ON h.id_hlasovani = hp.id_hlasovani
        GROUP BY hp.id_poslanec, DATE_TRUNC('month', h.datum);
    """
}

def create_materialized_views(session: Session):
    for name, ddl in MVIEW_DEFS.items():
        session.execute(text(ddl))
    session.commit()

def refresh_materialized_views(session: Session):
    for name in MVIEW_DEFS.keys():
        session.execute(text(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {name};"))
    session.commit()
