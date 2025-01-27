import shutil
import string
from typing import List
import random

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm.session import Session

from auth.oauth2 import get_current_user
from db.database import get_db
from db import db_post
from routers.schemas import PostBaseSchema, PostDisplaySchema, UserAuthSchema

from logger import logger


router = APIRouter(
    prefix='/post',
    tags=['post']
)

image_url_types = ['absolute', 'relative']


@router.post('')
def create(
    request: PostBaseSchema,
    db: Session = Depends(get_db),
    current_user: UserAuthSchema = Depends(get_current_user)
) -> PostDisplaySchema:
    if not request.image_url_type in image_url_types:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Parameter image_url_type can only take values 'absolute' or 'relative'."
        )
    return db_post.create(db, request)


@router.get('/all')
def posts(db: Session = Depends(get_db)) -> List[PostDisplaySchema]:
    return db_post.get_all(db)


@router.post('/image')
def upload_image(
    image: UploadFile = File(...),
    current_user: UserAuthSchema = Depends(get_current_user)
):
    letters = string.ascii_letters
    logger.debug('letters: %s', letters)
    rand_str = ''.join(random.choice(letters) for i in range(6))
    logger.debug('rand_str: %s', rand_str)
    new = f'_{rand_str}.'
    logger.debug('new: %s', new)
    logger.debug('image.filename: %s', image.filename)
    filename = new.join(image.filename.rsplit('.', 1))
    logger.debug('filename: %s', filename)
    path = f'images/{filename}'
    logger.debug('path: %s', path)

    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}


@router.delete('/delete/{id}')
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserAuthSchema = Depends(get_current_user)
):
    return db_post.delete(db, id, current_user.id)
