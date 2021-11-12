import enum
import sqlalchemy
from sqlalchemy.sql import func
from .users import users_table

metadata = sqlalchemy.MetaData()


task_price_table = sqlalchemy.Table(
    "task_price",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "task_id", 
        sqlalchemy.Integer,
    ),
    sqlalchemy.Column(
        "price",
        sqlalchemy.DECIMAL,
        default=0
    ),
    sqlalchemy.Column(
        "updated_at",
        sqlalchemy.DateTime(timezone=True),
        server_default=func.now()
    ),
)


class ActionType(str, enum.Enum):
    ADD = 1
    DEBIT = 2


task_balance_log_table = sqlalchemy.Table(
    "task_balance_log",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "task_id",
        sqlalchemy.Integer,
    ),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey(users_table.c.id),
    ),
    sqlalchemy.Column(
        "price",
        sqlalchemy.DECIMAL,
        default=0
    ),
    sqlalchemy.Column(
        "action_type",
        sqlalchemy.Enum(ActionType),
        default=ActionType.ADD,
        nullable=False,
    ),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime(timezone=True),
        server_default=func.now()
    ),
)
