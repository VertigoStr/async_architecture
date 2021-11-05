import enum
import sqlalchemy
from sqlalchemy.sql import func
from .users import users_table

metadata = sqlalchemy.MetaData()


class Status(str, enum.Enum):
    OPEN = 1
    IN_PROGRESS = 2
    FINISHED = 3


task_table = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(40), index=True),
    sqlalchemy.Column("description", sqlalchemy.String()),
    sqlalchemy.Column(
        "status",
        sqlalchemy.Enum(Status),
        default=Status.OPEN,
        nullable=False,
    ),
    sqlalchemy.Column(
        "creator_id", 
        sqlalchemy.ForeignKey(users_table.c.id),
    ),
    sqlalchemy.Column(
        "assignee_id", 
        sqlalchemy.ForeignKey(users_table.c.id),
    ),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime(timezone=True),
        server_default=func.now()
    ),
)


task_status_log_table = sqlalchemy.Table(
    "task_status_logs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "task_id", 
        sqlalchemy.ForeignKey("tasks.id"),
    ),
    sqlalchemy.Column(
        "actor_id", 
        sqlalchemy.ForeignKey(users_table.c.id),
    ),
    sqlalchemy.Column(
        "from_status",
        sqlalchemy.Enum(Status),
        nullable=True,
    ),
    sqlalchemy.Column(
        "to_status",
        sqlalchemy.Enum(Status),
        nullable=True,
    ),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime(timezone=True),
        server_default=func.now()
    ),
)
