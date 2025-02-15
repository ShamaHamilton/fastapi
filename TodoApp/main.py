import logging

from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from .models import Base
from .database import engine
from .routers.auth import router as router_auth
from .routers.todos import router as router_todos
from .routers.admin import router as router_admin
from .routers.users import router as router_users


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


app = FastAPI()

Base.metadata.create_all(bind=engine)

# templates = Jinja2Templates(directory='templates')

app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/')
def test(request: Request):
    # return templates.TemplateResponse('home.html', {'request': request})
    return RedirectResponse(url='/todos/todo-page', status_code=status.HTTP_302_FOUND)


@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}


app.include_router(router_auth)
app.include_router(router_todos)
app.include_router(router_admin)
app.include_router(router_users)
