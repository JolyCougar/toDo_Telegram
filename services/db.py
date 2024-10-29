from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models_db import Base, UserToken, Task
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

# Настройки подключения к базе данных
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

# Создаем движок и сессию
engine = create_engine(DB_URL,  pool_size=10, max_overflow=20, pool_timeout=60)
Session_local = sessionmaker(bind=engine)

# Создаем таблицы, если они не существуют
Base.metadata.create_all(engine)


def save_token(user_id, token):
    """ Сохранение токена авторизации в БД """

    session = Session_local()
    user_token = UserToken(user_id=user_id, token=token)
    session.merge(user_token)  # Используем merge для обновления или вставки
    session.commit()
    session.close()


def get_token(user_id: int, session: Session_local) -> str:
    """ Получение токена авторизации из БД """

    user = session.query(UserToken).filter(UserToken.user_id == user_id).first()
    return user.token if user else None


def get_local_mode(user_id: int, session: Session_local) -> bool:
    """ Получение статуса локального режима """

    user_token = session.query(UserToken).filter_by(user_id=user_id).first()
    return user_token.local_mode if user_token else False


def set_local_mode(user_id: int, local_mode: bool, session: Session_local) -> None:
    """ Установка локального режима """

    user_token = session.query(UserToken).filter_by(user_id=user_id).first()
    if user_token:
        user_token.local_mode = local_mode
    else:
        user_token = UserToken(user_id=user_id, local_mode=local_mode)
        session.add(user_token)
    session.commit()


def add_task(user_id: int, title: str, description: str, session: Session_local) -> Task:
    """ Добавление задачи в локальную БД """

    new_task = Task(user_id=user_id, title=title, description=description)
    session.add(new_task)
    session.commit()
    return new_task


def delete_task_local(task_id: int, session: Session_local) -> bool:
    """ Удаление задачи из локальной БД """

    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        session.delete(task)
        session.commit()
        return True
    return False


def complete_task(task_id: int, session: Session_local) -> bool:
    """ Подтверждение выполнения задачи в локальной БД """

    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        task.is_completed = True
        session.commit()
        return True
    return False


def get_tasks_from_local(user_id: int, session: Session_local, completed: bool = '') -> list:
    """ Получение задач из локальной БД,
    флаг completed позволяет получить либо выполненные
    либо не выполненные задачи из локальной БД """

    query = session.query(Task).filter_by(user_id=user_id)

    if completed != '':
        query = query.filter_by(is_completed=completed)
    return query.all()
