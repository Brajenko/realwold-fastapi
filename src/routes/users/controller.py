from fastapi import Depends
from sqlalchemy.orm import Session

from src.util import jwt_manager, password_manager

from . import models, schemas


def get_user(db: Session, user_id: int) -> models.User | None:
    """Get user by id"""
    return db.query(models.User).get(user_id)


def get_user_by_email(db: Session, email: schemas.Email) -> models.User | None:
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(
    db: Session, username: schemas.Username
) -> models.User | None:
    """Get user by username"""
    return (
        db.query(models.User).filter(models.User.username == username).first()
    )


def create_user(db: Session, user: schemas.RegisterUser) -> models.User:
    """Add new user to db"""
    hashed_password = password_manager.get_hashed_password(
        user.password.get_secret_value()
    )
    db_user = models.User(
        username=user.username, email=user.email, password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenficate_user(
    db: Session, email: schemas.Email, password: schemas.Password
) -> models.User | None:
    """Check credintials and return User"""
    db_user = db.query(models.User).filter(email == email).first()
    if not db_user:
        return None
    if not password_manager.verify_password(password, db_user.password):
        return None
    return db_user


def create_access_token(user: models.User):
    """Create access token for user by email"""
    return jwt_manager.create_access_token(user.email)


def get_user_from_token(db: Session, token: str):
    """Get user db instance from token"""
    email = jwt_manager.get_email_from_token(token)
    return get_user_by_email(db, email)


def update_user(
    db: Session, user: models.User, update_user: schemas.UpdateUser
):
    """Update user"""
    user.email = update_user.email or user.email
    user.username = update_user.username or user.username
    user.image = update_user.image or user.image
    user.bio = update_user.bio or user.bio
    if update_user.password:
        user.password = password_manager.get_hashed_password(
            update_user.password.get_secret_value()
        )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
