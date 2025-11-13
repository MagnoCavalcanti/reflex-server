from .base import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    username = Column('username', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
    email = Column('email', String, nullable=False)
    fullname = Column('fullname', String)
    telephone = Column('telephone', String)
