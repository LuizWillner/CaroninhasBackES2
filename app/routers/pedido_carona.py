from app.core.user_carona import add_user_carona_to_db
from app.database.carona_orm import Carona
from app.database.user_orm import User
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Annotated
from sqlalchemy.orm import Session
from app.database.pedido_carona_orm import PedidoCarona
from pydantic import BaseModel

from datetime import datetime, timedelta
from app.models.pedido_carona_oop import PedidoCaronaBase, PedidoCaronaCreate, PedidoCaronaUpdate, PedidoCaronaExtended
from app.models.user_carona_oop import UserCaronaBase
from app.utils.db_utils import apply_limit_offset, get_db
from app.core.pedido_carona import (
    add_pedido_carona_to_db, 
    get_pedido_carona_by_id, 
    get_pedido_caronas, 
    update_pedido_carona_in_db, 
    delete_pedido_carona_from_db
)
from app.core.authentication import get_current_active_user
from app.models.router_tags import RouterTags
from app.utils.pedido_carona_utils import PedidoCaronaOrderByOptions


router = APIRouter(prefix="/pedido-carona", tags=[RouterTags.pedido_carona])


@router.post("", response_model=PedidoCaronaExtended)
def create_pedido_carona(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    hora_partida_minima: datetime = Query(datetime.now()),
    hora_partida_maxima: datetime = Query(),
    valor_sugerido: float = Query()
    # coord_partida: str,
    # coord_destino: str,
) -> PedidoCaronaExtended:
    pedido_carona = add_pedido_carona_to_db(
        pedido_carona_to_add=PedidoCaronaBase(
            fk_user=current_user.id,
            hora_partida_maxima=hora_partida_maxima,
            hora_partida_minima=hora_partida_minima,
            valor=valor_sugerido,
            # coord_partida=coord_partida,
            # coord_destino=coord_destino
        ),
        db=db
    )


    caronas_query = (
        db.query(Carona)
        .filter(Carona.hora_partida >= hora_partida_minima, Carona.hora_partida <= hora_partida_maxima)
        .all()
    )

    carona_escolhida = None
    preco_mais_barato = float('inf')

    for carona in caronas_query:
        if carona.valor < valor_sugerido:
            if carona.valor < preco_mais_barato:
                carona_escolhida = carona
                preco_mais_barato = carona.valor

    if carona_escolhida:
        add_user_carona_to_db(
            user_carona_to_add=UserCaronaBase(
                fk_user=current_user.id,
                fk_carona=carona_escolhida.id
            ),
            db=db
        )

    return pedido_carona



@router.get("/{pedido_carona_id}", response_model=PedidoCaronaExtended)
def read_pedido_carona(
    pedido_carona_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)]  # precisa estar logado para usar o endpoint
) -> PedidoCaronaExtended:
    pedido_carona = get_pedido_carona_by_id(db, pedido_carona_id)
    if not pedido_carona:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido de Carona não encontrado.")
    return pedido_carona


@router.put("/{pedido_carona_id}", response_model=PedidoCaronaExtended)
def update_pedido_carona(
    pedido_carona_id: int,
    pedido_carona: PedidoCaronaUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)]  # precisa estar logado para usar o endpoint
) -> PedidoCaronaExtended:
    return update_pedido_carona_in_db(db=db, pedido_carona_id=pedido_carona_id, pedido_carona=pedido_carona)


@router.delete("/{pedido_carona_id}", response_model=str)
def delete_pedido_carona(
    pedido_carona_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)]  # precisa estar logado para usar o endpoint
) -> str:
    return delete_pedido_carona_from_db(db=db, pedido_carona_id=pedido_carona_id)


@router.get("", response_model=list[PedidoCaronaExtended])
def search_pedidos_carona(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_id: int | None = Query(None, description="ID do usuário para filtrar os pedidos feitos por um usuário. Se nada for passado, os pedidos não serão filtrados por usuário"),
    hora_minima: datetime = Query(datetime.now()-timedelta(hours=12), description="Hora mínima de partida para filtrar os pedidos. Se nada for passado, será considerada a hora atual-12h"),
    hora_maxima: datetime = Query(datetime.now()-timedelta(days=365), description="Hora máxima de partida para filtrar os pedidos. Se nada for passado, será considerada a hora atual+1ano"),
    valor_minimo: float = Query(0, description="Valor mínimo de preço do pedido de carona"),
    valor_maximo: float = Query(999999, description="Valor máximo de preço pedido de carona"),
    # local_partida: ?? = Query(),
    # raio_partida: ?? = Query(),
    # local_destino: ?? = Query(),
    order_by: PedidoCaronaOrderByOptions = Query(PedidoCaronaOrderByOptions.hora_minima_partida, description="Como a query deve ser ordenada."),
    is_crescente: bool = Query(True, description="Indica se a ordenação deve ser feita em ordem crescente."),
    limite: int = Query(10, description="Limite de pedidos de carona retornados pela query"),
    deslocamento: int = Query(0, description="Deslocamento (offset) da query. Os params _deslocamento_=1 e _limit_=10, por exemplo, indicam que a query retornará os pedidos de 11 a 20, pulando os pedidos de 1 a 10."),
) -> list[PedidoCaronaExtended]:
    
    if hora_minima > hora_maxima:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="hora_minima não pode ser maior que hora_maxima"
        )
    if valor_minimo > valor_maximo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="valor_minimo não pode ser maior que hvalor_maximo"
        )
    
    filters = []

    if user_id is not None:
        filters.append(PedidoCarona.fk_user == user_id)
    if hora_minima:
        filters.append(PedidoCarona.hora_partida_minima >= hora_minima)
    if hora_maxima:
        filters.append(PedidoCarona.hora_partida_maxima <= hora_maxima)
    if valor_minimo:
        filters.append(PedidoCarona.valor >= valor_minimo)
    if valor_maximo:
        filters.append(PedidoCarona.valor <= valor_maximo)
    # if local_partida:
    #     # filtra pelo local_partida com base no raio_partida
    # if local_destino: 
    #     # filtra pelo local_destino com base no raio_destino
    
    order_by_dict = PedidoCaronaOrderByOptions.get_order_by_dict()

    pedidos_caronas_query = db.query(PedidoCarona).filter(*filters).order_by(order_by_dict[order_by.value][is_crescente])
    pedidos_caronas_query = apply_limit_offset(query=pedidos_caronas_query, limit=limite, offset=deslocamento)
    
    pedidos_caronas = pedidos_caronas_query.all()
    
    return pedidos_caronas

