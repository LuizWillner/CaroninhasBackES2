"""driver_vehicle recriada

Revision ID: 0b087816ac5d
Revises: 1a513b54c162
Create Date: 2024-05-13 10:18:37.436487

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b087816ac5d'
down_revision: Union[str, None] = '1a513b54c162'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('driver_vehicle',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fk_driver', sa.Integer(), nullable=False),
    sa.Column('fk_vehicle', sa.Integer(), nullable=False),
    sa.Column('plate', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['fk_driver'], ['driver.id_fk_user'], ),
    sa.ForeignKeyConstraint(['fk_vehicle'], ['vehicle.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_driver_vehicle_fk_driver'), 'driver_vehicle', ['fk_driver'], unique=False)
    op.create_index(op.f('ix_driver_vehicle_fk_vehicle'), 'driver_vehicle', ['fk_vehicle'], unique=False)
    op.create_index(op.f('ix_driver_vehicle_id'), 'driver_vehicle', ['id'], unique=False)
    op.create_index(op.f('ix_driver_vehicle_plate'), 'driver_vehicle', ['plate'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_driver_vehicle_plate'), table_name='driver_vehicle')
    op.drop_index(op.f('ix_driver_vehicle_id'), table_name='driver_vehicle')
    op.drop_index(op.f('ix_driver_vehicle_fk_vehicle'), table_name='driver_vehicle')
    op.drop_index(op.f('ix_driver_vehicle_fk_driver'), table_name='driver_vehicle')
    op.drop_table('driver_vehicle')
    # ### end Alembic commands ###
