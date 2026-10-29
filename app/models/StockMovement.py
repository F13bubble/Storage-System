import enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class MovementType(enum.Enum):
    IN = "IN"  # to_location only
    OUT = "OUT"  # from_location only
    TRANSFER = "TRANSFER"  # from_location -> to_location
    ADJUSTMENT = "ADJUSTMENT"  # inventory correction


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    from_location_id: Mapped[int | None] = mapped_column(ForeignKey("locations.id"))
    to_location_id: Mapped[int | None] = mapped_column(ForeignKey("locations.id"))
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    type: Mapped[MovementType] = mapped_column(Enum(MovementType), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255))
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    item: Mapped["Item"] = relationship()
    from_location: Mapped["Location | None"] = relationship(foreign_keys=[from_location_id])
    to_location: Mapped["Location | None"] = relationship(foreign_keys=[to_location_id])
