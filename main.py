from fastapi import FastAPI, Depends
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from db_connection import AsyncDatabaseConnection
from models import Task, TaskCreate  # Asegúrate de que estas importaciones sean correctas

# Inicializar la conexión a la base de datos
db = AsyncDatabaseConnection()
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await db.init_db("sqlite+aiosqlite:///./database.db")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

# Endpoint para crear tareas
@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate, session: AsyncSession = Depends(db.get_session)):
    new_task = Task(**task.dict())
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task

# Endpoint para listar tareas
@app.get("/tasks/", response_model=list[Task])
async def list_tasks(session: AsyncSession = Depends(db.get_session)):
    result = await session.execute(select(Task))
    tasks = result.scalars().all()
    return tasks