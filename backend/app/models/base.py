from sqlalchemy.orm import declarative_mixin, declared_attr
from sqlalchemy import func, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column

@declarative_mixin
class TimestampMixin:
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True),
                                                server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

@declarative_mixin
class PKMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
