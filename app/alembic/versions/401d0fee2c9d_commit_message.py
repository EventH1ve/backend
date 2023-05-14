"""Commit Message

Revision ID: 401d0fee2c9d
Revises: 464942aca772
Create Date: 2023-05-14 19:45:40.802593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '401d0fee2c9d'
down_revision = '464942aca772'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('admin_id', sa.Integer(), nullable=True))
    op.drop_constraint('event_adminId_fkey', 'event', type_='foreignkey')
    op.create_foreign_key(None, 'event', 'users', ['admin_id'], ['id'])
    op.drop_column('event', 'adminId')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('adminId', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.create_foreign_key('event_adminId_fkey', 'event', 'users', ['adminId'], ['id'])
    op.drop_column('event', 'admin_id')
    # ### end Alembic commands ###
