"""add user table

Revision ID: d5ccb47fe8e7
Revises: c71271f7be47
Create Date: 2024-11-04 11:19:33.525849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'd5ccb47fe8e7'
down_revision: Union[str, None] = 'c71271f7be47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False),
        sa.UniqueConstraint('email'),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() :
    op.drop_table('users')
    pass
