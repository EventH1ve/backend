"""added changes

Revision ID: 6a496e7398ab
Revises: 08711ce48372
Create Date: 2023-05-15 16:58:03.497497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a496e7398ab'
down_revision = '08711ce48372'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ticket', 'checked')
    op.add_column('usereventbooking', sa.Column('checkedIn', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usereventbooking', 'checkedIn')
    op.add_column('ticket', sa.Column('checked', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
