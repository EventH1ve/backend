"""Commit Message

Revision ID: 1dfb0ce9d260
Revises: d282261c92f3
Create Date: 2023-05-14 13:48:23.282275

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1dfb0ce9d260'
down_revision = 'd282261c92f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('datetime', sa.DateTime(), nullable=True))
    op.drop_column('event', 'date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('event', 'datetime')
    # ### end Alembic commands ###
