from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserToken(Base):
    __tablename__ = 'user_tokens'

    user_id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
