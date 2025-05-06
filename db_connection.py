
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import  AsyncSession
from sqlalchemy.orm import sessionmaker
#from .env import *
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./database.db")
DATABASE_URL = (
    f"postgresql+asyncpg://{os.environ['POSTGRESQL_ADDON_USER']}:"
    f"{os.environ['POSTGRESQL_ADDON_PASSWORD']}@"
    f"{os.environ['POSTGRESQL_ADDON_HOST']}:"
    f"{os.environ['POSTGRESQL_ADDON_PORT']}/"
    f"{os.environ['POSTGRESQL_ADDON_DB']}"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
