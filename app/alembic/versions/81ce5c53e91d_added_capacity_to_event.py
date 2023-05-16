"""added capacity to event

Revision ID: 81ce5c53e91d
Revises: 5aa723971c26
Create Date: 2023-05-16 23:48:01.642302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81ce5c53e91d'
down_revision = '5aa723971c26'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usereventbooking', sa.Column('capacity', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usereventbooking', 'capacity')
    # ### end Alembic commands ###
