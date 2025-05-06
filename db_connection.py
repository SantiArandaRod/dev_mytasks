
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import  AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./database.db")
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

POSTGRESQL_ADDON_HOST="blrds6moy36ytber4epr-postgresql.services.clever-cloud.com"
POSTGRESQL_ADDON_DB="blrds6moy36ytber4epr"
POSTGRESQL_ADDON_USER="ub73yioakc05zqt9meah"
POSTGRESQL_ADDON_PORT=5432
POSTGRESQL_ADDON_PASSWORD="XhCtvMSYLlU4w5z5KpXIzYeSvIUxuc"
POSTGRESQL_ADDON_URI="postgresql://ub73yioakc05zqt9meah:XhCtvMSYLlU4w5z5KpXIzYeSvIUxuc@blrds6moy36ytber4epr-postgresql.services.clever-cloud.com:5432/blrds6moy36ytber4epr"

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session
