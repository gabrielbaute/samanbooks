class UsuarioNoEncontrado(Exception):
    def __init__(self, mensaje: str = "Usuario no encontrado"):
        super().__init__(mensaje)