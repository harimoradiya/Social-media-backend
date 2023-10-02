"""foreign  key for

Revision ID: 11339344680f
Revises: 6979e761e3bd
Create Date: 2022-09-29 12:54:14.272979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11339344680f'
down_revision = '6979e761e3bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable = False))
    op.create_foreign_key('post_user_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['users'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk',table_name='posts')
    op.drop_column('post','owner_id')
    pass
