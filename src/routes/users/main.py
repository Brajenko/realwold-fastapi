from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from src.util.db_dependency import get_db

from . import controller, schemas, models

router = APIRouter()

auth_router = APIRouter(prefix='/users')


@auth_router.post('/')
async def registration(
    user: Annotated[schemas.RegisterUser, Body(embed=True)], db: Session = Depends(get_db)
) -> schemas.UserResponse:
    """Add new user"""
    db_user = controller.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = controller.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    created_user = controller.create_user(db, user)
    return {'user': schemas.AuthenficatedUser(**created_user.__dict__, token='token')}


@auth_router.get('/')
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()



@auth_router.post('/login')
async def authentication(user: Annotated[schemas.LoginUser, Body(embed=True)]) -> schemas.UserResponse:
    """Authenficate user"""
    pass


user_router = APIRouter(prefix='/user')


@user_router.get('/')
async def get_current_user(db: Session = Depends(get_db)) -> schemas.UserResponse:
    """Return current user"""
    return {'user': schemas.AuthenficatedUser(**controller.get_user(db, 2), token='token')}


# @user_router.put('/')
# async def update_user(req: UpdateRequest) -> UserResponse:
#     """Update current user"""


router.include_router(auth_router)
router.include_router(user_router)
