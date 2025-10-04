from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = "0001_init_schema"
down_revision = None
branch_labels = None
depends_on = None
def upgrade():
    bind = op.get_bind()

# 1) Vytvoř ENUM typy explicitně a idempotentně pomocí DO $$ … $$ (bez ohledu na SQLAlchemy interní create)
op.execute("""
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'hlasvysledek') THEN
        CREATE TYPE hlasvysledek AS ENUM ('A','N','C','F','NP','OML');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'roleenum') THEN
        CREATE TYPE roleenum AS ENUM ('navrhovatel','spolu-navrhovatel','zástupce');
    END IF;
END
$$;
""")

# 2) Tabulky — u ENUM sloupců odkazuj pouze na existující typ jménem přes sa.Enum(name=..., create_type=False)
op.create_table(
    "poslanci",
    sa.Column("id_poslanec", sa.Integer(), primary_key=True),
    sa.Column("jmeno", sa.String(100), nullable=False),
    sa.Column("prijmeni", sa.String(100), nullable=False),
    sa.Column("datum_narozeni", sa.Date(), nullable=True),
    sa.Column("strana", sa.String(120), nullable=True),
    sa.Column("kraj", sa.String(120), nullable=True),
    sa.Column("kontakty", sa.String(500), nullable=True),
    sa.Column("foto_url", sa.String(500), nullable=True),
    sa.Column("aktivni_od", sa.Date(), nullable=True),
    sa.Column("aktivni_do", sa.Date(), nullable=True),
    sa.Column("aktivni", sa.Boolean(), server_default=sa.text("true"), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
)

op.create_table(
    "hlasovani",
    sa.Column("id_hlasovani", sa.Integer(), primary_key=True),
    sa.Column("schuze", sa.Integer(), nullable=False),
    sa.Column("cislo", sa.Integer(), nullable=False),
    sa.Column("bod", sa.Integer(), nullable=True),
    sa.Column("datum", sa.Date(), nullable=False),
    sa.Column("cas", sa.Time(), nullable=True),
    sa.Column("nazev_kratky", sa.String(255), nullable=True),
    sa.Column("nazev_dlouhy", sa.String(2000), nullable=True),
    sa.Column("pro", sa.Integer(), nullable=True),
    sa.Column("proti", sa.Integer(), nullable=True),
    sa.Column("zdrzel", sa.Integer(), nullable=True),
    sa.Column("nehlasoval", sa.Integer(), nullable=True),
    sa.Column("vysledek", sa.String(10), nullable=True),
    sa.Column("id_organ", sa.Integer(), nullable=True),
)
op.create_index("ix_hlasovani_datum", "hlasovani", ["datum"])

op.create_table(
    "tisky",
    sa.Column("id_tisk", sa.Integer(), primary_key=True),
    sa.Column("druh", sa.String(120), nullable=True),
    sa.Column("datum_rozsahu_od", sa.Date(), nullable=True),
    sa.Column("datum_rozsahu_do", sa.Date(), nullable=True),
    sa.Column("nazev", sa.String(1000), nullable=True),
    sa.Column("stav_legislativni_faze", sa.String(255), nullable=True),
    sa.Column("cislo_tisku", sa.String(50), nullable=True),
    sa.Column("obdobi", sa.Integer(), nullable=True),
)
op.create_index("ix_tisky_datum_od", "tisky", ["datum_rozsahu_od"])
op.create_index("ix_tisky_obdobi", "tisky", ["obdobi"])

op.create_table(
    "hlasovani_poslancu",
    sa.Column("id_poslanec", sa.Integer(), sa.ForeignKey("poslanci.id_poslanec"), primary_key=True),
    sa.Column("id_hlasovani", sa.Integer(), sa.ForeignKey("hlasovani.id_hlasovani"), primary_key=True),
    sa.Column("vysledek", postgresql.ENUM(name="hlasvysledek", create_type=False), nullable=False),
)

op.create_table(
    "tisky_poslanci",
    sa.Column("id_tisk", sa.Integer(), sa.ForeignKey("tisky.id_tisk"), primary_key=True),
    sa.Column("id_poslanec", sa.Integer(), sa.ForeignKey("poslanci.id_poslanec"), primary_key=True),
    sa.Column("role", postgresql.ENUM(name="roleenum", create_type=False), primary_key=True),
)
op.create_index("ix_tp_idposlanec", "tisky_poslanci", ["id_poslanec"])

op.create_table(
    "tematika",
    sa.Column("id_tema", sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column("nazev", sa.String(200), nullable=False),
    sa.Column("popis", sa.String(1000), nullable=True),
    sa.Column("barva", sa.String(10), nullable=True),
)

op.create_table(
    "hlasovani_tematika",
    sa.Column("id_hlasovani", sa.Integer(), sa.ForeignKey("hlasovani.id_hlasovani"), primary_key=True),
    sa.Column("id_tema", sa.Integer(), sa.ForeignKey("tematika.id_tema"), primary_key=True),
    sa.Column("relevance", sa.Numeric(3, 2), nullable=False),
)

op.create_table(
    "tisky_tematika",
    sa.Column("id_tisk", sa.Integer(), sa.ForeignKey("tisky.id_tisk"), primary_key=True),
    sa.Column("id_tema", sa.Integer(), sa.ForeignKey("tematika.id_tema"), primary_key=True),
    sa.Column("relevance", sa.Numeric(3, 2), nullable=False),
)

op.create_table(
    "mapovani_nazvu_na_poslance",
    sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column("cele_jmeno_normalizovane", sa.String(300), nullable=False),
    sa.Column("obdobi", sa.Integer(), nullable=False),
    sa.Column("id_poslanec", sa.Integer(), nullable=False),
    sa.Column("zdroj", sa.String(50), nullable=False, server_default="manual"),
    sa.UniqueConstraint("cele_jmeno_normalizovane", "obdobi", name="uq_jmeno_obdobi"),
)
op.create_index("ix_mapovani_idposl", "mapovani_nazvu_na_poslance", ["id_poslanec"])

op.create_table(
    "import_audit",
    sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
    sa.Column("soubor", sa.String(255), nullable=False),
    sa.Column("hash", sa.String(64), nullable=False),
    sa.Column("verze", sa.String(50), nullable=False),
    sa.Column("zaznamenano", sa.String(50), nullable=False),
    sa.Column("radku_ok", sa.Integer(), nullable=False, server_default="0"),
    sa.Column("radku_fail", sa.Integer(), nullable=False, server_default="0"),
)
def downgrade():
    op.drop_table("import_audit")
    op.drop_index("ix_mapovani_idposl", table_name="mapovani_nazvu_na_poslance")
    op.drop_table("mapovani_nazvu_na_poslance")
    op.drop_table("tisky_tematika")
    op.drop_table("hlasovani_tematika")
    op.drop_table("tematika")
    op.drop_index("ix_tp_idposlanec", table_name="tisky_poslanci")
    op.drop_table("tisky_poslanci")
    op.drop_table("hlasovani_poslancu")
    op.drop_index("ix_tisky_obdobi", table_name="tisky")
    op.drop_index("ix_tisky_datum_od", table_name="tisky")
    op.drop_table("tisky")
    op.drop_index("ix_hlasovani_datum", table_name="hlasovani")
    op.drop_table("hlasovani")
    op.drop_table("poslanci")

    # Smazání ENUM typů explicitně
    op.execute("DROP TYPE IF EXISTS hlasvysledek;")
    op.execute("DROP TYPE IF EXISTS roleenum;")