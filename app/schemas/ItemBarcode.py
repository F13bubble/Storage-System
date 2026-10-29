from datetime import datetime

from pydantic import Field, model_validator

from app.models.ItemBarcode import BarcodeSource, Symbology
from app.schemas.Common import Schema

GTIN_LENGTHS = {Symbology.EAN13: 13, Symbology.EAN8: 8, Symbology.UPCA: 12}


def gtin_check_digit_ok(code: str) -> bool:
    """EAN-8, EAN-13 and UPC-A share one rule: weights 3,1,3,... from the right."""
    *body, check = (int(c) for c in code)
    total = sum(d * (3 if i % 2 == 0 else 1) for i, d in enumerate(reversed(body)))
    return (10 - total % 10) % 10 == check


class ItemBarcodeBase(Schema):
    code: str = Field(min_length=1, max_length=64)
    symbology: Symbology
    source: BarcodeSource
    pack_quantity: int = Field(default=1, ge=1)
    is_primary: bool = False

    @model_validator(mode="after")
    def validate_gtin(self):
        length = GTIN_LENGTHS.get(self.symbology)
        if length is None:
            return self
        if not self.code.isdigit() or len(self.code) != length:
            raise ValueError(f"{self.symbology.value} must be exactly {length} digits")
        if not gtin_check_digit_ok(self.code):
            raise ValueError(f"invalid {self.symbology.value} check digit")
        return self


class ItemBarcodeCreate(ItemBarcodeBase):
    # item_id comes from the URL (/items/{id}/barcodes) or the parent ItemCreate
    pass


class ItemBarcodeUpdate(Schema):
    pack_quantity: int | None = Field(default=None, ge=1)
    is_primary: bool | None = None


class ItemBarcodeRead(ItemBarcodeBase):
    id: int
    item_id: int
    created_at: datetime
    created_by: int | None
