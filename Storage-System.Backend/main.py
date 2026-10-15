from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import get_db, engine
from models import Base, Item, Location, Size, Type
from schemas import ItemCreate, ItemRead, LocationCreate, LocationRead, TypeCreate, TypeRead, SizeCreate, SizeRead

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Helper Functions
def count_items(db: Session, item_column, entity_id: int) -> int:
    return db.scalar(
        select(func.count())
        .select_from(Item)
        .where(item_column == entity_id)
    ) or 0

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/items", response_model=ItemRead, status_code=201)
def create_item(data: ItemCreate, db: Session = Depends(get_db)):
    if db.get(Location, data.location_id) is None:
        raise HTTPException(status_code=404, detail="Location not found")
    if db.get(Size, data.size_id) is None:
        raise HTTPException(status_code=404, detail="Size not found")
    if db.get(Type, data.type_id) is None:
        raise HTTPException(status_code=404, detail="Type not found")

    item = Item(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)

    return item

@app.put("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, data: ItemCreate, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    if db.get(Location, data.location_id) is None:
        raise HTTPException(status_code=404, detail="Location not found")
    if db.get(Size, data.size_id) is None:
        raise HTTPException(status_code=404, detail="Size not found")
    if db.get(Type, data.type_id) is None:
        raise HTTPException(status_code=404, detail="Type not found")

    for field, value in data.model_dump().items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)

    return item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()


@app.post("/locations", response_model=LocationRead, status_code=201)
def create_location(data: LocationCreate, db: Session = Depends(get_db)):
    location = Location(**data.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)

    return location

@app.put("/locations/{location_id}", response_model=LocationRead)
def update_location(location_id: int, data: LocationCreate, response: Response, db: Session = Depends(get_db)):
    location = db.get(Location, location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    values = data.model_dump()
    changed = any(getattr(location, field) != value for field, value in values.items())
    affected = count_items(db, Item.location_id, location_id) if changed else 0

    for field, value in values.items():
        setattr(location, field, value)

    db.commit()
    db.refresh(location)
    response.headers["X-Items-Affected"] = str(affected)
    return location


@app.delete("/locations/{location_id}", status_code=204)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    location = db.get(Location, location_id)
    if location is None:
        raise HTTPException(status_code=404, detail="Location not found")

    item_count = count_items(db, Item.location_id, location_id)
    child_count = db.scalar(
        select(func.count())
        .select_from(Location)
        .where(Location.parent_id == location_id)
    ) or 0

    if item_count or child_count:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Location cannot be deleted while it is in use",
                "items_using_location": item_count,
                "child_locations": child_count,
            },
        )


    db.delete(location)
    db.commit()


@app.post("/sizes", response_model=SizeRead, status_code=201)
def create_size(data: SizeCreate, db: Session = Depends(get_db)):
    size = Size(**data.model_dump())
    db.add(size)
    db.commit()
    db.refresh(size)

    return size

@app.put("/sizes/{size_id}", response_model=SizeRead)
def update_size(size_id: int, data: SizeCreate, response: Response, db: Session = Depends(get_db)):
    size = db.get(Size, size_id)
    if size is None:
        raise HTTPException(status_code=404, detail="Size not found")

    values = data.model_dump()
    changed = any(getattr(size, field) != value for field, value in values.items())
    affected = count_items(db, Item.size_id, size_id) if changed else 0

    for field, value in values.items():
        setattr(size, field, value)

    db.commit()
    db.refresh(size)
    response.headers["X-Items-Affected"] = str(affected)
    return size

@app.delete("/sizes/{size_id}", status_code=204)
def delete_size(size_id: int, db: Session = Depends(get_db)):
    size = db.get(Size, size_id)
    if size is None:
        raise HTTPException(status_code=404, detail="Size not found")

    item_count = count_items(db, Item.size_id, size_id)
    if item_count:
        raise HTTPException(
            status_code=409,
            detail={
                "message": "Size cannot be deleted while items use it",
                "items_using_size": item_count,
            },
        )

    db.delete(size)
    db.commit()


@app.post("/types", response_model=TypeRead, status_code=201)
def create_type(data: TypeCreate, db: Session = Depends(get_db)):
    type_obj = Type(**data.model_dump())
    db.add(type_obj)
    db.commit()
    db.refresh(type_obj)

    return type_obj

@app.put("/types/{type_id}", response_model=TypeRead)
def update_type(type_id: int, data: TypeCreate, response: Response, db: Session = Depends(get_db)):
    type_obj = db.get(Type, type_id)
    if type_obj is None:
        raise HTTPException(status_code=404, detail="Type not found")

    values = data.model_dump()
    changed = any(getattr(type_obj, field) != value for field, value in values.items())
    affected = count_items(db, Item.type_id, type_id) if changed else 0

    for field, value in values.items():
        setattr(type_obj, field, value)

    db.commit()
    db.refresh(type_obj)
    response.headers["X-Items-Affected"] = str(affected)
    return type_obj

@app.delete("/types/{type_id}", status_code=204)
def delete_type(type_id: int, db: Session = Depends(get_db)):
    type_obj = db.get(Type, type_id)
    if type_obj is None:
        raise HTTPException(status_code=404, detail="Type not found")

    item_count = count_items(db, Item.type_id, type_id)
    if item_count:
        raise HTTPException(
            status_code=409,
            detail={
            "message": "Type cannot be deleted while items use it",
            "items_using_type": item_count,
            },
        )

    db.delete(type_obj)
    db.commit()