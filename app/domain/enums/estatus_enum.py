from enum import Enum

class Estatus(Enum):
    PENDIENTE = "pendiente"
    LEYENDO = "leyendo"
    TERMINADO = "terminado"
    RELEER = "releer"
    PAUSADO = "pausado"
    ABANDONADO = "abandonado"