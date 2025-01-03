from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import MetaData, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, delete

tags = ['Задачи 📃']
engine = create_async_engine('postgresql+asyncpg://postgres:serat@localhost:5432/tasks', echo=False)
new_session = async_sessionmaker(engine)
app = FastAPI()
metadata = MetaData()

'''
Base sqlalchemy class
'''

class Base(DeclarativeBase):
    ...
'''
Pydantic Schema
'''
class TaskSchema(BaseModel):
    title: str
    body: str
    completed: bool = False
    categories: list | None

'''
Sqlalchemy ORM
'''
class TaskORM(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    body: Mapped[str]
    completed: Mapped[bool]
    categories: Mapped[str | None]

async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@app.post('/create_task', summary='Создать задачу', tags=tags)
async def create_task(task: TaskSchema):
    task.categories = str(task.categories)
    task = TaskORM(title=task.title, body=task.body, completed=task.completed, categories=task.categories)
    async with new_session() as session:
        session.add(task)
        await session.commit()
    return {'success': 'Успешно добавлено в базу'}

@app.get('/get_tasks', summary='Получить список задач', tags=tags)
async def get_tasks_list():
    async with new_session() as session:
        query = select(TaskORM)
        results = await session.execute(query)
        result = results.scalars().all()
    return {'tasks': result}

@app.get('/get_task/{id}', summary='Получить задачу по id', tags=tags)
async def get_task(id: int):
    async with new_session() as session:
        query = select(TaskORM).filter_by(id=id)
        results = await session.execute(query)
        result = results.scalars().all()
    return {'task': result}

@app.delete('/delete_task/{id}', summary='Удалить задачу', tags=tags)
async def delete_task(id: int):
    async with new_session() as session:
        query = select(TaskORM.id)
        ids = await session.execute(query)
        ids = ids.scalars().all()
        if id in ids:
            query = select(TaskORM).filter_by(id=id)
            result = await session.execute(query)
            task = result.scalars().first()
            await session.delete(task)
            await session.commit()
            return {'success': 'Успешно удалено из базы'}
        else:
            return HTTPException(status_code=404, detail='ID нет в базе')

@app.get('/get_tasks_by_categories/{category}', summary='Получить все задачи по категориям', tags=tags)
async def get_tasks_by_categories(category: str):
    async with new_session() as session:
        query = text("""
        SELECT * FROM tasks
        WHERE categories LIKE :category;
        """)
        results = await session.execute(query, {'category': f"%{category}%"})
        result = results.mappings().all()
        print(result)
    return {'tasks': result}


@app.post('/update_task_status/{id}', summary='Обновить статус задачи', tags=tags)
async def update_task_status(id: int):
    async with new_session() as session:
        query = select(TaskORM).filter_by(id=id)
        results = await session.execute(query)
        result = results.scalars().first()
        result.completed = True
        await session.commit()
    return {'success': 'Статус задачи обновлён'}