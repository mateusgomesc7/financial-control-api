"""initial database

Revision ID: 6a67455a92ee
Revises: 
Create Date: 2024-12-15 10:23:02.219236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a67455a92ee'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('month',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('member',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('id_user_fk', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['id_user_fk'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_month',
    sa.Column('id_user_fk', sa.Integer(), nullable=False),
    sa.Column('id_month_fk', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_month_fk'], ['month.id'], ),
    sa.ForeignKeyConstraint(['id_user_fk'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id_user_fk', 'id_month_fk')
    )
    op.create_table('essential_expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('id_member_fk', sa.Integer(), nullable=True),
    sa.Column('expected', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['id_member_fk'], ['member.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('income',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('id_member_fk', sa.Integer(), nullable=True),
    sa.Column('amount', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['id_member_fk'], ['member.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('non_essential_expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('id_member_fk', sa.Integer(), nullable=True),
    sa.Column('expected', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['id_member_fk'], ['member.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_essential_expense',
    sa.Column('id_user_fk', sa.Integer(), nullable=False),
    sa.Column('id_essential_expense_fk', sa.Integer(), nullable=False),
    sa.Column('id_month_fk', sa.Integer(), nullable=False),
    sa.Column('expected', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('paid', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['id_essential_expense_fk'], ['essential_expense.id'], ),
    sa.ForeignKeyConstraint(['id_month_fk'], ['month.id'], ),
    sa.ForeignKeyConstraint(['id_user_fk'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id_user_fk', 'id_essential_expense_fk')
    )
    op.create_table('user_income',
    sa.Column('id_user_fk', sa.Integer(), nullable=False),
    sa.Column('id_income_fk', sa.Integer(), nullable=False),
    sa.Column('id_month_fk', sa.Integer(), nullable=False),
    sa.Column('amount', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['id_income_fk'], ['income.id'], ),
    sa.ForeignKeyConstraint(['id_month_fk'], ['month.id'], ),
    sa.ForeignKeyConstraint(['id_user_fk'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id_user_fk', 'id_income_fk')
    )
    op.create_table('user_non_essential_expense',
    sa.Column('id_user_fk', sa.Integer(), nullable=False),
    sa.Column('id_non_essential_expense_fk', sa.Integer(), nullable=False),
    sa.Column('id_month_fk', sa.Integer(), nullable=False),
    sa.Column('expected', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('paid', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['id_month_fk'], ['month.id'], ),
    sa.ForeignKeyConstraint(['id_non_essential_expense_fk'], ['non_essential_expense.id'], ),
    sa.ForeignKeyConstraint(['id_user_fk'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id_user_fk', 'id_non_essential_expense_fk')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_non_essential_expense')
    op.drop_table('user_income')
    op.drop_table('user_essential_expense')
    op.drop_table('non_essential_expense')
    op.drop_table('income')
    op.drop_table('essential_expense')
    op.drop_table('user_month')
    op.drop_table('member')
    op.drop_table('user')
    op.drop_table('month')
    # ### end Alembic commands ###
