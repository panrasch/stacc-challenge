"""initial migration

Revision ID: 4281795e4adc
Revises: 
Create Date: 2023-10-10 21:06:54.767739

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4281795e4adc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('password_hash',mysql.VARCHAR(255), nullable=False))

def downgrade():
    op.drop_column('users','password_hash')
