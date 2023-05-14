"""Change UserEventBooking id to eid

Revision ID: c62076496eae
Revises: d37ca7bf94ff
Create Date: 2023-05-14 23:46:56.001161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c62076496eae'
down_revision = 'd37ca7bf94ff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usereventbooking',
    sa.Column('eid', sa.UUID(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('eventid', sa.Integer(), nullable=True),
    sa.Column('bookingdate', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('transactionid', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['eventid'], ['event.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('eid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usereventbooking')
    # ### end Alembic commands ###