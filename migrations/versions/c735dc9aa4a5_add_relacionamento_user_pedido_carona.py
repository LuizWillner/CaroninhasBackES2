"""ADD_Relacionamento_User_Pedido_Carona

Revision ID: c735dc9aa4a5
Revises: 6fa453bb0886
Create Date: 2024-05-20 07:07:53.160307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c735dc9aa4a5'
down_revision: Union[str, None] = '6fa453bb0886'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_pedido_carona_id', 'pedido_carona', ['id'], unique=False)
    op.drop_index('ix_pedido_carona_fk_user', table_name='pedido_carona')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pedido_carona',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('fk_user', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('hora_partida_minima', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('hora_partida_maxima', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('coord_partida', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('coord_destino', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['fk_user'], ['user.id'], name='pedido_carona_fk_user_fkey'),
    sa.PrimaryKeyConstraint('id', name='pedido_carona_pkey'),
    )
    op.create_table('user_carona',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('fk_carona', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('fk_user', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['fk_carona'], ['carona.id'], name='user_carona_fk_carona_fkey'),
    sa.ForeignKeyConstraint(['fk_user'], ['user.id'], name='user_carona_fk_user_fkey'),
    sa.PrimaryKeyConstraint('id', name='user_carona_pkey'),
    sa.UniqueConstraint('fk_carona', 'fk_user', name='user_carona_fk_carona_fk_user_key')
    )
    op.create_index('ix_user_carona_id', 'user_carona', ['id'], unique=False)
    op.create_index('ix_user_carona_fk_user', 'user_carona', ['fk_user'], unique=False)
    op.create_index('ix_user_carona_fk_carona', 'user_carona', ['fk_carona'], unique=False)
    # ### end Alembic commands ###
