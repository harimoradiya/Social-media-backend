"""create post table

Revision ID: 93433dc8980d
Revises: aecf304bb7b6
Create Date: 2022-09-29 12:22:15.434363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93433dc8980d'
down_revision = 'aecf304bb7b6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id',sa.Integer(),nullable =False, primary_key=True) ,
                    sa.Column('title',sa.String))

    pass


def downgrade():
    op.drop_table('posts')
    pass
