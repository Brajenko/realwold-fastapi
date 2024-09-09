from typing import Annotated, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from src.util.db_dependency import get_db
from src.util.user_dependency import get_user, get_user_optional
from src.util.article_dependency import get_article_dependency
from src.routes.users.models import User as USER
from src.routes.articles.models import Article as ARTICLE

from . import schemas, controller

router = APIRouter(prefix="/articles/{slug}/comments", tags=["comments"])


@router.post("")
async def add_comment(
    comment: Annotated[schemas.CreateComment, Body(embed=True)],
    article: Annotated[ARTICLE, Depends(get_article_dependency)],
    user: Annotated[USER, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
) -> schemas.CommentResponse:
    db_comment = controller.create_comment(comment, article, user, db)
    return schemas.CommentResponse(comment=controller.db_comment_to_schema(db_comment))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    id: int,
    article: Annotated[ARTICLE, Depends(get_article_dependency)],
    user: Annotated[USER, Depends(get_user)],
    db: Annotated[Session, Depends(get_db)],
):
    db_comment = controller.get_comment_by_id(id, db)
    if db_comment is None or db_comment not in article.comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if db_comment.author != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You need to be comment author to delete it",
            headers={"WWW-Authenticate": "Bearer"},
        )
    controller.delete_comment(db_comment, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("")
async def get_comments(
    article: Annotated[ARTICLE, Depends(get_article_dependency)],
    user: Annotated[Optional[USER], Depends(get_user_optional)],
    db: Annotated[Session, Depends(get_db)],
) -> schemas.MultipleCommentsResponse:
    db_comments = controller.get_comments_by_article(article, db)
    schema_comments = [controller.db_comment_to_schema(c, user) for c in db_comments]
    return schemas.MultipleCommentsResponse(comments=schema_comments)
