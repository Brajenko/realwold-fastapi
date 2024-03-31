from fastapi import FastAPI
import uvicorn

from src.config.database import engine
from src.routes.users import models as users_models
from src.routes.users.main import router as users_router

app = FastAPI()

# creating models
users_models.Base.metadata.create_all(bind=engine)

app.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
