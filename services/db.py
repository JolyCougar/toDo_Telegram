from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import Base, UserToken, Task
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

# Настройки подключения к базе данных
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

# Создаем движок и сессию
engine = create_engine(DB_URL)
Session_local = sessionmaker(bind=engine)

# Создаем таблицы, если они не существуют
Base.metadata.create_all(engine)


def save_token(user_id, token):
    session = Session_local()
    user_token = UserToken(user_id=user_id, token=token)
    session.merge(user_token)  # Используем merge для обновления или вставки
    session.commit()
    session.close()


def get_token(user_id: int, session: Session_local) -> str:
    user = session.query(UserToken).filter(UserToken.user_id == user_id).first()
    return user.token if user else None


def get_local_mode(user_id: int, session: Session_local) -> bool:
    user_token = session.query(UserToken).filter_by(user_id=user_id).first()
    return user_token.local_mode if user_token else False


def set_local_mode(user_id: int, local_mode: bool, session: Session_local) -> None:
    user_token = session.query(UserToken).filter_by(user_id=user_id).first()
    if user_token:
        user_token.local_mode = local_mode
    else:
        user_token = UserToken(user_id=user_id, local_mode=local_mode)
        session.add(user_token)
    session.commit()


def add_task(user_id: int, title: str, description: str, session: Session_local) -> Task:
    new_task = Task(user_id=user_id, title=title, description=description)
    session.add(new_task)
    session.commit()
    return new_task


def delete_task(task_id: int, session: Session_local) -> bool:
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        session.delete(task)
        session.commit()
        return True
    return False


def complete_task(task_id: int, session: Session_local) -> bool:
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        task.complete = True
        session.commit()
        return True
    return False


def get_tasks_from_local(user_id: int, session: Session_local, completed: bool = None) -> list:
    query = session.query(Task).filter_by(user_id=user_id)
    print(completed)

    if completed is not None:
        query = query.filter_by(is_completed=completed)
        print(query)
    return query.all()


def get_task_details(task_id: int, session: Session_local) -> Task:
    return session.query(Task).filter_by(id=task_id).first()
