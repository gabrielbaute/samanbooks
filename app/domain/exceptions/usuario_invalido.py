class UsuarioInvalido(Exception):
    def __init__(self, mensaje: str = "El usuario no es válido"):
        super().__init__(mensaje)