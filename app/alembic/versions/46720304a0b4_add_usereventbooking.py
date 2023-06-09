"""Add UserEventBooking

Revision ID: 46720304a0b4
Revises: bec0cce7753a
Create Date: 2023-05-10 21:57:51.716651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46720304a0b4'
down_revision = 'bec0cce7753a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usereventbooking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('eventid', sa.Integer(), nullable=True),
    sa.Column('bookingdate', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('transactionid', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['eventid'], ['event.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usereventbooking_id'), 'usereventbooking', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_usereventbooking_id'), table_name='usereventbooking')
    op.drop_table('usereventbooking')
    # ### end Alembic commands ###
