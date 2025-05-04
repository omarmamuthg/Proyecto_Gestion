#Cotizacion_servicio
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CotizacionServicio(BaseModel):
    id_cotizacion_servicio: Optional[int] = None
    id_cotizacion: int
    nombre_servicio: str
    descripcion_servicio: Optional[str] = None
    tipo_servicio: Optional[str] = None
    costo_servicio: float
    cantidad_servicio: Optional[float] = None
    fecha_creacion_servicio: Optional[datetime] = None
    activo: bool = True
    usuario_creador_servicio: str
    fecha_actualizacion_servicio: Optional[datetime] = None
