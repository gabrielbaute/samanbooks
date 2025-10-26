class SerieNoEncontrada(Exception):
    def __init__(self, mensaje: str = "La serie solicitada no se encuentra en la biblioteca"):
        super().__init__(mensaje)