from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, time
from sqlalchemy import String, Integer, Date, Time, Enum, ForeignKey, Index, DateTime, Numeric
from ..db import Base
import enum

class Hlasovani(Base):
    __tablename__ = "hlasovani"
    id_hlasovani: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    schuze: Mapped[int]
    cislo: Mapped[int]
    bod: Mapped[int | None]
    datum: Mapped[date] = mapped_column(Date, nullable=False)
    cas: Mapped[time | None] = mapped_column(Time, nullable=True)
    nazev_kratky: Mapped[str | None] = mapped_column(String(255))
    nazev_dlouhy: Mapped[str | None] = mapped_column(String(2000))
    pro: Mapped[int | None]
    proti: Mapped[int | None]
    zdrzel: Mapped[int | None]
    nehlasoval: Mapped[int | None]
    vysledek: Mapped[str | None] = mapped_column(String(10))
    id_organ: Mapped[int | None]

    tematika = relationship("HlasovaniTematika", back_populates="hlasovani")

Index("ix_hlasovani_datum", Hlasovani.datum)

class HlasVysledekEnum(str, enum.Enum):
    A="A"; N="N"; C="C"; F="F"; NP="NP"; OML="OML"

class HlasovaniPoslancu(Base):
    __tablename__ = "hlasovani_poslancu"
    id_poslanec: Mapped[int] = mapped_column(ForeignKey("poslanci.id_poslanec"), primary_key=True)
    id_hlasovani: Mapped[int] = mapped_column(ForeignKey("hlasovani.id_hlasovani"), primary_key=True)
    vysledek: Mapped[HlasVysledekEnum]

    poslanec = relationship("Poslanec", back_populates="hlasovani")
    hlasovani = relationship("Hlasovani")
