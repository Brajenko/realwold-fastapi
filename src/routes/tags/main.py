from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from src.routes.articles import controller as article_controller
from src.routes.articles import schemas as article_schemas
from src.util.db_dependency import get_db

from . import controller


router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("")
async def get_tags(db: Session = Depends(get_db)) -> article_schemas.TagList:
    return controller.taglist_to_schema(article_controller.get_tags(db))
