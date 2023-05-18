"""Fix missing revision

Revision ID: 13abbf30cd2a
Revises: 6b20497da0ba
Create Date: 2023-05-15 14:36:51.656765

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '13abbf30cd2a'
down_revision = '6b20497da0ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickettype', sa.Column('seats', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True))
    op.add_column('tickettype', sa.Column('limit', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('tickettype', sa.Column('seated', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('event', sa.Column('admin_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('event', sa.Column('datetime', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.create_foreign_key('event_admin_id_fkey', 'event', 'users', ['admin_id'], ['id'])
    op.drop_index(op.f('ix_eventseatlayout_id'), table_name='eventseatlayout')
    op.drop_table('eventseatlayout')
    # ### end Alembic commands ###