from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from ..models import TodosModel
from ..database import db_dependency
from .auth import get_current_user


templates = Jinja2Templates(directory='templates')

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequestSchema(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response


### Pages ###

@router.get('/todo-page')
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        todos = db.query(TodosModel).filter(TodosModel.owner_id == user.get('id')).all()
        return templates.TemplateResponse(
            'todo.html',
            {'request': request, 'todos': todos, 'user': user}
        )
    except:
        return redirect_to_login()


### Endpoints ###
@router.get('/')
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed')
    return db.query(TodosModel).filter(TodosModel.owner_id == user.get('id')).all()


@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed')

    todo_model = db.query(TodosModel).filter(TodosModel.id == todo_id)\
        .filter(TodosModel.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')


@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, request: TodoRequestSchema):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed')
    todo_model = TodosModel(**request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()


@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    request: TodoRequestSchema,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed')

    todo_model = db.query(TodosModel).filter(TodosModel.id == todo_id)\
        .filter(TodosModel.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found.')

    todo_model.title = request.title
    todo_model.description = request.description
    todo_model.priority = request.priority
    todo_model.complete = request.complete

    db.add(todo_model)
    db.commit()


@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Authentication Failed')

    todo_model = db.query(TodosModel).filter(TodosModel.id == todo_id)\
        .filter(TodosModel.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found.')

    db.query(TodosModel).filter(TodosModel.id == todo_id)\
        .filter(TodosModel.owner_id == user.get('id')).delete()
    db.commit()
