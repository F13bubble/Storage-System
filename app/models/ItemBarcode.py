import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Symbology(enum.Enum):
    EAN13 = "EAN13"
    EAN8 = "EAN8"
    UPCA = "UPCA"
    CODE128 = "CODE128"
    QR = "QR"
    DATAMATRIX = "DATAMATRIX"


class BarcodeSource(enum.Enum):
    MANUFACTURER = "MANUFACTURER"
    INTERNAL = "INTERNAL"


class ItemBarcode(Base):
    __tablename__ = "item_barcodes"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    symbology: Mapped[Symbology] = mapped_column(Enum(Symbology), nullable=False)
    source: Mapped[BarcodeSource] = mapped_column(Enum(BarcodeSource), nullable=False)
    pack_quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    is_primary: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    item: Mapped["Item"] = relationship(back_populates="barcodes")
