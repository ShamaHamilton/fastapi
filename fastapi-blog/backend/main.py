import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.base import BaseHTTPMiddleware


from database import models
from database.database import engine
from routers import post

from logger import logger
# from middleware import log_middleware

app = FastAPI()
# app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
logger.info('Starting API...')

app.include_router(post.router)

models.Base.metadata.create_all(engine)

app.mount('/images', StaticFiles(directory='images'), name='images')

origins = [
    'http://127.0.0.1:3000',
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


# @app.get('/')
# async def index() -> dict:
#     # logger.info('Request to index page')
#     await asyncio.sleep(1.5)
#     return {'message': 'Hello'}


# @app.get('/upload-videos')
# async def upload_videos() -> dict:
#     # logger.info('Request to video-upload page')
#     return {'message': 'Video Uploaded'}
