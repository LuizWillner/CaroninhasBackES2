import enum
from sqlalchemy import asc, desc
from app.database.pedido_carona_orm import PedidoCarona


class PedidoCaronaOrderByOptions(str, enum.Enum):
    hora_minima_partida = "hora mínima de partida"
    hora_maxima_partida = "hora máxima de partida"
    valor = "valor"
    hora_criacao = "hora de criação do pedido"
    
    @classmethod
    def get_order_by_dict(self) -> dict:
        return {
            self.hora_minima_partida.value: {
                True: asc(PedidoCarona.hora_partida_minima),
                False: desc(PedidoCarona.hora_partida_minima)
            },
            self.hora_maxima_partida.value: {
                True: asc(PedidoCarona.hora_partida_maxima),
                False: desc(PedidoCarona.hora_partida_maxima)
            },
            self.valor.value: {
                True: asc(PedidoCarona.valor),
                False: desc(PedidoCarona.valor)
            },
            self.hora_criacao.value: {
                True: asc(PedidoCarona.created_at),
                False: desc(PedidoCarona.created_at)
            }
        }
        