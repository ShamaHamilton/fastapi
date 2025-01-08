from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_user
from db import db_user
from db.database import get_db
from schemas import UserBaseSchema, UserDisplaySchema

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('')
def create_user(request: UserBaseSchema, db: Session = Depends(get_db)) -> UserDisplaySchema:
    return db_user.create_user(db, request)


@router.get('')
def get_all_users(
    db: Session = Depends(get_db),
    current_user: UserBaseSchema = Depends(get_current_user)
) -> List[UserDisplaySchema]:
    return db_user.get_all_users(db)


@router.get('/{id}')
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserBaseSchema = Depends(get_current_user)
) -> UserDisplaySchema:
    return db_user.get_user(db, id)


@router.post('/{id}/update')
def update_user(
    id: int,
    request: UserBaseSchema,
    db: Session = Depends(get_db),
    current_user: UserBaseSchema = Depends(get_current_user)
):
    return db_user.update_user(db, id, request)


@router.get('/{id}/delete')
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserBaseSchema = Depends(get_current_user)
):
    return db_user.delete_user(db, id)
