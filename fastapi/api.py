from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy import MetaData
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

tags = ['Задачи 📃']
engine = create_engine('postgresql://postgres:serat@localhost:5432/tasks', echo=False)
new_session = sessionmaker(engine)
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

TaskORM.metadata.create_all(engine)

@app.post('/create_task', summary='Создать задачу', tags=tags)
def create_task(task: TaskSchema):
    task = TaskORM(title=task.title, body=task.body, completed=task.completed, categories=task.categories)
    with new_session() as session:
        session.add(task)
        session.commit()
    return {'success': 'Успешно добавлено в базу'}

@app.get('/get_tasks', summary='Получить список задач', tags=tags)
def get_tasks_list():
    with new_session() as session:
        result = session.query(TaskORM).all()
    return {'tasks': result}

@app.get('/get_task/{id}', summary='Получить задачу по id', tags=tags)
def get_task(id: int):
    with new_session() as session:
        result = session.query(TaskORM).filter_by(id=id).all()
    return {'task': result}

@app.delete('/delete_task/{id}', summary='Удалить задачу', tags=tags)
def delete_task(id: int):
    with new_session() as session:
        ids = session.query(TaskORM.id).all()
        if id in ids[0]:
            session.query(TaskORM).filter_by(id=id).delete()
            session.commit()
            return {'success': 'Успешно удалено из базы'}
        else:
            return HTTPException(status_code=404, detail='ID нет в базе')

@app.get('/get_tasks_by_categories/{category}', summary='Получить все задачи по категориям', tags=tags)
def get_tasks_by_categories(category: str):
    with new_session() as session:
        sql = text("""
        SELECT * FROM tasks
        WHERE categories LIKE :category;
        """)
        result = session.execute(sql, {'category': f"%{category}%"}).mappings().all()
    return {'tasks': result}


@app.post('/update_task_status/{id}', summary='Обновить статус задачи', tags=tags)
def update_task_status(id: int):
    with new_session() as session:
        completed = session.query(TaskORM).filter_by(id=id).first()
        completed.completed = True
        session.commit()
    return {'success': 'Статус задачи обновлён'}