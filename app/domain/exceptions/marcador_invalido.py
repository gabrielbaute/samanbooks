class MarcadorInvalido(Exception):
    def __init__(self, mensaje: str = "El marcador no es válido"):
        super().__init__(mensaje)