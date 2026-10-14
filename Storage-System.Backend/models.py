from sqlalchemy import ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(80))
    type_id: Mapped[int] = mapped_column(ForeignKey("type.id"))             # what type
    amount: Mapped[int] = mapped_column(Integer)                            # how many
    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))     # what location its in
    size_id: Mapped[int] = mapped_column(ForeignKey("sizes.id"))            # under what size it falls
    code: Mapped[str] = mapped_column(String(20))                           # generated code, that identifies that product and holds important info
    log_needed: Mapped[bool] = mapped_column(Boolean(False))                # if taking that item needs to be logged

    type: Mapped["Type"] = relationship(back_populates="items")
    location: Mapped["Location"] = relationship(back_populates="items")
    size: Mapped["Size"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, name={self.name!r}, descripion={self.description!r}, type_id={self.type_id!r}, amount={self.amount!r}, location_id={self.location_id!r}, size_id={self.size_id!r}, code={self.code!r}, lod_needed={self.log_needed!r})"


class Type(Base):
    __tablename__ = "type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(80))

    items: Mapped[list["Item"]] = relationship(back_populates="type")

    def __repr__(self) -> str:
        return f"Type(id={self.id!r}, name={self.name!r}, description={self.description!r})"


class Location(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    space: Mapped[str] = mapped_column(String(50))                                              # how often the max size fits
    max_size: Mapped[str] = mapped_column(String(30))                                           # the biggest size it can hold
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("location.id"), nullable=True)     # for smth like compartments inside a box

    items: Mapped[list["Item"]] = relationship(back_populates="location")

    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, name={self.name!r}, space={self.space!r}, max_size={self.max_size!r}, parent_id={self.parent_id!r})"


class Size(Base):
    __tablename__ = "sizes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(80))
    measures: Mapped[str] = mapped_column(String(20))

    items: Mapped[list["Item"]] = relationship(back_populates="size")

    def __repr__(self) -> str:
        return f"Size(id={self.id!r}, name={self.name!r}, description={self-self.description!r}, measures={self.measures!r})"