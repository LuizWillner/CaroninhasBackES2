import logging
from sqlalchemy import func, asc
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Annotated
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body

from app.database.user_carona_orm import UserCarona
from app.database.user_orm import User
from app.database.carona_orm import Carona
from app.database.pedido_carona_orm import PedidoCarona

from app.models.router_tags import RouterTags
from app.models.user_carona_oop import UserCaronaBase
from app.models.pedido_carona_oop import (
    PedidoCaronaBase, PedidoCaronaBasePartidaDestino, PedidoCaronaCreate, PedidoCaronaCreateWithDetail, 
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


@router.post("", response_model=PedidoCaronaCreateWithDetail)
def create_pedido_carona(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    hora_partida_minima: datetime = Query(datetime.now()),
    hora_partida_maxima: datetime = Query(),
    valor_sugerido: float = Query(),
    partida_destino: PedidoCaronaBasePartidaDestino = Body(),
    inserir_automatico: bool = Query(False, description="Indica se o sistema deve tentar inserir automaticamente o usuário em uma carona que atenda aos critérios do pedido. Se True, os params _keyword_partida_ e _keyword_destino_ devem ser fornecidos."),
    keyword_partida: str = Query(None, description="Caso _inserir_automatico_=True, o usuário será adicionado numa carona que contenha essa palavra chave no endereço de partida."),
    keyword_destino: str = Query(None, description="Caso _inserir_automatico_=True, o usuário será adicionado numa carona que contenha essa palavra chave no endereço de partida."),
) -> PedidoCaronaCreateWithDetail:
    if inserir_automatico and not (keyword_partida and keyword_destino):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se inserir_automatico=True, os params keyword_partida e keyword_destino devem ser fornecidos."
        )
        
    db_pedido_carona = add_pedido_carona_to_db(
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
    
    try:
        if inserir_automatico:
            vagas_subquery = (
                db.query(UserCarona.fk_carona, func.count(UserCarona.fk_user).label("num_passageiros"))
                .group_by(UserCarona.fk_carona)
                .subquery()
            )
            carona_escolhida = (
                db.query(Carona)
                .outerjoin(vagas_subquery, Carona.id == vagas_subquery.c.fk_carona)
                .filter(
                    Carona.hora_partida >= hora_partida_minima,
                    Carona.hora_partida <= hora_partida_maxima,
                    func.upper(Carona.local_partida).contains(keyword_partida.upper()),
                    func.upper(Carona.local_destino).contains(keyword_destino.upper()),
                    Carona.valor <= valor_sugerido,
                    Carona.vagas - func.coalesce(vagas_subquery.c.num_passageiros, 0) >= 1  # filra as caronas que possuem pelo menos 1 vaga disponível
                )
                .order_by(asc(Carona.valor))
                .first()
            )

            pedido_carona_model = PedidoCaronaCreate.from_orm(db_pedido_carona)
            response_pedido_carona = PedidoCaronaCreateWithDetail(**pedido_carona_model.model_dump(), sucesso_insercao=False)
            if carona_escolhida:
                db_user_carona = add_user_carona_to_db(
                    user_carona_to_add=UserCaronaBase(
                        fk_user=current_user.id,
                        fk_carona=carona_escolhida.id
                    ),
                    db_carona=carona_escolhida,
                    db=db
                )
                if db_user_carona:
                    response_pedido_carona.sucesso_insercao = True
                    
    except Exception as e:
        db.rollback()
        db.delete(db_pedido_carona)
        db.commit()
        logging.error(f"Erro ao tentar inserir automaticamente o usuário numa carona: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao tentar inserir automaticamente o usuário numa carona: {e}"
        )

    return response_pedido_carona



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

