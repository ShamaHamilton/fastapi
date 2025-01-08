from typing import List
from pydantic import BaseModel


class ArticleSchema(BaseModel):
    title: str
    content: str
    published: bool

    class Config():
        from_attributes = True


class UserBaseSchema(BaseModel):
    username: str
    email: str
    password: str


class UserDisplaySchema(BaseModel):
    username: str
    email: str
    items: List[ArticleSchema] = []

    class Config():
        # orm_mode = True -> from_attributes = True
        from_attributes = True


class UserSchema(BaseModel):
    id: int
    username: str

    class Config():
        from_attributes = True


class ArticleBaseSchema(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int


class ArticleDisplaySchema(BaseModel):
    title: str
    content: str
    published: bool
    user: UserSchema

    class Config():
        from_attributes = True
