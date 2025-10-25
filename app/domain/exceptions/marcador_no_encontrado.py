class MarcadorNoEncontrado(Exception):
    def __init__(self, mensaje: str = "El marcador solicitado no se encuentra en la biblioteca"):
        super().__init__(mensaje)