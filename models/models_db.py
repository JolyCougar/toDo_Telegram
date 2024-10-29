from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserToken(Base):
    """ Модель user для локальной таблицы """

    __tablename__ = 'user_tokens'

    user_id = Column(BigInteger, primary_key=True)
    token = Column(String, nullable=True)
    local_mode = Column(Boolean, default=False)


class Task(Base):
    """ Модель задачи для локальной таблицы """

    __tablename__ = 'tasks'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user_tokens.user_id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
