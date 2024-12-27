"""Create base schema

Revision ID: cfa9f38a6647
Revises: 
Create Date: 2024-12-27 01:39:35.500881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfa9f38a6647'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sudoku',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('difficulty', sa.Integer(), nullable=False),
    sa.Column('puzzle_data', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('puzzle_data')
    )
    op.create_index(op.f('ix_sudoku_id'), 'sudoku', ['id'], unique=False)
    op.create_table('sudoku_registry',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('sudoku_id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('solving_time', sa.Float(), nullable=False),
    sa.Column('is_applicable', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sudoku_registry_id'), 'sudoku_registry', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('firebase_id', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('firebase_id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_sudoku_registry_id'), table_name='sudoku_registry')
    op.drop_table('sudoku_registry')
    op.drop_index(op.f('ix_sudoku_id'), table_name='sudoku')
    op.drop_table('sudoku')
    # ### end Alembic commands ###
