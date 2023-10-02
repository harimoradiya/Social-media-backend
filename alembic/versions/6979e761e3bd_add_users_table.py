"""add users table

Revision ID: 6979e761e3bd
Revises: d2a37cfd5369
Create Date: 2022-09-29 12:43:14.824986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6979e761e3bd'
down_revision = 'd2a37cfd5369'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id',sa.Integer(),nullable = False),
                    sa.Column('email',sa.String(),nullable = False),
                    sa.Column('password',sa.String(),nullable= False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')

                    
                    
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
