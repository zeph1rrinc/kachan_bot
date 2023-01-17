"""init tables

Revision ID: 20d8c5cbed2f
Revises: 
Create Date: 2023-01-16 02:14:07.531842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20d8c5cbed2f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(), nullable=False),
    sa.Column('right_answer', sa.String(), nullable=False),
    sa.Column('wrong_answer1', sa.String(), nullable=False),
    sa.Column('wrong_answer2', sa.String(), nullable=False),
    sa.Column('wrong_answer3', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('participants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('current_question', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['current_question'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('participants')
    op.drop_table('questions')
    # ### end Alembic commands ###
