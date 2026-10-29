from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    manufacturer: Mapped[str | None] = mapped_column(String(255))
    unit: Mapped[str] = mapped_column(String(20), nullable=False, default="pcs")
    purchase_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    reorder_limit: Mapped[int] = mapped_column(nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    updated_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    category: Mapped["Category | None"] = relationship()
    barcodes: Mapped[list["ItemBarcode"]] = relationship(
        back_populates="item", cascade="all, delete-orphan"
    )
