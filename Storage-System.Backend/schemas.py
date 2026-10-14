from pydantic import BaseModel, ConfigDict

class ItemCreate(BaseModel):
    name: str
    description: str
    type_id: int
    amount: int
    location_id: int
    size_id: int
    code: str
    log_needed: bool


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    type_id: int
    amount: int
    location_id: int
    size_id: int
    code: str
    log_needed: bool


class LocationCreate(BaseModel):
    name: str
    space: str
    max_size: str
    parent_id: int

class LocationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    space: str
    max_size: str
    parent_id: int


class TypeCreate(BaseModel):
    name: str
    description: str

class TypeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str


class SizeCreate(BaseModel):
    name: str
    description: str
    measures: str

class SizeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    measures: str