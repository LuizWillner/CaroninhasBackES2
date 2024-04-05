"""Create Driver, DriverVehicle and Vehicle tables

Revision ID: b9ddf16fc7d0
Revises: 85e8046a33a9
Create Date: 2024-04-05 13:51:25.044341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9ddf16fc7d0'
down_revision: Union[str, None] = '85e8046a33a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicle',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('brand', sa.String(), nullable=False),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('color', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type', 'brand', 'model', 'color')
    )
    op.create_index(op.f('ix_vehicle_brand'), 'vehicle', ['brand'], unique=False)
    op.create_index(op.f('ix_vehicle_id'), 'vehicle', ['id'], unique=False)
    op.create_index(op.f('ix_vehicle_model'), 'vehicle', ['model'], unique=False)
    op.create_index(op.f('ix_vehicle_type'), 'vehicle', ['type'], unique=False)
    op.create_table('driver',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fk_user', sa.Integer(), nullable=True),
    sa.Column('license', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['fk_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_driver_fk_user'), 'driver', ['fk_user'], unique=True)
    op.create_index(op.f('ix_driver_id'), 'driver', ['id'], unique=False)
    op.create_index(op.f('ix_driver_license'), 'driver', ['license'], unique=True)
    op.create_table('driver_vehicle',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fk_driver', sa.Integer(), nullable=True),
    sa.Column('fk_vehicle', sa.Integer(), nullable=True),
    sa.Column('plate', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['fk_driver'], ['driver.id'], ),
    sa.ForeignKeyConstraint(['fk_vehicle'], ['vehicle.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_driver_vehicle_fk_driver'), 'driver_vehicle', ['fk_driver'], unique=False)
    op.create_index(op.f('ix_driver_vehicle_fk_vehicle'), 'driver_vehicle', ['fk_vehicle'], unique=False)
    op.create_index(op.f('ix_driver_vehicle_id'), 'driver_vehicle', ['id'], unique=False)
    op.create_index(op.f('ix_driver_vehicle_plate'), 'driver_vehicle', ['plate'], unique=True)
    op.add_column('user', sa.Column('hashed_password', sa.String(), nullable=False))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('user', 'hashed_password')
    op.drop_index(op.f('ix_driver_vehicle_plate'), table_name='driver_vehicle')
    op.drop_index(op.f('ix_driver_vehicle_id'), table_name='driver_vehicle')
    op.drop_index(op.f('ix_driver_vehicle_fk_vehicle'), table_name='driver_vehicle')
    op.drop_index(op.f('ix_driver_vehicle_fk_driver'), table_name='driver_vehicle')
    op.drop_table('driver_vehicle')
    op.drop_index(op.f('ix_driver_license'), table_name='driver')
    op.drop_index(op.f('ix_driver_id'), table_name='driver')
    op.drop_index(op.f('ix_driver_fk_user'), table_name='driver')
    op.drop_table('driver')
    op.drop_index(op.f('ix_vehicle_type'), table_name='vehicle')
    op.drop_index(op.f('ix_vehicle_model'), table_name='vehicle')
    op.drop_index(op.f('ix_vehicle_id'), table_name='vehicle')
    op.drop_index(op.f('ix_vehicle_brand'), table_name='vehicle')
    op.drop_table('vehicle')
    # ### end Alembic commands ###