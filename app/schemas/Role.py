from datetime import datetime

from pydantic import Field

from app.schemas.Common import Schema


class RoleBase(Schema):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    can_manage_users: bool = False
    can_edit_items: bool = False
    can_move_stock: bool = False
    can_adjust_stock: bool = False


class RoleCreate(RoleBase):
    pass


class RoleUpdate(Schema):
    # Partial update: apply with model_dump(exclude_unset=True)
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    can_manage_users: bool | None = None
    can_edit_items: bool | None = None
    can_move_stock: bool | None = None
    can_adjust_stock: bool | None = None


class RoleRead(RoleBase):
    id: int
    created_by: int | None
    created_at: datetime
    updated_by: int | None
    updated_at: datetime
