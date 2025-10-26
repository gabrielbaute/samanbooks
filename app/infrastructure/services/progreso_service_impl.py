from uuid import uuid4, UUID
from typing import Optional, List, Dict
from datetime import date


from app.domain.services import ProgresoService
from app.domain.entities import Progreso
from app.domain.enums import Estatus
from app.domain.exceptions import MetadatosIncompletos, ProgresoInvalido
from app.infrastructure.database.repositories.sqlalchemy_progreso_repository import SQLAlchemyProgresoRepository

class ProgresoServiceImpl(ProgresoService):
    def __init__(self, progreso_repo: SQLAlchemyProgresoRepository):
        self.repo = progreso_repo
    
    def iniciar_lectura(self, usuario_id: UUID, libro_id: UUID) -> Progreso:
        if not usuario_id or not libro_id:
            raise MetadatosIncompletos()
        
        progreso = Progreso(
            id=uuid4(),
            usuario_id=usuario_id,
            libro_id=libro_id,
            fecha_inicio=date.today(),
            estatus=Estatus.LEYENDO
        )

        try:
            self.repo.guardar(progreso)
        except Exception as e:
            raise ProgresoInvalido(f"Error al iniciar la lectura: {e}")
        
        return progreso
    
    def actualizar_progreso(self, progreso_id: UUID, pagina_actual: int, estatus: Estatus) -> Progreso:
        progreso = self.repo.obtener_por_id(progreso_id)
        if not progreso:
            raise ProgresoInvalido("Progreso no encontrado.")
        
        progreso.pagina_actual = pagina_actual
        progreso.estatus = estatus
        if estatus == Estatus.TERMINADO:
            progreso.fecha_finalizacion = date.today()
        
        try:
            self.repo.guardar(progreso)
        except Exception as e:
            raise ProgresoInvalido(f"Error al actualizar el progreso: {e}")
        
        return progreso
    
    def obtener_progreso_por_usuario_y_libro(self, usuario_id: UUID, libro_id: UUID) -> Optional[Progreso]:
        return self.repo.obtener_por_usuario_y_libro(usuario_id, libro_id)
    
    def obtener_progresos_por_usuario(self, usuario_id: UUID) -> List[Progreso]:
        return self.repo.obtener_por_usuario(usuario_id)
    
    def eliminar_progreso(self, progreso_id: UUID) -> None:
        self.repo.eliminar(progreso_id)
    
    def obtener_todos(self) -> List[Progreso]:
        return self.repo.listar_todos()