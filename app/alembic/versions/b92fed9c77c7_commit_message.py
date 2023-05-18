"""Commit Message

Revision ID: b92fed9c77c7
Revises: 10cf619a331a
Create Date: 2023-05-14 19:42:38.198354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b92fed9c77c7'
down_revision = '10cf619a331a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('adminId', sa.Integer(), nullable=True))
    op.drop_constraint('event_admin_id_fkey', 'event', type_='foreignkey')
    op.create_foreign_key(None, 'event', 'users', ['adminId'], ['id'])
    op.drop_column('event', 'admin_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('admin_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.create_foreign_key('event_admin_id_fkey', 'event', 'users', ['admin_id'], ['id'])
    op.drop_column('event', 'adminId')
    # ### end Alembic commands ###