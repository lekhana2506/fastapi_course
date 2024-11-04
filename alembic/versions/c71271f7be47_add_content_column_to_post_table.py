"""add content column to post table

Revision ID: c71271f7be47
Revises: 89718e4fca46
Create Date: 2024-11-04 11:14:01.596643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c71271f7be47'
down_revision: Union[str, None] = '89718e4fca46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))


def downgrade():
    op.drop_column('posts','content')
    pass
