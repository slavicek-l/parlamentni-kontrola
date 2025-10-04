from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, Numeric
from ..db import Base

class Tematika(Base):
    __tablename__ = "tematika"
    id_tema: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nazev: Mapped[str] = mapped_column(String(200))
    popis: Mapped[str | None] = mapped_column(String(1000))
    barva: Mapped[str | None] = mapped_column(String(10))

class HlasovaniTematika(Base):
    __tablename__ = "hlasovani_tematika"
    id_hlasovani: Mapped[int] = mapped_column(ForeignKey("hlasovani.id_hlasovani"), primary_key=True)
    id_tema: Mapped[int] = mapped_column(ForeignKey("tematika.id_tema"), primary_key=True)
    relevance: Mapped[float] = mapped_column(Numeric(3,2))

class TiskyTematika(Base):
    __tablename__ = "tisky_tematika"
    id_tisk: Mapped[int] = mapped_column(ForeignKey("tisky.id_tisk"), primary_key=True)
    id_tema: Mapped[int] = mapped_column(ForeignKey("tematika.id_tema"), primary_key=True)
    relevance: Mapped[float] = mapped_column(Numeric(3,2))
