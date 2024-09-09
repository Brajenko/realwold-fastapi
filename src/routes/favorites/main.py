from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.util.db_dependency import get_db
from src.util.user_dependency import get_user
from src.util.article_dependency import get_article_dependency
from src.routes.users.models import User as USER
from src.routes.articles.models import Article as ARTICLE
from src.routes.articles.controller import article_to_schema
from src.routes.articles.schemas import ArticleResponse

from . import controller

router = APIRouter(prefix="/articles/{slug}/favorite", tags=["favorite"])


@router.post("")
async def favorite_article(
    article: Annotated[ARTICLE, Depends(get_article_dependency)],
    user: Annotated[USER, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ArticleResponse:
    controller.favorite_article(article, user, db)
    return ArticleResponse(article=article_to_schema(article, user))


@router.delete("")
async def unfavorite_article(
    article: Annotated[ARTICLE, Depends(get_article_dependency)],
    user: Annotated[USER, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
) -> ArticleResponse:
    controller.unfavorite_article(article, user, db)
    return ArticleResponse(article=article_to_schema(article, user))
