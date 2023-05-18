"""Remove unnecessary field in userveventbooking

Revision ID: 4fa1837236e1
Revises: 163c8cef8aec
Create Date: 2023-05-18 21:46:25.249648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fa1837236e1'
down_revision = '163c8cef8aec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usereventbooking', 'checkedIn')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('usereventbooking', sa.Column('checkedIn', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###