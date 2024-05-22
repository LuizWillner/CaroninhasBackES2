import enum


class Cor(str, enum.Enum):
    amarelo = "AMARELO"
    azul = "AZUL"
    branco = "BRANCO"
    dourado = "DOURADO"
    laranja = "LARANJA"
    marrom = "MARROM"
    prata = "PRATA"
    preto = "PRETO"
    rosa = "ROSA"
    roxo = "ROXO"
    verde = "VERDE"
    vermelho = "VERMELHO"
    
    @classmethod
    def get_cores(self):
        return [cor.value for cor in self]


class TipoVeiculo(str, enum.Enum):
    carro = "CARRO"
    # moto = "MOTO"
    
    @classmethod
    def get_tipos(self):
        return [tipo.value for tipo in self]
    
    
class MarcaVeiculo(str, enum.Enum):
    audi = "AUDI"
    bmw = "BMW"
    chery = "CHERY"
    chevrolet = "CHEVROLET"
    citroen = "CITROЁN"
    daewoo = "DAEWOO"
    daihatsu = "DAIHATSU"
    fiat = "FIAT"
    ford = "FORD"
    gmw = "GMW"
    honda = "HONDA"
    hyundai = "HYUNDAI"
    jac = "JAC"
    jeep = "JEEP"
    kia = "KIA"
    land_rover = "LAND ROVER"
    mercedes_benz = "MERCEDES-BENZ"
    mitsubishi = "MITSUBISHI"
    nissan = "NISSAN"
    peugeot = "PEUGEOT"
    renault = "RENAULT"
    smart = "SMART"
    suzuki = "SUZUKI"
    toyota = "TOYOTA"
    volvo = "VOLVO"
    volkswagen = "VOLKSWAGEN"
    outro = "OUTRO"
    
    @classmethod
    def get_marcas(self):
        return [marca.value for marca in self]
    