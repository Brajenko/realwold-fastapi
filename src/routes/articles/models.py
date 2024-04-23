from typing import TYPE_CHECKING


from sqlalchemy import Column, DateTime, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.config.database import Base
from src.routes.favorites.models import favorites_to_users_table
from src.routes.users.models import User


if TYPE_CHECKING:
    from src.routes.comments.models import Comment

articles_to_tags_table = Table(
    'articles_to_tags',
    Base.metadata,
    Column('article_id', ForeignKey('articles.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True),
)


class Article(Base):
    __tablename__ = 'articles'

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text())
    tags: Mapped[list['Tag']] = relationship(secondary=articles_to_tags_table)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    author: Mapped['User'] = relationship()
    favorited_by: Mapped[list['User']] = relationship(secondary=favorites_to_users_table)
    comments: Mapped[list['Comment']] = relationship(back_populates='article')


class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
