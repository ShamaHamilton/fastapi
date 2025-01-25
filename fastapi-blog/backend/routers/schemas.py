from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    image_url: str
    title: str
    content: str
    creator: str


class PostDisplaySchema(PostBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime

#    class Config:  # == model_config = ConfigDict(from_attributes=True)
#        orm_mode = True
