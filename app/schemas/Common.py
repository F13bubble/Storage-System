from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    # from_attributes: allows Schema.model_validate(orm_object)
    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True)
