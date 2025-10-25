from sqlalchemy.types import TypeDecorator, CHAR
import uuid

class GUID(TypeDecorator):
    """Plataforma-agnóstico UUID type."""
    impl = CHAR

    def load_dialect_impl(self, dialect):
        """

        """
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        """
        
        """
        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            return str(uuid.UUID(value))
        return str(value)

    def process_result_value(self, value, dialect):
        """
        
        """
        if value is None:
            return value
        return uuid.UUID(value)