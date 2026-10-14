from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db, engine
from models import Base, Item, Location, Size, Type
from schemas import ItemCreate, ItemRead, LocationCreate, LocationRead, TypeCreate, TypeRead, SizeCreate, SizeRead

Base.metadata.create_all(bind=engine)
app = FastAPI()

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

@app.post("/sizes", response_model=SizeRead, status_code=201)
def create_size(data: SizeCreate, db: Session = Depends(get_db)):
    size = Size(**data.model_dump())
    db.add(size)
    db.commit()
    db.refresh(size)

    return size

@app.post("/types", response_model=TypeRead, status_code=201)
def create_type(data: TypeCreate, db: Session = Depends(get_db)):
    type = Type(**data.model_dump())
    db.add(type)
    db.commit()
    db.refresh(type)

    return type
