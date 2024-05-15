"""Tabela Carona criada

Revision ID: c67716f007d1
Revises: c89c25badffe
Create Date: 2024-05-13 12:35:04.898235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c67716f007d1'
down_revision: Union[str, None] = 'c89c25badffe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carona',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('fk_motorista', sa.Integer(), nullable=False),
    sa.Column('fk_motorista_veiculo', sa.Integer(), nullable=False),
    sa.Column('hora_partida', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['fk_motorista'], ['motorista.id_fk_user'], ),
    sa.ForeignKeyConstraint(['fk_motorista_veiculo'], ['motorista_veiculo.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_carona_fk_motorista'), 'carona', ['fk_motorista'], unique=False)
    op.create_index(op.f('ix_carona_fk_motorista_veiculo'), 'carona', ['fk_motorista_veiculo'], unique=False)
    op.create_index(op.f('ix_carona_hora_partida'), 'carona', ['hora_partida'], unique=False)
    op.create_index(op.f('ix_carona_id'), 'carona', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_carona_id'), table_name='carona')
    op.drop_index(op.f('ix_carona_hora_partida'), table_name='carona')
    op.drop_index(op.f('ix_carona_fk_motorista_veiculo'), table_name='carona')
    op.drop_index(op.f('ix_carona_fk_motorista'), table_name='carona')
    op.drop_table('carona')
    # ### end Alembic commands ###
