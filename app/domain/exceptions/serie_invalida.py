class SerieInvalida(Exception):
    def __init__(self, mensaje: str = "La serie no es válida"):
        super().__init__(mensaje)