from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy import String, Integer, Date, Enum, ForeignKey, Index, Numeric
from ..db import Base
import enum

class Tisk(Base):
    __tablename__ = "tisky"
    id_tisk: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    druh: Mapped[str | None] = mapped_column(String(120))
    datum_rozsahu_od: Mapped[date | None] = mapped_column(Date, nullable=True)
    datum_rozsahu_do: Mapped[date | None] = mapped_column(Date, nullable=True)
    nazev: Mapped[str | None] = mapped_column(String(1000))
    stav_legislativni_faze: Mapped[str | None] = mapped_column(String(255))
    cislo_tisku: Mapped[str | None] = mapped_column(String(50))
    obdobi: Mapped[int | None]

Index("ix_tisky_datum_od", Tisk.datum_rozsahu_od)
Index("ix_tisky_obdobi", Tisk.obdobi)

class RoleEnum(str, enum.Enum):
    navrhovatel="navrhovatel"
    spolu_navrhovatel="spolu-navrhovatel"
    zastupce="zástupce"

class TiskyPoslanci(Base):
    __tablename__ = "tisky_poslanci"
    id_tisk: Mapped[int] = mapped_column(ForeignKey("tisky.id_tisk"), primary_key=True)
    id_poslanec: Mapped[int] = mapped_column(ForeignKey("poslanci.id_poslanec"), primary_key=True)
    role: Mapped[RoleEnum] = mapped_column(primary_key=True)

    poslanec = relationship("Poslanec", back_populates="tisky")
    tisk = relationship("Tisk")
