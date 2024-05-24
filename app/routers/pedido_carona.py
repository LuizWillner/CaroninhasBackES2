from sqlalchemy import func
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Annotated
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body

from app.database.user_orm import User
from app.database.carona_orm import Carona
from app.database.pedido_carona_orm import PedidoCarona

from app.models.router_tags import RouterTags
from app.models.user_carona_oop import UserCaronaBase
from app.models.pedido_carona_oop import (
    PedidoCaronaBase, PedidoCaronaBasePartidaDestino, PedidoCaronaCreate, 
    PedidoCaronaUpdate, PedidoCaronaExtended
)

from app.utils.pedido_carona_utils import PedidoCaronaOrderByOptions
from app.utils.db_utils import apply_limit_offset, get_db

from app.core.user_carona import add_user_carona_to_db
from app.core.authentication import get_current_active_user
from app.core.pedido_carona import (
    add_pedido_carona_to_db, 
    get_pedido_carona_by_id, 
    get_pedido_caronas, 
    update_pedido_carona_in_db, 
    delete_pedido_carona_from_db
)


router = APIRouter(prefix="/pedido-carona", tags=[RouterTags.pedido_carona])


@router.post("", response_model=PedidoCaronaExtended)
def create_pedido_carona(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    hora_partida_minima: datetime = Query(datetime.now()),
    hora_partida_maxima: datetime = Query(),
    valor_sugerido: float = Query(),
    partida_destino: PedidoCaronaBasePartidaDestino = Body(),
) -> PedidoCaronaExtended:
    pedido_carona = add_pedido_carona_to_db(
        pedido_carona_to_add=PedidoCaronaBase(
            fk_user=current_user.id,
            hora_partida_maxima=hora_partida_maxima,
            hora_partida_minima=hora_partida_minima,
            valor=valor_sugerido,
            local_partida=partida_destino.local_partida,
            local_destino=partida_destino.local_destino
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


description_search_pedidos_caronas = (
    '''
    **Importante**  \\
    - Os endereços armazenados no banco de dados são strings, e não coordenadas geográficas. Eles possuem um formato específico que segue o padrão do Google Maps.\\
    ---- Exemplo: "R. Passo da Pátria, 152-470 - São Domingos, Niterói - RJ, 24210-240"\\
    - A filtragem por _keyword_partida_ e _keyword_destino_ é feita por meio de uma busca textual, isto é, a query retornará as caronas cujo local de partida ou destino contém a palavra chave passada.\\
    ---- Exemplo: se _keyword_partida_="Ipanema", a query retornará as caronas cujo local de partida contém a palavra "Ipanema" (ex: "Ipanema, Rio de Janeiro").
    '''
)
@router.get("", response_model=list[PedidoCaronaExtended], description=description_search_pedidos_caronas)
def search_pedidos_carona(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_id: int | None = Query(None, description="ID do usuário para filtrar os pedidos feitos por um usuário. Se nada for passado, os pedidos não serão filtrados por usuário"),
    hora_minima: datetime = Query(datetime.now()-timedelta(hours=12), description="Hora mínima de partida para filtrar os pedidos. Se nada for passado, será considerada a hora atual-12h"),
    hora_maxima: datetime = Query(datetime.now()-timedelta(days=365), description="Hora máxima de partida para filtrar os pedidos. Se nada for passado, será considerada a hora atual+1ano"),
    valor_minimo: float = Query(0, description="Valor mínimo de preço do pedido de carona"),
    valor_maximo: float = Query(999999, description="Valor máximo de preço pedido de carona"),
    keyword_partida: str = Query(None, description="Palavra chave para filtrar os endereços de partida."),
    # raio_partida: ? = x,
    keyword_destino: str = Query(None, description="Palavra chave para filtrar os endereços destinos."),
    # raio_destino: ? = x
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
    if keyword_partida:
        filters.append(func.upper(PedidoCarona.local_partida).contains(keyword_partida.upper()))
    if keyword_destino: 
        filters.append(func.upper(PedidoCarona.local_destino).contains(keyword_destino.upper()))
    
    order_by_dict = PedidoCaronaOrderByOptions.get_order_by_dict()

    pedidos_caronas_query = db.query(PedidoCarona).filter(*filters).order_by(order_by_dict[order_by.value][is_crescente])
    pedidos_caronas_query = apply_limit_offset(query=pedidos_caronas_query, limit=limite, offset=deslocamento)
    
    pedidos_caronas = pedidos_caronas_query.all()
    
    return pedidos_caronas

