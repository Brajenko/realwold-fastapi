from typing import Optional

from pydantic import BaseModel, NonNegativeInt

from src.util.global_schemas import MicrosecondsDateTime
from src.routes.users.schemas import Profile


class BaseArticle(BaseModel):
    title: str
    description: str
    body: str
    tagList: list[str] = []


class CreateArticle(BaseArticle):
    pass


class UpdateArticle(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None


class Article(BaseArticle):
    slug: str
    createdAt: MicrosecondsDateTime
    updatedAt: MicrosecondsDateTime
    favorited: bool
    favoritesCount: NonNegativeInt
    author: Profile


class ArticleResponse(BaseModel):
    article: Article


class MultipleArticlesResponse(BaseModel):
    articles: list[Article]
    articlesCount: NonNegativeInt


class TagList(BaseModel):
    tags: list[str]
