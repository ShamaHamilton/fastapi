import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from ..models import UsersModel
from ..database import SessionLocal


logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# openssl rand -hex 32
SECRET_KEY = '459cd31cfef92d473b6b2ece98d3ad31a1f0471fa30b39a48a1d20d48c11de0e'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')  # '/auth/token'


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class CreateUserRequestSchema(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


templates = Jinja2Templates(directory='templates')


### Pages ###
@router.get('/login-page')
def render_login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@router.get('/register-page')
def render_register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})


### Endpoints ###
def authenticate_user(username: str, password: str, db: Session):
    user = db.query(UsersModel).filter(UsersModel.username == username).first()
    if not user:
        return False
    logger.debug('User "%s" is find', user.username)
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    logger.debug('Password is successful')
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user.')


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequestSchema):
    create_user_model = UsersModel(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number
    )

    db.add(create_user_model)
    db.commit()


@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
) -> TokenSchema:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
