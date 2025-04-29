from fastapi import FastAPI, Depends
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from operations import create_task, list_tasks
from models import TaskBase
from db_connection import get_session, init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.post("/tasks/", response_model=TaskBase)
async def create_task_endpoint(task: TaskBase, session: AsyncSession = Depends(get_session)):
    return await create_task(session, task)

@app.get("/tasks/", response_model=list[TaskBase])
async def list_tasks_endpoint(session: AsyncSession = Depends(get_session)):
    return await list_tasks(session)