from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, UniqueConstraint, Index, DateTime
from ..db import Base

class MapovaniNazvuNaPoslance(Base):
    __tablename__ = "mapovani_nazvu_na_poslance"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cele_jmeno_normalizovane: Mapped[str] = mapped_column(String(300))
    obdobi: Mapped[int]
    id_poslanec: Mapped[int]
    zdroj: Mapped[str] = mapped_column(String(50), default="manual")

    __table_args__ = (
        UniqueConstraint("cele_jmeno_normalizovane", "obdobi", name="uq_jmeno_obdobi"),
        Index("ix_mapovani_idposl", "id_poslanec"),
    )

class ImportAudit(Base):
    __tablename__ = "import_audit"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    soubor: Mapped[str] = mapped_column(String(255))
    hash: Mapped[str] = mapped_column(String(64))
    verze: Mapped[str] = mapped_column(String(50))
    zaznamenano: Mapped[str] = mapped_column(String(50))
    radku_ok: Mapped[int] = mapped_column(Integer, default=0)
    radku_fail: Mapped[int] = mapped_column(Integer, default=0)
