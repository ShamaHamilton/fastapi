import logging
import time

from fastapi import Depends, FastAPI, HTTPException, Request, Response, WebSocket, status
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from db import models
from db.database import engine
from exceptions import StoryException
from client import html

from router.blog_get import router as router_blog_get
from router.blog_post import router as router_blog_post
from router.user import router as router_user
from router.article import router as router_article
from router.product import router as router_product
from auth.authentication import router as router_auth
from router.file import router as router_file
from templates.template import router as router_templates
from router.dependencies import router as router_dependencies

app = FastAPI(
    # dependencies=[Depends(any_dependency)]  # app Dependency
)
app.include_router(router_dependencies)
app.include_router(router_templates)
app.include_router(router_auth)
app.include_router(router_file)
app.include_router(router_user)
app.include_router(router_article)
app.include_router(router_product)
app.include_router(router_blog_get)
app.include_router(router_blog_post)


logger = logging.getLogger('uvicorn.error')
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)


# @app.get('/')
# def home_page():
#     logger.debug('this is a debug message')
#     return {'message': 'ok'}


@app.get('/')
async def get():
    return HTMLResponse(html)

clients = []


@app.websocket('/chat')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


@app.get('/hello')
def index():
    return {'message': 'Hello world!'}


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={'detail': exc.name}
    )


# @app.exception_handler(HTTPException)
# def custom_exception(request: Request, exc: StoryException):
#     return PlainTextResponse(
#         str(exc),
#         status_code=status.HTTP_404_NOT_FOUND
#     )


models.Base.metadata.create_all(engine)


@app.middleware('http')
async def add_middleware(request: Request, call_next):
    """Измерение времени мужду запросом и ответом."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response


origins = [
    'http://localhost:3000/',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/files', StaticFiles(directory='files'), name='files')
app.mount('/templates/static', StaticFiles(directory='templates/static'), name='static')
