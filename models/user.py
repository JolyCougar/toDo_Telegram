from sqlalchemy import Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserToken(Base):
    __tablename__ = 'user_tokens'

    user_id = Column(BigInteger, primary_key=True)
    token = Column(String, nullable=True)
