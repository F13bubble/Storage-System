from datetime import datetime

from pydantic import Field

from app.schemas.Common import Schema


class LocationBase(Schema):
    code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    parent_id: int | None = None
    is_active: bool = True


class LocationCreate(LocationBase):
    pass


class LocationUpdate(Schema):
    # Partial update: apply with model_dump(exclude_unset=True)
    code: str | None = Field(default=None, min_length=1, max_length=64)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    parent_id: int | None = None
    is_active: bool | None = None


class LocationRead(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: int | None
    updated_by: int | None
