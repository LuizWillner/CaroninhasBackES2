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

class TipoVeiculo(str, enum.Enum):
    carro = "CARRO"
    # moto = "MOTO"
    
    
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
    
    