from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    address = Column(String(255), nullable=True)
    gender = Column(String(20), nullable=True)
    age = Column(Integer, nullable=True)
