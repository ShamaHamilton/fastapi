from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from db.models import DbUserModel
from db.hashing import Hash
from routers.schemas import UserBaseSchema


def create_user(db: Session, request: UserBaseSchema):
    new_user = DbUserModel(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUserModel).filter(DbUserModel.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with username {username} not found'
        )
    return user
