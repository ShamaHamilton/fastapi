from typing import Dict, List, Optional

from fastapi import APIRouter, Body, Path, Query
from pydantic import BaseModel

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)


class Image(BaseModel):
    url: str
    alias: str


class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: List[str] = []
    metadata: Dict[str, str] = {'key1': 'val1'}
    image: Optional[Image] = None


@router.post('/new/{id}')
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        'id': id,
        'data': blog,
        'version': version,
    }


@router.post('/new/{id}/comment/{comment_id}')
def create_comment(
    blog: BlogModel,
    id: int,
    comment_title: int = Query(
        None,
        title='Title of the comment',
        description='Some description for comment title',
        alias='commentTitle',
        deprecated=True
    ),
    # content: str = Body('hi how are you'),  # deafult value
    content: str = Body(
        ...,  # required
        min_length=10,
        max_length=50,
        # regex='^[a-z ]*$'
        pattern='^[a-z ]*$'
    ),
    v: Optional[List[str]] = Query(['v1.0', 'v1.1', 'v1.2']),
    comment_id: int = Path(gt=5, le=10)
):
    return {
        'data': blog,
        'id': id,
        'comment_title': comment_title,
        'content': content,
        'version': v,
        'comment_id': comment_id,
    }


def required_functionality():
    return {'message': 'Learning FastAPI is important'}
