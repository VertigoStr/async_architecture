import enum
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

metadata = sqlalchemy.MetaData()


class Role(str, enum.Enum):
    WORKER = 1
    ACCOUNTANT = 2
    ADMIN = 3


users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(40), unique=True, index=True),
    sqlalchemy.Column(
        "role",
        sqlalchemy.Enum(Role),
        default=Role.WORKER,
        nullable=False,
    ),
    sqlalchemy.Column(
        "is_deleted",
        sqlalchemy.Boolean(),
        server_default=sqlalchemy.sql.expression.false(),
        nullable=False,
    ),
    sqlalchemy.Column(
        "token",
        UUID(as_uuid=False),
        server_default=sqlalchemy.text("uuid_generate_v4()"),
        unique=True,
        nullable=False,
        index=True,
    ),
    sqlalchemy.Column("expires", sqlalchemy.DateTime()),
)
