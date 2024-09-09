from pydantic import BaseModel, PositiveInt

from src.routes.users.schemas import Profile
from src.util.global_schemas import MicrosecondsDateTime


class CreateComment(BaseModel):
    body: str


class Comment(CreateComment):
    id: PositiveInt
    createdAt: MicrosecondsDateTime
    updatedAt: MicrosecondsDateTime
    body: str
    author: Profile


class CommentResponse(BaseModel):
    comment: Comment


class MultipleCommentsResponse(BaseModel):
    comments: list[Comment]
