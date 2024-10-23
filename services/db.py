from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import Base, UserToken
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

# Настройки подключения к базе данных
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

# Создаем движок и сессию
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

# Создаем таблицы, если они не существуют
Base.metadata.create_all(engine)


def save_token(user_id, token):
    session = Session()
    user_token = UserToken(user_id=user_id, token=token)
    session.merge(user_token)  # Используем merge для обновления или вставки
    session.commit()
    session.close()
