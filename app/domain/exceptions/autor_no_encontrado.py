class AutorNoEncontrado(Exception):
    def __init__(self, mensaje: str = "El autor solicitado no se encuentra en la biblioteca"):
        super().__init__(mensaje)