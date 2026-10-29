from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))
    color: Mapped[str | None] = mapped_column(String(7))  # hex, e.g. "#ff8800"
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)

    parent: Mapped["Category | None"] = relationship(back_populates="children", remote_side=[id])
    children: Mapped[list["Category"]] = relationship(back_populates="parent")
