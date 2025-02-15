from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from database.models import DbPostModel
from routers.schemas import PostBaseSchema


def create(db: Session, request: PostBaseSchema):
    new_post = DbPostModel(
        image_url=request.image_url,
        title=request.title,
        content=request.content,
        creator=request.creator,
        timestamp=datetime.now(timezone.utc)
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all(db: Session):
    return db.query(DbPostModel).all()


def delete(id: int, db: Session):
    post = db.query(DbPostModel).filter(DbPostModel.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found')

    db.delete(post)
    db.commit()
    return 'ok'
