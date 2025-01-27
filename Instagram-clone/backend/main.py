from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from db import models
from db.database import engine
from routers import user
from routers import post
from auth import authentication
from routers import comment

from logger import logger

app = FastAPI()
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(authentication.router)


logger.info('Started App...')


@app.get('/')
def root():
    logger.debug('Main page')
    return "Hello world!"


origins = [
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory='images'), name='images')
