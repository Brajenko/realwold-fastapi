from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.database import Base


follows_table = Table(
    "follows",
    Base.metadata,
    Column("follower_id", ForeignKey("users.id"), primary_key=True),
    Column("following_id", ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(length=100), unique=True)
    username: Mapped[str] = mapped_column(String(length=50), unique=True)
    bio: Mapped[Optional[str]] = mapped_column(Text())
    image: Mapped[str] = mapped_column(
        String(length=255), default="https://api.realworld.io/images/smiley-cyrus.jpeg"
    )
    password: Mapped[str] = mapped_column(String(length=255))
    followings: Mapped[list["User"]] = relationship(
        secondary=follows_table,
        primaryjoin=lambda: User.id == follows_table.c.follower_id,
        secondaryjoin=lambda: User.id == follows_table.c.following_id,
    )
