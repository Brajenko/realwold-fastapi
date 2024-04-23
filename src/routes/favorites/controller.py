from sqlalchemy.orm import Session

from src.routes.articles.models import Article as ARTICLE
from src.routes.users.models import User as USER


def favorite_article(article: ARTICLE, user: USER, db: Session) -> ARTICLE:
    article.favorited_by.append(user)
    db.add_all([user, article])
    db.commit()
    db.refresh(article)
    return article


def unfavorite_article(article: ARTICLE, user: USER, db: Session) -> ARTICLE:
    article.favorited_by.remove(user)
    db.add_all([user, article])
    db.commit()
    db.refresh(article)
    return article
