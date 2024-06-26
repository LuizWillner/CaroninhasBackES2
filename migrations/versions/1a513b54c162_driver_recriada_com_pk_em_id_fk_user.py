"""driver recriada com pk em id_fk_user

Revision ID: 1a513b54c162
Revises: 2548c731dcf5
Create Date: 2024-05-13 10:16:21.142973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a513b54c162'
down_revision: Union[str, None] = '2548c731dcf5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('driver',
    sa.Column('id_fk_user', sa.Integer(), nullable=False),
    sa.Column('license', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['id_fk_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id_fk_user')
    )
    op.create_index(op.f('ix_driver_id_fk_user'), 'driver', ['id_fk_user'], unique=True)
    op.create_index(op.f('ix_driver_license'), 'driver', ['license'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_driver_license'), table_name='driver')
    op.drop_index(op.f('ix_driver_id_fk_user'), table_name='driver')
    op.drop_table('driver')
    # ### end Alembic commands ###
