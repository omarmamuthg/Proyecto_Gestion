# from pydantic import BaseModel
# from typing import Optional
# from decimal import Decimal

# class CotizacionMaterial(BaseModel):
#     id_cotizacion_material: Optional[int] = None  # Opcional si es autoincremental
#     id_cotizacion: int                             # Clave foránea a la tabla Cotizaciones (NOT NULL)
#     id_proveedor_material: Optional[int] = None    # Clave foránea a la tabla Proveedor_Material (YES)
#     cantidad: Optional[Decimal] = None             # Cantidad del material en la cotización (YES)

from pydantic import BaseModel, validator
from typing import Optional
from decimal import Decimal

class CotizacionMaterial(BaseModel):
    id_cotizacion_material: Optional[int] = None
    id_cotizacion: int
    id_proveedor_material: Optional[int] = None
    cantidad: Optional[float] = None  # Cambiado a float para compatibilidad con pyodbc