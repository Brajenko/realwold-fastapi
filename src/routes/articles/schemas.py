import datetime as dt
from typing import Optional

from pydantic import BaseModel, NonNegativeInt, PositiveInt

from src.routes.users.schemas import Profile


class BaseArticle(BaseModel):
    title: str
    description: str
    body: str
    tagList: Optional[list[str]] = []


class CreateArticle(BaseArticle):
    pass


class UpdateArticle(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None


class Article(BaseArticle):
    slug: str
    createdAt: dt.datetime
    updatedAt: dt.datetime
    favorited: bool
    favorites_count: NonNegativeInt
    author: Profile


class ArticleResponse(BaseModel):
    article: Article


class MultipleArticlesResponse(BaseModel):
    articles: list[Article]
    articles_count: NonNegativeInt


class TagList(BaseModel):
    tags: list[str]
