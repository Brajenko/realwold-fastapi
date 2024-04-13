from typing import Optional

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base
from src.routes.articles.models import Article, favorites_to_users_table


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(length=100), unique=True)
    username: Mapped[str] = mapped_column(String(length=50), unique=True)
    bio: Mapped[Optional[str]] = mapped_column(Text())
    image: Mapped[str] = mapped_column(default='https://api.realworld.io/images/smiley-cyrus.jpeg')
    password: Mapped[str]
    favorited_articles: Mapped[list[Article]] = relationship(
        secondary=favorites_to_users_table, back_populates='users'
    )