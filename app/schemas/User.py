from datetime import datetime

from pydantic import EmailStr, Field

from app.schemas.Common import Schema


class UserBase(Schema):
    firstname: str = Field(min_length=1, max_length=100)
    lastname: str = Field(min_length=1, max_length=100)
    email: EmailStr
    role_id: int
    is_active: bool = True


class UserCreate(UserBase):
    # Plain password; the service hashes it into User.password_hash
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(Schema):
    # Partial update: apply with model_dump(exclude_unset=True)
    firstname: str | None = Field(default=None, min_length=1, max_length=100)
    lastname: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    role_id: int | None = None
    is_active: bool | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)


# Never exposes password_hash
class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None
