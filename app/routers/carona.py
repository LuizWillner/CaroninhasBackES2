from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.authentication import get_current_active_user
from app.database.carona_orm import Carona
from app.database.pedido_carona_orm import PedidoCarona
from app.database.user_carona_orm import UserCarona
from app.database.user_orm import Motorista, User
from app.database.veiculo_orm import MotoristaVeiculo

from app.models.carona_oop import CaronaBase, CaronaBasePartidaDestino, CaronaExtended, CaronaUpdate, CaronaUpdatePartidaDestino

from app.utils.db_utils import apply_limit_offset, get_db
from app.utils.carona_utils import CaronaOrderByOptions

from app.core.carona import add_carona_to_db, get_carona_by_id, remove_carona_from_db, update_carona_in_db
from app.core.motorista import get_current_active_motorista
from app.core.veiculo import get_motorista_veiculo_of_user
from app.models.router_tags import RouterTags


router = APIRouter(prefix="/carona", tags=[RouterTags.carona])


@router.post("", response_model=CaronaExtended)
def create_carona(
    motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    motorista_veiculo: Annotated[MotoristaVeiculo, Depends(get_motorista_veiculo_of_user)],
    veiculo_id: int,
    hora_de_partida: datetime,
    preco_carona: float,
    partida_destino: CaronaBasePartidaDestino,
    db: Annotated[Session, Depends(get_db)]
)-> CaronaExtended:
    '''
    Cria uma nova carona no sistema.

    Parâmetros:
    - _veiculo_id_: O ID do veículo que pertence ao motorista.
    - _hora_de_partida_: A hora de partida da carona.
    - _preco_carona_: O preço da carona.
    
    Body:
    - _local_partida_: O local de partida da carona.
    - _local_destino_: O local de destino da carona.
    - **IMPORTANTE**: Os endereços armazenados no banco de dados são strings, e não coordenadas geográficas. **Siga SEMPRE o padrão de endereço do Google Maps** (ex: R. Passo da Pátria, 152-470 - São Domingos, Niterói - RJ, 24210-240)

    Retorna:
    - A carona criada.

    Lança:
    - HTTPException com status code 404 (not found) se o veículo do motorista atual não for encontrado.
    - HTTPException com status code 500 (internal server error) se houver um erro na hora de adicionar a carona no banco.
    '''
    
    if not motorista_veiculo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle of current user with id {veiculo_id} not found.")
    carona = add_carona_to_db(
        carona_to_add=CaronaBase(
            fk_motorista=motorista.id_fk_user,
            fk_motorista_veiculo=motorista_veiculo.id,
            hora_partida= hora_de_partida,
            valor=preco_carona,
            local_partida=partida_destino.local_partida,
            local_destino=partida_destino.local_destino,
        ),
        db=db
    )
    return carona


description_search_caronas = (
    '''
    **Importante**  \\
    - Os endereços armazenados no banco de dados são strings, e não coordenadas geográficas. Eles possuem um formato específico que segue o padrão do Google Maps.\\
    ---- Exemplo: "R. Passo da Pátria, 152-470 - São Domingos, Niterói - RJ, 24210-240"\\
    - A filtragem por _keyword_partida_ e _keyword_destino_ é feita por meio de uma busca textual, isto é, a query retornará as caronas cujo local de partida ou destino contém a palavra chave passada.\\
    ---- Exemplo: se _keyword_partida_="Ipanema", a query retornará as caronas cujo local de partida contém a palavra "Ipanema" (ex: "Ipanema, Rio de Janeiro").
    '''
)
@router.get("", response_model=list[CaronaExtended], description=description_search_caronas)
def search_caronas(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],  # precisa estar logado para usar o endpoint
    motorista_id: int | None = Query(None, description="ID do motorista para filtrar as caronas de um motorista. Se nada for passado, as caronas não serão filtradas por motorista"),
    hora_minima: datetime = Query(datetime.now(), description="Hora mínima de partida da carona. Se nada for passado, será considerada a hora atual"),
    hora_maxima: datetime = Query(datetime.now()+timedelta(days=365), description="Hora máxima de partida da carona. Se nada for passado, será considerada a hora atual+1ano"),
    valor_minimo: float = Query(0, description="Valor mínimo de preço da carona"),
    valor_maximo: float = Query(999999, description="Valor máximo de preço da carona"),
    keyword_partida: str = Query(None, description="Palavra chave para filtrar os endereços de partida."),
    # raio_partida: ? = x,
    keyword_destino: str = Query(None, description="Palavra chave para filtrar os endereços destinos."),
    # raio_destino: ? = x
    order_by: CaronaOrderByOptions = Query(CaronaOrderByOptions.hora_partida, description="Como a query deve ser ordenada."),
    is_crescente: bool = Query(True, description="Indica se a ordenação deve ser feita em ordem crescente."),
    limite: int = Query(10, description="Limite de caronas retornadas pela query"),
    deslocamento: int = Query(0, description="Deslocamento (offset) da query. Os params _deslocamento_=1 e _limit_=10, por exemplo, indicam que a query retornará as caronas de 11 a 20, pulando as caronas de 1 a 10."),
) -> list[CaronaExtended]:
    filters = []

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

    if motorista_id is not None:
        filters.append(Carona.fk_motorista == motorista_id)
    if hora_minima:
        filters.append(Carona.hora_partida >= hora_minima)
    if hora_maxima:
        filters.append(Carona.hora_partida <= hora_maxima)
    if valor_minimo:
        filters.append(Carona.valor >= valor_minimo)
    if valor_maximo:
        filters.append(Carona.valor <= valor_maximo)
    if keyword_partida:
        filters.append(func.upper(Carona.local_partida).contains(keyword_partida.upper()))
    if keyword_destino: 
        filters.append(func.upper(Carona.local_destino).contains(keyword_destino.upper()))

    order_by_dict = CaronaOrderByOptions.get_order_by_dict()
    
    caronas_query = db.query(Carona).filter(*filters).order_by(order_by_dict[order_by.value][is_crescente])
    caronas_query = apply_limit_offset(query=caronas_query, limit=limite, offset=deslocamento)
    
    caronas = caronas_query.all()
    
    return caronas


@router.put("/{carona_id}", response_model=CaronaExtended)
def update_carona(
    carona: Annotated[Carona, Depends(get_carona_by_id)],
    carona_id: int,
    motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    db: Annotated[Session, Depends(get_db)],
    partida_destino: CaronaUpdatePartidaDestino,
    veiculo_id: int | None = None,
    hora_de_partida: datetime | None = None,
    preco_carona: float | None = None
) -> CaronaExtended:
    '''
    - Atualiza informações de uma carona criada pelo usuário, passando seu id em _carona_id_. 
    - Podem ser alterados o carro da carona (_veículo_id_), o preço (_preco_carona_), o local de partida (_local_partida_ no body), 
    o local de destino (_local_destino_ no body) e/ou a hora de partida (_hora_de_partida_). Valores nulos em qualquer parâmetro 
    opcional indica que não haverá alteração de tal informação da carona no banco.
    - Retorna a carona modificada
    '''
    
    if carona.fk_motorista != motorista.id_fk_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Carona id={carona_id} não encontrada.")
    
    if veiculo_id is not None:
        db_motorista_veiculo = get_motorista_veiculo_of_user(
            veiculo_id=veiculo_id,
            motorista=motorista,
            db=db
        )
        if not db_motorista_veiculo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle of current user with id {veiculo_id} not found.")
    
    carona = update_carona_in_db(
        db_carona=carona,
        carona_new_info=CaronaUpdate(
            fk_motorista_veiculo=veiculo_id,
            hora_partida=hora_de_partida,
            valor=preco_carona,
            local_partida=partida_destino.local_partida,
            local_destino=partida_destino.local_destino,
        ),
        db=db
    )
    
    return carona


@router.delete("/{carona_id}", response_model=str)
def delete_carona(
    carona: Annotated[Carona, Depends(get_carona_by_id)],
    carona_id: int,
    motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    db: Annotated[Session, Depends(get_db)],
)-> str:
    '''
    - Remove a carona criada pelo usuário passando seu id em _carona_id_
    - Retorna uma mensagem "Carona id={_carona_id_} removida com sucesso" caso a carona seja removida
    '''
    if carona.fk_motorista != motorista.id_fk_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Carona id={carona_id} não encontrada.")

    remove_carona_from_db(db_carona=carona, db=db)
    
    return f"Carona id={carona_id} removida com sucesso"


@router.get("/historico/me/motorista", response_model=list[CaronaExtended])
def get_my_historico_as_motorista(
    current_motorista: Annotated[Motorista, Depends(get_current_active_motorista)],
    db: Annotated[Session, Depends(get_db)],
    data_minima: datetime = Query(datetime.now()-timedelta(days=365), description="Data mínima de partida da carona. Se nada for passado, será considerada a data atual-1ano"),
    data_maxima: datetime = Query(datetime.now()+timedelta(days=365), description="Data máxima de partida da carona. Se nada for passado, será considerada a data atual+1ano"),
    limite: int = Query(10, description="Limite de caronas retornadas pela query"),
    deslocamento: int = Query(0, description="Deslocamento (offset) da query. Os params _deslocamento_=1 e _limit_=10, por exemplo, indicam que a query retornará as caronas de 11 a 20, pulando as caronas de 1 a 10."),
) -> list[CaronaExtended]:
    filters = []
    
    if data_minima > data_maxima:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="data_minima não pode ser maior que data_maxima"
        )
    
    filters.append(Carona.fk_motorista == current_motorista.id_fk_user)
    if data_minima:
        filters.append(Carona.hora_partida >= data_minima)
    if data_maxima:
        filters.append(Carona.hora_partida <= data_maxima)
    
    order_by_dict = CaronaOrderByOptions.get_order_by_dict()
    
    caronas_query = db.query(Carona).filter(*filters).order_by(order_by_dict[CaronaOrderByOptions.hora_partida.value][False])
    caronas_query = apply_limit_offset(query=caronas_query, limit=limite, offset=deslocamento)
    
    caronas = caronas_query.all()
    
    return caronas


@router.get("/historico/me/passageiro", response_model=list[CaronaExtended])
def get_my_historico_as_passageiro(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    data_minima: datetime = Query(datetime.now()-timedelta(days=365), description="Data mínima de partida da carona. Se nada for passado, será considerada a data atual-1ano"),
    data_maxima: datetime = Query(datetime.now()+timedelta(days=365), description="Data máxima de partida da carona. Se nada for passado, será considerada a data atual+1ano"),
    limite: int = Query(10, description="Limite de caronas retornadas pela query"),
    deslocamento: int = Query(0, description="Deslocamento (offset) da query. Os params _deslocamento_=1 e _limit_=10, por exemplo, indicam que a query retornará as caronas de 11 a 20, pulando as caronas de 1 a 10."),
) -> list[CaronaExtended]:
    filters = []
    
    if data_minima > data_maxima:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="data_minima não pode ser maior que data_maxima"
        )
    
    if data_minima:
        filters.append(Carona.hora_partida >= data_minima)
    if data_maxima:
        filters.append(Carona.hora_partida <= data_maxima)
    filters.append(UserCarona.fk_user == current_user.id)
    
    order_by_dict = CaronaOrderByOptions.get_order_by_dict()
    
    caronas_query = (
        db.query(Carona)
        .join(UserCarona, Carona.id == UserCarona.fk_carona)
        .filter(*filters)
        .order_by(order_by_dict[CaronaOrderByOptions.hora_partida.value][False])
    )
    caronas_query = apply_limit_offset(query=caronas_query, limit=limite, offset=deslocamento)
    
    caronas = caronas_query.all()
    
    return caronas

@router.post("/caronas/from_pedido/", response_model=CaronaExtended)
def create_carona_from_pedido(
    pedido_carona_id: int,
    db: Annotated[Session, Depends(get_db)], 
    current_user: Annotated[User, Depends(get_current_active_user)],
    veiculo_id: int = Query()
    ):
    pedido_carona = db.query(PedidoCarona).filter(PedidoCarona.id == pedido_carona_id).first()
    if not pedido_carona:
        raise HTTPException(status_code=404, detail="Pedido de carona não encontrado")

    nova_carona = Carona(
        hora_partida=pedido_carona.hora_partida_minima,
        local_partida=pedido_carona.local_partida,
        fk_motorista_veiculo=veiculo_id,
        fk_motorista=current_user.id,
        local_destino=pedido_carona.local_destino,
        valor=pedido_carona.valor
    )
    db.add(nova_carona)
    db.commit()
    db.refresh(nova_carona)
    
    user_carona = UserCarona(
        fk_user=pedido_carona.fk_user,
        fk_carona=nova_carona.id
    )
    db.add(user_carona)
    db.commit()
    
    return nova_carona