from typing import Optional

from sqlalchemy.orm import Session

from src.routes.users.controller import profile_from_user
from src.routes.users.models import User as USER

from . import models, schemas


def article_to_schema(article: models.Article, user: Optional[USER] = None) -> schemas.Article:
    return schemas.Article(
        title=article.title,
        description=article.description,
        body=article.body,
        tagList=[tag.name for tag in article.tags],
        slug=article.slug,
        createdAt=article.created_at,
        updatedAt=article.updated_at,
        favorited=(user in article.favorited_by),
        favoritesCount=len(article.favorited_by),
        author=profile_from_user(article.author, user),
    )


def generate_slug(db: Session, title: str) -> str:
    slug = "-".join(title.lower().split(" "))
    if get_article_by_slug(db, slug):
        slug += "-1"
        while get_article_by_slug(db, slug):
            slug, _, n = slug.rpartition("-")
            slug += "-" + str(int(n) + 1)
    return slug


def get_tags_by_names(db: Session, tag_names: list[str]):
    tags = []
    for tag_name in tag_names:
        tag = db.query(models.Tag).filter_by(name=tag_name).first()
        if tag is None:
            tag = models.Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        tags.append(tag)
    return tags


def get_article_by_slug(db: Session, slug: str) -> models.Article | None:
    return db.query(models.Article).filter_by(slug=slug).first()


def create_article(db: Session, article: schemas.CreateArticle, author: USER) -> models.Article:
    db_article = models.Article(
        slug=generate_slug(db, article.title),
        title=article.title,
        description=article.description,
        body=article.body,
        tags=get_tags_by_names(db, article.tagList),
        author=author,
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(
    db: Session, db_article: models.Article, article: schemas.UpdateArticle
) -> models.Article:
    if article.title:
        db_article.title = article.title
        db_article.slug = generate_slug(db, article.title)
    db_article.description = article.description or db_article.description
    db_article.body = article.body or db_article.body
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def get_tags(db: Session):
    return db.query(models.Tag).all()


def db_tags_to_list(tags: list[models.Tag]):
    return [tag.name for tag in tags]


def get_articles(
    db: Session,
    limit: int,
    offset: int,
    tag: Optional[str] = None,
    author: Optional[USER] = None,
    favorited: Optional[USER] = None,
) -> list[models.Article]:
    q = db.query(models.Article)
    if tag is not None:
        q = q.filter(models.Article.tags.any(models.Tag.name == tag))
    if author is not None:
        q = q.filter(models.Article.author == author)
    if favorited is not None:
        q = q.filter(models.Article.favorited_by.contains(favorited))
    return list(q.order_by(models.Article.created_at).limit(limit).offset(offset))


def get_articles_by_followings(
    db: Session, user: USER, limit: int, offset: int
) -> list[models.Article]:
    return list(
        db.query(models.Article)
        .join(models.Article.author)
        .filter(USER.id.in_(set(u.id for u in user.followings)))
        .order_by(models.Article.created_at)
        .limit(limit)
        .offset(offset)
    )
