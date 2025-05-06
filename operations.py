from datetime import datetime
from models import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List, Dict, Any
from datetime import datetime
async def create_task_sql(session: AsyncSession, task:TaskSQL):
    dbtask= TaskSQL.model_validate(task, from_attributes=True)
    dbtask.created_at = datetime.now()

    session.add(dbtask)
    await session.commit()
    await session.refresh(dbtask)
    return dbtask

async def list_tasks(session: AsyncSession):
    query =select(TaskSQL)
    results = await session.execute(query)
    tasks=results.scalars().all()
    return tasks

async def create_user_sql(session: AsyncSession, user:UserSQL):
    dbuser= UserSQL.model_validate(user, from_attributes=True)
    session.add(dbuser)
    await session.commit()
    await session.refresh(dbuser)
    return dbuser

async def list_users(session: AsyncSession):
    query =select(UserSQL)
    results = await session.execute(query)
    users=results.scalars().all()
    return users
##Get task with id
async def get_task(session: AsyncSession, task_id:int):
    return await session.get(TaskSQL, task_id)
###Get user with id
async def get_user(session: AsyncSession, user_id:int):
    return await session.get(UserSQL, user_id)


async def update_user(session: AsyncSession, user_id:int, user_update: Dict[str, Any]):
    user= await session.get(UserSQL, user_id)
    if user is None:
        return None

    user_data= user.dict()
    for key, value in user_update.items():
        if value is not None:
            user_data[key] = value
        setattr(user, key, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
async def update_task(session: AsyncSession, task_id: int, task_update: Dict[str, Any]):
    task = await session.get(TaskSQL, task_id)
    if task is None:
        return None

    for key, value in task_update.items():
        if value is not None:
            if key in ["created_at", "updated_at"] and isinstance(value, str):
                value = datetime.fromisoformat(value.replace("Z", "+00:00"))
            setattr(task, key, value)

    task.updated_at = datetime.now()

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task(session: AsyncSession, task_id:int):
    return await session.get(TaskSQL, task_id)
async def get_user(session: AsyncSession, user_id:int):
    return await session.get(UserSQL, user_id)
