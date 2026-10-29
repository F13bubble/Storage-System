from datetime import datetime
from decimal import Decimal

from app.schemas.Common import Schema


# Read-only: stock levels change only through StockMovements
class StockRead(Schema):
    item_id: int
    location_id: int
    quantity: Decimal
    updated_at: datetime
