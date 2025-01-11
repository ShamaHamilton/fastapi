from typing import List
from pydantic import BaseModel, ConfigDict


class ArticleSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
    published: bool


class UserBaseSchema(BaseModel):
    username: str
    email: str
    password: str


class UserDisplaySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str
    items: List[ArticleSchema] = []


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str


class ArticleBaseSchema(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int


class ArticleDisplaySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
    published: bool
    user: UserSchema
