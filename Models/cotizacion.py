
# #clase cotizacion
# from pydantic import BaseModel, Field
# from typing import Optional
# from datetime import datetime

# class Cotizacion(BaseModel):
#     id_cotizacion: Optional[int] = None
#     id_cliente: int  # Es obligatorio (NO NULL)

#     fecha_creacion: Optional[datetime] = None  # Se asigna automáticamente con getdate()
#     fecha_activacion: Optional[datetime] = None
#     fecha_finalizacion: Optional[datetime] = None
#     fecha_cancelacion: Optional[datetime] = None

#     estado: Optional[str] = Field(default=None, max_length=50)
#     total: Optional[float] = None
#     descuento: Optional[float] = Field(default=0.00)
#     total_con_descuento: Optional[float] = None

#     observaciones: Optional[str] = None
#     validez: Optional[int] = Field(default=15)  # Valor por defecto (15 días)

#     usuario_creador: Optional[str] = Field(default=None, max_length=100)
#     nombre_cliente: str  # Campo obligatorio (NO NULL)
#     correo_cliente: str  # Campo obligatorio (NO NULL)
#     telefono_cliente: Optional[str] = Field(default=None, max_length=20)
#     tipo_cliente: Optional[str] = Field(default=None, max_length=50)
#     rfc_cliente: Optional[str] = Field(default=None, max_length=20)

#     nombre_servicio: Optional[str] = Field(default="Servicio personalizado", max_length=100)
#     descripcion_servicio: Optional[str] = None
#     tipo_servicio: Optional[str] = Field(default="Personalizado", max_length=50)

#     costo_servicio: float = Field(default=0.00)
#     cantidad_servicios: int = Field(default=1)
#     subtotal_servicio: float = Field(default=0.00)
#     usuario_creador_servicio: Optional[str] = Field(default=None, max_length=100)
#     descuento_servicio: float = Field(default=0.00)
#     total_con_descuento_servicio: float = Field(default=0.00)

#     fecha_actualizacion: Optional[datetime] = None  # Se asigna automáticamente con getdate()


#cotizacion clase
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Cotizacion(BaseModel):
    id_cotizacion: Optional[int] = None
    id_cliente: int
    fecha_creacion: Optional[datetime] = None
    fecha_activacion: Optional[datetime] = None
    fecha_finalizacion: Optional[datetime] = None
    fecha_cancelacion: Optional[datetime] = None
    observaciones: Optional[str] = None
    usuario_creador: Optional[str] = None
    nombre_cliente: Optional[str] = None
    correo_cliente: Optional[str] = None
    telefono_cliente: Optional[str] = None
    tipo_cliente: Optional[str] = None
    rfc_cliente: str
    activo: bool = True

