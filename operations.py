from datetime import datetime
from models import TaskBase, UserBase
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

async def create_user(session: AsyncSession, user:UserBase):
    dbuser= UserBase.model_validate(user, from_attributes=True)
    session.add(dbuser)
    await session.commit()
    await session.refresh(dbuser)
    return dbuser

async def list_users(session: AsyncSession):
    query =select(UserBase)
    results = await session.execute(query)
    users=results.scalars().all()
    return users
