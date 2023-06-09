"""Change membership to membershipend in admin table

Revision ID: 44ff3b60f7fc
Revises: d842253b87f2
Create Date: 2023-05-18 20:58:41.792649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44ff3b60f7fc'
down_revision = 'd842253b87f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin', sa.Column('membershipend', sa.DateTime(), nullable=True))
    op.drop_column('admin', 'membership')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin', sa.Column('membership', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('admin', 'membershipend')
    # ### end Alembic commands ###
