class LibroNoValido(Exception):
    def __init__(self, mensaje: str = "El libro no es válido"):
        super().__init__(mensaje)