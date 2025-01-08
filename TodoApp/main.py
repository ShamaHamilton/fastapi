from fastapi import FastAPI

from .models import Base
from .database import engine
from .routers.auth import router as router_auth
from .routers.todos import router as router_todos


app = FastAPI()
app.include_router(router_auth)
app.include_router(router_todos)

Base.metadata.create_all(bind=engine)
