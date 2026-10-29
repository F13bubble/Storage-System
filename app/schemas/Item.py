from datetime import datetime
from decimal import Decimal

from pydantic import Field

from app.schemas.Common import Schema
from app.schemas.ItemBarcode import ItemBarcodeCreate, ItemBarcodeRead


class ItemBase(Schema):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    category_id: int | None = None
    manufacturer: str | None = Field(default=None, max_length=255)
    unit: str = Field(default="pcs", min_length=1, max_length=20)
    purchase_price: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    reorder_limit: int = Field(default=0, ge=0)
    is_active: bool = True


class ItemCreate(ItemBase):
    barcodes: list[ItemBarcodeCreate] = []


class ItemUpdate(Schema):
    # Partial update: apply with model_dump(exclude_unset=True)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    category_id: int | None = None
    manufacturer: str | None = Field(default=None, max_length=255)
    unit: str | None = Field(default=None, min_length=1, max_length=20)
    purchase_price: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    reorder_limit: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ItemRead(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: int | None
    updated_by: int | None
    barcodes: list[ItemBarcodeRead] = []
