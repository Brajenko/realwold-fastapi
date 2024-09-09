from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.util.db_dependency import get_db
from src.util.user_dependency import get_user

from . import controller, models, schemas

router = APIRouter(tags=["users"])

auth_router = APIRouter(prefix="/users", tags=["auth"])


@auth_router.post("")
async def registration(
    user: Annotated[schemas.RegisterUser, Body(embed=True)],
    db: Session = Depends(get_db),
) -> schemas.UserResponse:
    """Add new user"""
    db_user = controller.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = controller.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    created_user = controller.create_user(db, user)
    token = controller.create_access_token(created_user)
    return schemas.UserResponse(
        user=schemas.AuthenficatedUser(**created_user.__dict__, token=token)
    )


@auth_router.post("/login")
async def authentication(
    user: Annotated[schemas.LoginUser, Body(embed=True)],
    db: Session = Depends(get_db),
) -> schemas.UserResponse:
    """Authenficate user"""
    db_user = controller.authenficate_user(db, user.email, user.password)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with given credintials not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = controller.create_access_token(db_user)
    return schemas.UserResponse(user=schemas.AuthenficatedUser(**db_user.__dict__, token=token))


user_router = APIRouter(prefix="/user", tags=["current_user"])


@user_router.get("")
async def get_current_user_view(
    user: Annotated[models.User, Depends(get_user)],
    db: Session = Depends(get_db),
) -> schemas.UserResponse:
    """Return current user"""
    token = controller.create_access_token(user)
    return schemas.UserResponse(user=schemas.AuthenficatedUser(**user.__dict__, token=token))


@user_router.put("")
async def update_user(
    update_user: Annotated[
        schemas.UpdateUser,
        Body(embed=True, serialization_alias="user", validation_alias="user", alias="user"),
    ],
    user: Annotated[models.User, Depends(get_user)],
    db: Session = Depends(get_db),
) -> schemas.UserResponse:
    """Update current user"""
    updated_user = controller.update_user(db, user, update_user)
    token = controller.create_access_token(updated_user)
    return schemas.UserResponse(
        user=schemas.AuthenficatedUser(**updated_user.__dict__, token=token)
    )


profiles_router = APIRouter(prefix="/profiles", tags=["profile"])


@profiles_router.get("/{username}")
async def get_profile(
    username: schemas.Username, user: models.User = Depends(get_user), db: Session = Depends(get_db)
) -> schemas.ProfileResponse:
    db_user = controller.get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.ProfileResponse(profile=controller.profile_from_user(db_user, user))


@profiles_router.post("/{username}/follow")
async def follow_user(
    username: schemas.Username, user: models.User = Depends(get_user), db: Session = Depends(get_db)
) -> schemas.ProfileResponse:
    user_to_follow = controller.get_user_by_username(db, username)
    if user_to_follow is None:
        raise HTTPException(status_code=404, detail="User not found")
    followed_user = controller.create_follow(db, user, user_to_follow)
    return schemas.ProfileResponse(profile=controller.profile_from_user(followed_user, user))


@profiles_router.delete("/{username}/follow")
async def unfollow_user(
    username: schemas.Username, user: models.User = Depends(get_user), db: Session = Depends(get_db)
) -> schemas.ProfileResponse:
    user_to_unfollow = controller.get_user_by_username(db, username)
    if user_to_unfollow is None:
        raise HTTPException(status_code=404, detail="User not found")
    unfollowed_user = controller.delete_follow(db, user, user_to_unfollow)
    return schemas.ProfileResponse(profile=controller.profile_from_user(unfollowed_user, user))


router.include_router(auth_router)
router.include_router(user_router)
router.include_router(profiles_router)
