"""“Third-commit”

Revision ID: 34ecea15989c
Revises: 7b9ae9608f47
Create Date: 2023-04-27 04:17:42.650354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34ecea15989c'
down_revision = '7b9ae9608f47'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('venueid', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'event', 'venue', ['venueid'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event', type_='foreignkey')
    op.drop_column('event', 'venueid')
    # ### end Alembic commands ###
