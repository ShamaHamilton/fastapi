from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from db.database import get_db
from db import db_user
from routers.schemas import UserBaseSchema, UserDisplaySchema


router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('')
def create_user(request: UserBaseSchema, db: Session = Depends(get_db)) -> UserDisplaySchema:
    return db_user.create_user(db, request)
