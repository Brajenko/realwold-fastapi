from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.routes.articles.controller import get_article_by_slug
from .db_dependency import get_db


async def get_article(slug: str, db: Session = Depends(get_db)):
    db_article = get_article_by_slug(db, slug)
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Article with this slug not found',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return db_article
