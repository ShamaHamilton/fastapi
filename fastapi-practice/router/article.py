from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_article
from db.database import get_db
from schemas import ArticleBaseSchema, ArticleDisplaySchema, UserBaseSchema
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/article',
    tags=['article']
)


@router.post('')
def create_article(
    request: ArticleBaseSchema,
    db: Session = Depends(get_db),
    current_user: UserBaseSchema = Depends(get_current_user)
) -> ArticleDisplaySchema:
    return db_article.create_article(db, request)


@router.get('/{id}')
def get_article(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserBaseSchema = Depends(get_current_user)
):  # -> ArticleDisplaySchema:
    return {
        'data': db_article.get_article(db, id),
        'current_user': current_user
    }
