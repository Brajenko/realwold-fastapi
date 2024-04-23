from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

from src.config.database import engine
from src.routes.users import models as users_models
from src.routes.users.main import router as users_router
from src.routes.articles import models as articles_models
from src.routes.articles.main import router as articles_router
from src.routes.comments import models as comments_models
from src.routes.comments.main import router as comments_router
from src.routes.favorites import models as favorites_models
from src.routes.favorites.main import router as favorites_router

description = """
# Implemantation of conduit backend in fastAPI

## Endpoints
[https://realworld-docs.netlify.app/docs/specs/backend-specs/endpoints/](https://realworld-docs.netlify.app/docs/specs/backend-specs/endpoints/)

## Responses
[https://realworld-docs.netlify.app/docs/specs/backend-specs/api-response-format](https://realworld-docs.netlify.app/docs/specs/backend-specs/api-response-format)
"""

tags_metadata = [
    {
        'name': 'auth',
        'description': 'Authenfication and registration here.',
    },
    {
        'name': 'articles',
        'description': 'All operations with articles.',
    },
    {
        'name': 'comments',
        'description': 'All operations with comments to articles.'
    },
    {
        'name': 'favorite',
        'description': 'Favorite article operations.'
    },
    {
        'name': 'profile',
        'description': 'View profiles and follow them.',
    },
    {
        'name': 'current_user',
        'description': 'All operations with current user.',
    },
    {
        'name': 'users',
        'description': 'All operations with users. profile + auth + current_user',
    },
]

app = FastAPI(
    title='Conduit API',
    description=description,
    version='1.0.0',
    openapi_tags=tags_metadata
)

users_models.Base.metadata.create_all(bind=engine)
articles_models.Base.metadata.create_all(bind=engine)
comments_models.Base.metadata.create_all(bind=engine)
favorites_models.Base.metadata.create_all(bind=engine)

app.include_router(users_router, prefix='/api')
app.include_router(articles_router, prefix='/api')
app.include_router(comments_router, prefix='/api')
app.include_router(favorites_router, prefix='/api')


@app.get('/')
def index() -> RedirectResponse:
    '''Redirect to docs'''
    return RedirectResponse('/docs', 308)


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8080, reload=True)
