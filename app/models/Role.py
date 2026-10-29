from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    can_manage_users: Mapped[bool] = mapped_column(nullable=False, default=False)
    can_edit_items: Mapped[bool] = mapped_column(nullable=False, default=False)
    can_move_stock: Mapped[bool] = mapped_column(nullable=False, default=False)
    can_adjust_stock: Mapped[bool] = mapped_column(nullable=False, default=False)
    # use_alter: users.role_id -> roles and roles.created_by -> users form a cycle
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", use_alter=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", use_alter=True))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
