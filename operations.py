from datetime import datetime

from sqlmodel import Session

from models import TaskStatus, TaskBase
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def create_task(session: AsyncSession, task:TaskBase):
    dbtask= TaskBase.model_validate(task, from_attributes=True)
    dbtask.created_at = datetime.now()

    session.add(dbtask)
    await session.commit()
    await session.refresh(dbtask)
    return dbtask

async def list_tasks(session: AsyncSession):
    query =select(TaskBase)
    results = await session.execute(query)
    tasks=results.scalars().all()
    return tasks
