from typing import Optional
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from db.database import get_db
from db import db_user


oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

# choco install openssl (for windows)
# openssl rand -hex 32
SECRET_KEY = '7dfc723d2eb1dede296cfb1d9549447ffe4db3d781587d15b871dac0d2be3780'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('username')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db_user.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user
