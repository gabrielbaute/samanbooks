class AutorNoValido(Exception):
    def __init__(self, mensaje: str = "El autor no es válido"):
        super().__init__(mensaje)