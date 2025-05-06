from fastapi import FastAPI, Depends
from sqlalchemy.future import select
from sqlalchemy.testing.pickleable import User
from sqlmodel.ext.asyncio.session import AsyncSession
from operations import *
from models import TaskBase, UserBase
from db_connection import get_session, init_db

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.post("/tasks/", response_model=TaskBase)  ###Crear Task###
async def create_task_endpoint(task: TaskBase, session: AsyncSession = Depends(get_session)):
    return await create_task(session, task)

@app.get("/tasks/", response_model=list[TaskBase]) ###Listar Tasks###
async def list_tasks_endpoint(session: AsyncSession = Depends(get_session)):
    return await list_tasks(session)
@app.post("/users/", response_model=UserBase) ###Crear User###
async def create_user_endpoint(user: UserBase, session: AsyncSession = Depends(get_session)):
    return await create_user(session, user)

@app.get("/users/", response_model=list[UserBase]) ###Listar User###
async def list_users_endpoint(session: AsyncSession = Depends(get_session)):
    return await list_users(session)