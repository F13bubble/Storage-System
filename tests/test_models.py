from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

import app.models  # noqa: F401
from app.core.database import Base
from app.models import BarcodeSource, Item, ItemBarcode, Symbology


def test_item_with_barcode_roundtrip():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        item = Item(name="Screw M4x20")
        item.barcodes.append(
            ItemBarcode(code="4006381333931", symbology=Symbology.EAN13, source=BarcodeSource.MANUFACTURER)
        )
        session.add(item)
        session.commit()

        found = session.scalars(select(ItemBarcode).where(ItemBarcode.code == "4006381333931")).one()
        assert found.item.name == "Screw M4x20"
