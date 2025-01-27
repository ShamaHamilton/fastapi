from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from db.models import DbPostModel
from routers.schemas import PostBaseSchema


def create(db: Session, request: PostBaseSchema):
    new_post = DbPostModel(
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption=request.caption,
        timestamp=datetime.now(timezone.utc),
        user_id=request.creator_id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


def get_all(db: Session):
    return db.query(DbPostModel).all()


def delete(db: Session, id: int, user_id: int):
    post = db.query(DbPostModel).filter(DbPostModel.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {id} not found'
        )
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only post creator can delete post'
        )

    db.delete(post)
    db.commit()
    return 'ok'
