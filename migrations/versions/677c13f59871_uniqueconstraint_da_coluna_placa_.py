"""UniqueConstraint da coluna placa removido

Revision ID: 677c13f59871
Revises: 4358d06bd4ef
Create Date: 2024-05-22 00:58:59.282121

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '677c13f59871'
down_revision: Union[str, None] = '4358d06bd4ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_motorista_veiculo_placa', table_name='motorista_veiculo')
    op.create_index(op.f('ix_motorista_veiculo_placa'), 'motorista_veiculo', ['placa'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_motorista_veiculo_placa'), table_name='motorista_veiculo')
    op.create_index('ix_motorista_veiculo_placa', 'motorista_veiculo', ['placa'], unique=True)
    # ### end Alembic commands ###