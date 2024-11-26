# 標準モジュール
from typing import List, Optional
import datetime as dt
# サードパーティ製モジュール
from sqlalchemy import ForeignKey, String, BIGINT
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

# ref:
#    - https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-data-types
#    - https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    family_name: Mapped[Optional[str]] = mapped_column(String(30))
    first_name: Mapped[Optional[str]] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool]
    update_timestamp: Mapped[dt.datetime]
    create_timestamp: Mapped[dt.datetime]


# class Project(Base):
#     __tablename__ = "project"

# class Issue(Base):
#     __tablename__ = "issue"

# class Subtask(Base):
#     __tablename__ = "subtask"

# class Workload(Base):
#     __tablename__ = "workload"
