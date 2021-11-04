"""Added required tables

Revision ID: bf8b0853a694
Revises: 
Create Date: 2021-11-04 13:24:32.725132

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from app.utils.users import hash_password

# revision identifiers, used by Alembic.
revision = 'bf8b0853a694'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=40), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    sa.Column('role', sa.Enum('WORKER', 'ACCOUNTANT', 'ADMIN', name='role'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('expires', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_token'), 'tokens', ['token'], unique=True)
    salt = '123'
    password = hash_password('admin', salt)
    password = f'{salt}${password}'
    op.execute(
        f"INSERT INTO users VALUES (default, 'admin@admin.ru', '{password}', true, 'ADMIN')"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tokens_token'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.execute('drop type role')
    # ### end Alembic commands ###
