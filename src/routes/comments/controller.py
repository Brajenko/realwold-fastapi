from src.routes.users.controller import profile_from_user
from typing import Optional
from sqlalchemy.orm import Session
from src.routes.users.models import User as USER
from src.routes.articles.models import Article
from . import models, schemas


def get_comment_by_id(id: int, db: Session) -> Optional[models.Comment]:
    return db.query(models.Comment).get(id)


def get_comments_by_article(article: Article, db:Session) -> list[Optional[models.Comment]]:
    return list(db.query(models.Comment).filter(models.Comment.article == article))


def db_comment_to_schema(comment: models.Comment, user: Optional[USER] = None) -> schemas.Comment:
    return schemas.Comment(
        id=comment.id,
        body=comment.body,
        createdAt=comment.created_at,
        updatedAt=comment.updated_at,
        author=profile_from_user(comment.author, user)
    )


def create_comment(comment: schemas.CreateComment,article: Article, user: USER, db: Session) -> models.Comment:
    db_comment = models.Comment(body=comment.body, author=user, article=article)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(comment: models.Comment, db: Session) -> None:
    db.delete(comment)
    db.commit()
