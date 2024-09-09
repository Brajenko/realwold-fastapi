from src.routes.articles import models as article_models
from src.routes.articles import schemas as article_schemas


def taglist_to_schema(tags: list[article_models.Tag]) -> article_schemas.TagList:
    return article_schemas.TagList(tags=[t.name for t in tags])
