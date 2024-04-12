from sqlalchemy import Column, Integer, String, Text

from src.config.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(length=100), unique=True, nullable=False)
    username = Column(String(length=50), unique=True, nullable=False)
    bio = Column(Text(), nullable=True)
    image = Column(String(length=255), nullable=True, default='https://api.realworld.io/images/smiley-cyrus.jpeg')
    password = Column(String(length=255))