"""revert changes

Revision ID: a3aa33dc5b80
Revises: d24b9ace89d3
Create Date: 2023-05-16 16:05:31.818072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3aa33dc5b80'
down_revision = 'd24b9ace89d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'event', 'admin', ['adminid'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event', type_='foreignkey')
    # ### end Alembic commands ###
