"""added changes to event model

Revision ID: d24b9ace89d3
Revises: d6e5a8907ec6
Create Date: 2023-05-16 15:56:40.735551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd24b9ace89d3'
down_revision = 'd6e5a8907ec6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('event_adminid_fkey', 'event', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('event_adminid_fkey', 'event', 'admin', ['adminid'], ['id'])
    # ### end Alembic commands ###
