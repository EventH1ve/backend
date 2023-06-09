"""remove admin id  from event table 

Revision ID: 0c8c14d7ac5c
Revises: 459400fcc18b
Create Date: 2023-05-16 20:34:44.053808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c8c14d7ac5c'
down_revision = '459400fcc18b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('event_adminid_fkey', 'event', type_='foreignkey')
    op.drop_column('event', 'adminid')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('adminid', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('event_adminid_fkey', 'event', 'admin', ['adminid'], ['id'])
    # ### end Alembic commands ###
