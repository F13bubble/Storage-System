from pydantic import Field

from app.schemas.Common import Schema

HEX_COLOR = r"^#[0-9a-fA-F]{6}$"


class CategoryBase(Schema):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    color: str | None = Field(default=None, pattern=HEX_COLOR)
    parent_id: int | None = None
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(Schema):
    # Partial update: apply with model_dump(exclude_unset=True)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    color: str | None = Field(default=None, pattern=HEX_COLOR)
    parent_id: int | None = None
    is_active: bool | None = None


class CategoryRead(CategoryBase):
    id: int
