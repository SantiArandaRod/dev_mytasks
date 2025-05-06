from http.client import HTTPException

import uvicorn
from fastapi import FastAPI, Depends, Path, Query
from fastapi.openapi.utils import status_code_ranges
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from operations import *
from models import *
from db_connection import get_session, init_db
from sqlmodel import Session
from typing import List, Optional
import operations as crud
import os

app = FastAPI()
port = int(os.environ.get("PORT", 10000))
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.post("/tasks/", response_model=TaskSQL, tags=["Create Task"])  ###Crear Task###
async def create_task_endpoint(task: TaskBase, session: AsyncSession = Depends(get_session)):
    return await create_task_sql(session, task)

@app.get("/tasks/", response_model=list[TaskSQL], tags=["List task"]) ###Listar Tasks###
async def list_tasks_endpoint(session: AsyncSession = Depends(get_session)):
    return await list_tasks(session)
@app.get("/tasks/{task_id}", response_model=TaskSQL, tags=["List task"]) ###Listar taskId###
async def list_tasks_by_Id_endpoint(task_id: int, session: AsyncSession = Depends(get_session)):
    return await get_task(session, task_id)
@app.post("/users/", response_model=UserSQL, tags=["Create User"]) ###Crear User###
async def create_user_endpoint(user: UserBase, session: AsyncSession = Depends(get_session)):
    return await create_user_sql(session, user)

@app.get("/users/", response_model=list[UserSQL], tags=["List User"]) ###Listar User###
async def list_users_endpoint(session: AsyncSession = Depends(get_session)):
    return await list_users(session)
@app.get("/users/inactivo", response_model=list[UserSQL], tags=["Get Inactive Users"]) ###Listar Inactives Users###
async def list_inactive_users_endpoint(session: AsyncSession = Depends(get_session)):
    return await crud.list_inactive_users(session)
@app.get("/users/inactivo&premium", response_model=list[UserSQL], tags=["Get Inactive & Premium Users"]) ###Listar Inactives & Premium Users###
async def list_inactive_And_Premium_users_endpoint(session: AsyncSession = Depends(get_session)):
    return await crud.list_InactiveAndPremium(session)

@app.get("/users/{user_id}", response_model=UserSQL, tags=["List User"]) ###Listar UserID###
async def list_users_by_Id_endpoint(user_id: int, session: AsyncSession = Depends(get_session)):
    return await get_user(session, user_id)

@app.patch("/users/{user_id}", response_model=UserSQL, tags=["Update User"]) ###Actualizar User###
async def update_user_endpoint(user_id:int, user_update:UserSQL, session:AsyncSession = Depends(get_session)):
    updated_user = await crud.update_user(session, user_id, user_update.dict(exclude_unset=True))
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
@app.patch("/tasks/{task_id}", response_model=TaskBase, tags=["Update Task"]) ###Actualizar Tarea##
async def update_task_endpoint(task_id: int, task_update: TaskUpdated, session: AsyncSession = Depends(get_session)):
    updated_task = await crud.update_task(session, task_id, task_update.dict(exclude_unset=True))
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task
@app.patch("/users/{user_id}/premium", response_model=UserSQL, tags=["Update User"]) ###COnvertir usuario a premium###
async def convert_user_to_premium(user_id: int, session: AsyncSession = Depends(get_session)):
    updated_user = await crud.convert_userToPremium(session, user_id, {"premium": True})
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
@app.patch("/users/{user_id}/status", response_model=UserSQL, tags=["Update User"]) ###convertir status del usuario###
async def update_user_status_endpoint(
    user_id: int = Path(..., description="ID del usuario a actualizar"),
    new_status: UserStatus = Query(..., description="Nuevo estado: a (activo), i (inactivo), d (eliminado)"),
    session: AsyncSession = Depends(get_session)
):
    updated_user = await crud.convert_user_status(session, user_id, new_status)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
@app.patch("/tasks/{task_id}/status", response_model=TaskBase, tags=["Update Task"]) ###convertir status de la tarea###
async def update_task_status_endpoint(
    task_id: int = Path(..., description="ID del task a actualizar"),
    new_status: TaskStatus = Query(..., description="Nuevo estado: p(Pendiente), ip(en ejecucion), f(completada), c(cancelada)"),
    session: AsyncSession = Depends(get_session)
):
    updated_task = await crud.convert_task_status(session, task_id, new_status)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


