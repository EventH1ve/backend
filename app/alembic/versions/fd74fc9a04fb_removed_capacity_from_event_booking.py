"""removed capacity from event-booking

Revision ID: fd74fc9a04fb
Revises: cf87f784079a
Create Date: 2023-05-17 00:13:46.352489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd74fc9a04fb'
down_revision = 'cf87f784079a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usereventbooking', 'capacity')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usereventbooking', sa.Column('capacity', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###