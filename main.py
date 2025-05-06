from http.client import HTTPException

from fastapi import FastAPI, Depends
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from operations import *
from models import *
from db_connection import get_session, init_db
from sqlmodel import Session
from typing import List, Optional
import operations as crud

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.post("/tasks/", response_model=TaskBase)  ###Crear Task###
async def create_task_endpoint(task: TaskBase, session: AsyncSession = Depends(get_session)):
    return await create_task_sql(session, task)

@app.get("/tasks/", response_model=list[TaskBase]) ###Listar Tasks###
async def list_tasks_endpoint(session: AsyncSession = Depends(get_session)):
    return await list_tasks(session)
@app.post("/users/", response_model=UserBase) ###Crear User###
async def create_user_endpoint(user: UserBase, session: AsyncSession = Depends(get_session)):
    return await create_user_sql(session, user)

@app.get("/users/", response_model=list[UserBase]) ###Listar User###
async def list_users_endpoint(session: AsyncSession = Depends(get_session)):
    return await list_users(session)

@app.patch("/users/{user_id}", response_model=UserSQL, tags=["Update User"])
async def update_user_endpoint(user_id:int, user_update:UserSQL, session:AsyncSession = Depends(get_session)):
    updated_user = await crud.update_user(session, user_id, user_update.dict(exclude_unset=True))
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
@app.patch("/tasks/{task_id}", response_model=TaskBase, tags=["Update Task"])
async def update_task_endpoint(task_id: int, task_update: TaskUpdated, session: AsyncSession = Depends(get_session)):
    updated_task = await crud.update_task(session, task_id, task_update.dict(exclude_unset=True))
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task
