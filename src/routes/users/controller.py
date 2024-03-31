from fastapi import Depends
from sqlalchemy.orm import Session

from . import models, schemas
from src.util import password_manager, jwt_manager


def get_user(db: Session, user_id: int) -> models.User | None:
    """Get user by id"""
    return db.query(models.User).get(user_id)


def get_user_by_email(db: Session, email: schemas.Email) -> models.User | None:
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: schemas.Username) -> models.User | None:
    """Get user by username"""
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.RegisterUser) -> models.User:
    """Add new user to db"""
    hashed_password = password_manager.get_hashed_password(user.password.get_secret_value())
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenficate_user(db: Session, username: schemas.Username, password: schemas.Password) -> models.User | None:
    """Check credintials and return User"""
    db_user = db.query(models.User).filter(username == username).first()
    if not db_user:
        return None
    if not password_manager.verify_password(password, db_user.password):
        return None
    return db_user
        

def create_access_token(username: schemas.Username):
    """Create access token by username"""
    return jwt_manager.create_access_token(username)


def get_user_from_token(token: str):
    pass