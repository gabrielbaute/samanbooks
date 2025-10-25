class LibroNoEncontrado(Exception):
    def __init__(self, mensaje: str = "El libro solicitado no se encuentra en la biblioteca"):
        super().__init__(mensaje)