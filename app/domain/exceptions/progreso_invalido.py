class ProgresoInvalido(Exception):
    def __init__(self, mensaje: str = "El progreso de lectura es inválido"):
        super().__init__(mensaje)