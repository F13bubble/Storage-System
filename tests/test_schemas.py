from decimal import Decimal

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import app.models  # noqa: F401
from app.core.database import Base
from app.models import BarcodeSource, Item, ItemBarcode, MovementType, Symbology
from app.schemas import (
    CategoryCreate,
    ItemBarcodeCreate,
    ItemCreate,
    ItemRead,
    ItemUpdate,
    StockMovementCreate,
    UserCreate,
)


def barcode(code: str, symbology: Symbology = Symbology.EAN13) -> ItemBarcodeCreate:
    return ItemBarcodeCreate(code=code, symbology=symbology, source=BarcodeSource.MANUFACTURER)


@pytest.mark.parametrize(
    ("code", "symbology"),
    [("4006381333931", Symbology.EAN13), ("96385074", Symbology.EAN8), ("036000291452", Symbology.UPCA)],
)
def test_valid_gtin(code, symbology):
    assert barcode(code, symbology).code == code


@pytest.mark.parametrize(
    "code",
    ["4006381333932", "400638133393", "40063813339A1"],  # wrong check digit, too short, not digits
)
def test_invalid_ean13(code):
    with pytest.raises(ValidationError):
        barcode(code)


def test_code128_accepts_any_text_and_strips_whitespace():
    b = barcode("  ITM-000123 ", Symbology.CODE128)
    assert b.code == "ITM-000123"


def test_item_create_rejects_negative_price():
    with pytest.raises(ValidationError):
        ItemCreate(name="Screw", purchase_price=Decimal("-1"))


def test_item_update_only_contains_sent_fields():
    update = ItemUpdate(reorder_limit=5)
    assert update.model_dump(exclude_unset=True) == {"reorder_limit": 5}


@pytest.mark.parametrize(
    ("type_", "from_id", "to_id", "reason", "ok"),
    [
        (MovementType.IN, None, 1, None, True),
        (MovementType.IN, 1, None, None, False),
        (MovementType.OUT, 1, None, None, True),
        (MovementType.TRANSFER, 1, 2, None, True),
        (MovementType.TRANSFER, 1, 1, None, False),
        (MovementType.TRANSFER, 1, None, None, False),
        (MovementType.ADJUSTMENT, 1, None, "Inventory count", True),
        (MovementType.ADJUSTMENT, 1, None, None, False),
        (MovementType.ADJUSTMENT, 1, 2, "x", False),
    ],
)
def test_stock_movement_location_rules(type_, from_id, to_id, reason, ok):
    data = dict(item_id=1, from_location_id=from_id, to_location_id=to_id, quantity=Decimal("2"), type=type_, reason=reason)
    if ok:
        StockMovementCreate(**data)
    else:
        with pytest.raises(ValidationError):
            StockMovementCreate(**data)


def test_stock_movement_quantity_must_be_positive():
    with pytest.raises(ValidationError):
        StockMovementCreate(item_id=1, to_location_id=1, quantity=Decimal("0"), type=MovementType.IN)


def test_category_color_must_be_hex():
    assert CategoryCreate(name="Tools", color="#ff8800").color == "#ff8800"
    with pytest.raises(ValidationError):
        CategoryCreate(name="Tools", color="orange")


def test_user_create_validates_email_and_password():
    with pytest.raises(ValidationError):
        UserCreate(firstname="A", lastname="B", email="not-an-email", role_id=1, password="longenough")
    with pytest.raises(ValidationError):
        UserCreate(firstname="A", lastname="B", email="a@example.com", role_id=1, password="short")


def test_item_read_from_orm():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        item = Item(name="Screw M4x20")
        item.barcodes.append(
            ItemBarcode(code="4006381333931", symbology=Symbology.EAN13, source=BarcodeSource.MANUFACTURER)
        )
        session.add(item)
        session.commit()

        read = ItemRead.model_validate(item)
        assert read.id == item.id
        assert read.barcodes[0].code == "4006381333931"
