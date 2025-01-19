from sqlalchemy import Column, Integer, String, Text, DateTime

from db.session import Base

class User(Base):
    __tablename__ = "user"

    userid = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)