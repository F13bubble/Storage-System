from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Stock(Base):
    __tablename__ = "stock"

    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), primary_key=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"), primary_key=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    item: Mapped["Item"] = relationship()
    location: Mapped["Location"] = relationship()
