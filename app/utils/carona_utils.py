import enum
from sqlalchemy import asc, desc
from app.database.carona_orm import Carona


class CaronaOrderByOptions(str, enum.Enum):
    hora_partida = "hora da partida"
    valor = "valor"
    hora_oferta = "hora da oferta"
    
    @classmethod
    def get_order_by_dict(self) -> dict:
        return {
            self.hora_partida.value: {
                True: asc(Carona.hora_partida),
                False: desc(Carona.hora_partida)
            },
            self.valor.value: {
                True: asc(Carona.valor),
                False: desc(Carona.valor)
            },
            self.hora_oferta.value: {
                True: asc(Carona.created_at),
                False: desc(Carona.created_at)
            }
        }
        