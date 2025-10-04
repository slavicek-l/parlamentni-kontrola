from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Date
from datetime import date
from ..db import Base
from .base import TimestampMixin

class Poslanec(Base, TimestampMixin):
    __tablename__ = "poslanci"
    id_poslanec: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    jmeno: Mapped[str] = mapped_column(String(100))
    prijmeni: Mapped[str] = mapped_column(String(100))
    datum_narozeni: Mapped[date | None] = mapped_column(Date, nullable=True)
    strana: Mapped[str | None] = mapped_column(String(120))
    kraj: Mapped[str | None] = mapped_column(String(120))
    kontakty: Mapped[str | None] = mapped_column(String(500))
    foto_url: Mapped[str | None] = mapped_column(String(500))
    aktivni_od: Mapped[date | None] = mapped_column(Date, nullable=True)
    aktivni_do: Mapped[date | None] = mapped_column(Date, nullable=True)
    aktivni: Mapped[bool] = mapped_column(default=True)

    hlasovani = relationship("HlasovaniPoslancu", back_populates="poslanec")
    tisky = relationship("TiskyPoslanci", back_populates="poslanec")
