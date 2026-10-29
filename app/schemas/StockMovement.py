from datetime import datetime
from decimal import Decimal

from pydantic import Field, model_validator

from app.models.StockMovement import MovementType
from app.schemas.Common import Schema


class StockMovementBase(Schema):
    item_id: int
    from_location_id: int | None = None
    to_location_id: int | None = None
    quantity: Decimal = Field(gt=0, max_digits=12, decimal_places=3)
    type: MovementType
    reason: str | None = Field(default=None, max_length=255)


class StockMovementCreate(StockMovementBase):
    @model_validator(mode="after")
    def validate_locations(self):
        has_from = self.from_location_id is not None
        has_to = self.to_location_id is not None

        match self.type:
            case MovementType.IN if has_from or not has_to:
                raise ValueError("IN requires to_location_id only")
            case MovementType.OUT if not has_from or has_to:
                raise ValueError("OUT requires from_location_id only")
            case MovementType.TRANSFER if not (has_from and has_to):
                raise ValueError("TRANSFER requires from_location_id and to_location_id")
            case MovementType.TRANSFER if self.from_location_id == self.to_location_id:
                raise ValueError("TRANSFER locations must differ")
            # ADJUSTMENT: from_location = remove stock, to_location = add stock
            case MovementType.ADJUSTMENT if has_from == has_to:
                raise ValueError("ADJUSTMENT requires exactly one of from_location_id or to_location_id")
            case MovementType.ADJUSTMENT if not self.reason:
                raise ValueError("ADJUSTMENT requires a reason")
        return self


# No StockMovementUpdate: movements are an append-only log; fix mistakes with a new movement
class StockMovementRead(StockMovementBase):
    id: int
    created_by: int | None
    created_at: datetime
