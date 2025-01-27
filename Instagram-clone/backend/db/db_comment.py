from datetime import datetime, timezone
from sqlalchemy.orm.session import Session

from db.models import DbCommentModel
from routers.schemas import CommentBaseSchema


def create(db: Session, request: CommentBaseSchema):
    new_comment = DbCommentModel(
        text=request.text,
        username=request.username,
        post_id=request.post_id,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_all(db: Session, post_id: int):
    return db.query(DbCommentModel).filter(DbCommentModel.post_id == post_id).all()
