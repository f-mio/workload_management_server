# 標準モジュール
from typing import Optional
from decimal import Decimal
import datetime as dt
# サードパーティ製モジュール
from typing_extensions import Annotated
from sqlalchemy import ForeignKey, String, Numeric, BigInteger, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry

# ref:
#    - https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#postgresql-data-types
#    - https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html
#    - mapped_column: https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column

# 型の宣言
minute_value_type = Annotated[Decimal, 4]
bigint_type = Annotated[int, "bigint"]
text_type = Annotated[str, Text]


class Base(DeclarativeBase):
    """
    クラス情報に継承させるメタクラス(?)
    """
    registry = registry(
        type_annotation_map={
            bigint_type: BigInteger(),
            text_type: Text(),
            minute_value_type: Numeric(4, 2),
        }
    )


class User(Base):
    """
    本アプリケーションで作成するUserを格納するテーブル
    """
    __tablename__ = "user"

    id: Mapped[bigint_type] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), index=True, unique=True)
    family_name: Mapped[Optional[str]] = mapped_column(String(30))
    first_name: Mapped[Optional[str]] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    update_timestamp: Mapped[dt.datetime]
    create_timestamp: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now)


class Project(Base):
    """
    JIRA Projectを格納するテーブル
    """
    __tablename__ = "project"

    id: Mapped[bigint_type] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    jira_key: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[text_type]
    is_target: Mapped[bool] = mapped_column(default=False)
    update_timestamp: Mapped[dt.datetime] = mapped_column(nullable=False, onupdate=dt.datetime.now)
    create_timestamp: Mapped[dt.datetime] = mapped_column(nullable=False, default=dt.datetime.now)


class Issue(Base):
    """
    JIRA Issueを格納するテーブル
    """
    __tablename__ = "issue"

    id: Mapped[bigint_type] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    project_id: Mapped[bigint_type] = mapped_column(ForeignKey("project.id"))
    parrent_issue_id: Mapped[bigint_type] = mapped_column(ForeignKey("issue.id"))
    type: Mapped[str] = mapped_column(String(10))
    description: Mapped[text_type]
    status: Mapped[str] = mapped_column(String(10))
    start_date: Mapped[dt.date]
    limit_date: Mapped[dt.date]
    end_date: Mapped[dt.date]
    update_timestamp: Mapped[dt.datetime] = mapped_column(nullable=False, onupdate=dt.datetime.now)
    create_timestamp: Mapped[dt.datetime] = mapped_column(nullable=False, default=dt.datetime.now)


class Subtask(Base):
    """
    JIRA Subtaskを格納するテーブル
    """
    __tablename__ = "subtask"

    id: Mapped[bigint_type] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    issue_id: Mapped[bigint_type] = mapped_column(ForeignKey("issue.id"))
    status: Mapped[str] = mapped_column(String(10))
    description: Mapped[text_type]
    update_timestamp: Mapped[dt.datetime] = mapped_column(nullable=False, onupdate=dt.datetime.now)
    create_timestamp: Mapped[dt.datetime] = mapped_column(nullable=False, default=dt.datetime.now)


class Workload(Base):
    """
    JIRA Subtaskに紐づく各人の工数情報を格納するテーブル
    """
    __tablename__ = "workload"

    id: Mapped[bigint_type] = mapped_column(primary_key=True, index=True)
    subtask_id: Mapped[bigint_type] = mapped_column(ForeignKey("subtask.id"))
    user_id: Mapped[bigint_type] = mapped_column(ForeignKey("user.id"))
    work_date: Mapped[dt.date] = mapped_column(index=True)
    workload_minute: Mapped[minute_value_type]
    detail: Mapped[text_type]
    update_timestamp: Mapped[dt.datetime] = mapped_column(nullable=False, onupdate=dt.datetime.now)
    create_timestamp: Mapped[dt.datetime] = mapped_column(nullable=False, default=dt.datetime.now)
