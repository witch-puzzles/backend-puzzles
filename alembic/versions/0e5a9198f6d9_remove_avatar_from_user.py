"""Remove avatar from user

Revision ID: 0e5a9198f6d9
Revises: 9f950136d0a5
Create Date: 2025-01-03 10:36:07.273376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e5a9198f6d9'
down_revision: Union[str, None] = '9f950136d0a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
