"""add new column

Revision ID: d2a37cfd5369
Revises: 93433dc8980d
Create Date: 2022-09-29 12:38:04.366583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2a37cfd5369'
down_revision = '93433dc8980d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
