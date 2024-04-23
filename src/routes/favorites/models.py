from sqlalchemy import Column, ForeignKey, Table

from src.config.database import Base

favorites_to_users_table = Table(
    'favorites_to_users',
    Base.metadata,
    Column('article_id', ForeignKey('articles.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
)
