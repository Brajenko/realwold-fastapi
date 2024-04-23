from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from src.util.db_dependency import get_db
from src.util.user_dependency import get_user, get_user_optional
from src.util.article_dependency import get_article
from src.routes.users.models import User as USER
from src.routes.users.controller import get_user_by_username

from . import models, schemas, controller

router = APIRouter(prefix='/articles', tags=['articles'])


@router.post('')
async def create_article(
    article: Annotated[schemas.CreateArticle, Body(embed=True)],
    user: Annotated[USER, Depends(get_user)],
    db: Session = Depends(get_db),
) -> schemas.ArticleResponse:
    db_article = controller.create_article(db, article, user)
    return schemas.ArticleResponse(article=controller.article_to_schema(db_article, user))


@router.get('/')
async def list_articles(
    tag: str = None,
    author: str = None,
    favorited: str = None,
    limit: schemas.NonNegativeInt = 20,
    offset: schemas.NonNegativeInt = 0,
    user: USER = Depends(get_user_optional),
    db: Session = Depends(get_db),
) -> schemas.MultipleArticlesResponse:
    db_author = get_user_by_username(db, author)
    db_favorited = get_user_by_username(db, favorited)
    db_articles = controller.get_articles(db, limit, offset, tag, db_author, db_favorited)
    articles = [controller.article_to_schema(a, user) for a in db_articles]
    return schemas.MultipleArticlesResponse(articles=articles, articles_count=len(articles))


@router.get('/feed')
async def get_feed(
    limit: schemas.NonNegativeInt = 20,
    offset: schemas.NonNegativeInt = 0,
    user: USER = Depends(get_user),
    db: Session = Depends(get_db),
) -> schemas.MultipleArticlesResponse:
    db_articles = controller.get_articles_by_followings(db, user, limit, offset)
    articles = [controller.article_to_schema(a, user) for a in db_articles]
    return schemas.MultipleArticlesResponse(articles=articles, articles_count=len(articles))


@router.get('/{slug}')
async def get_article(
    db_article: models.Article = Depends(get_article),
    db: Session = Depends(get_db),
    user: USER = Depends(get_user_optional),
) -> schemas.ArticleResponse:
    return schemas.ArticleResponse(article=controller.article_to_schema(db_article, user))


@router.put('/{slug}')
async def update_article(
    article: Annotated[schemas.UpdateArticle, Body(embed=True)],
    db_article: models.Article = Depends(get_article),
    user: USER = Depends(get_user),
    db: Session = Depends(get_db),
) -> schemas.ArticleResponse:
    if db_article.author != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You can edit only your articles',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    db_article = controller.update_article(db, db_article, article)
    return schemas.ArticleResponse(article=controller.article_to_schema(db_article, user))


@router.delete('/{slug}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    db_article: models.Article = Depends(get_article),
    user: USER = Depends(get_user),
    db: Session = Depends(get_db),
):
    if db_article.author != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You can delete only your articles',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    db.delete(db_article)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
