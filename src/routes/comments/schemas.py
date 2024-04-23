import datetime as dt


from pydantic import BaseModel, PositiveInt

from src.routes.users.schemas import Profile


class CreateComment(BaseModel):
    body: str


class Comment(CreateComment):
    id: PositiveInt
    createdAt: dt.datetime
    updatedAt: dt.datetime
    body: str
    author: Profile


class CommentResponse(BaseModel):
    comment: Comment


class MultipleCommentsResponse(BaseModel):
    comments: list[Comment]