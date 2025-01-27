from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class UserBaseSchema(BaseModel):
    username: str
    email: str
    password: str


class UserDisplaySchema(BaseModel):
    # model_config = ConfigDict(from_attributes=True)

    username: str
    email: str


class PostBaseSchema(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creator_id: int


# for PostDisplaySchema
class UserSchema(BaseModel):
    username: str


# for PostDisplaySchema
class CommentSchema(BaseModel):
    text: str
    username: str
    timestamp: datetime


class PostDisplaySchema(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    user: UserSchema
    comments: List[CommentSchema]


class UserAuthSchema(BaseModel):
    id: int
    username: str
    email: str


class CommentBaseSchema(BaseModel):
    username: str
    text: str
    post_id: int
