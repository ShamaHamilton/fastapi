from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class DbUserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship('DbPostModel', back_populates='user')


class DbPostModel(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    image_url_type = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('DbUserModel', back_populates='items')
    comments = relationship('DbCommentModel', back_populates='post')


class DbCommentModel(Base):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('DbPostModel', back_populates='comments')
