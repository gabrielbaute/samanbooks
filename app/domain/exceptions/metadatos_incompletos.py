class MetadatosIncompletos(Exception):
    def __init__(self, mensaje: str = "Los metadatos del libro están incompletos"):
        super().__init__(mensaje)