from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class Material(BaseModel):
    id_material: Optional[int] = None  # Autoincremental, generado por la BD
    nombre: str                        # NOT NULL
    descripcion: Optional[str] = None  # Campo tipo TEXT (puede ser largo)
    unidad_medida: str                 # NOT NULL
    marca: Optional[str] = None        # Puede ser NULL
    categoria: Optional[str] = None    # Puede ser NULL
    fecha_registro: datetime           # NOT NULL, se registra en la BD
    activo: bool = True                 # Valor por defecto True (1 en SQL Server)
# from pydantic import BaseModel
# from datetime import datetime

# class Material(BaseModel):
#     id_material: Optional[int] = None
#     nombre: str
#     descripcion: Optional[str] = None
#     unidad_medida: str
#     marca: Optional[str] = None
#     categoria: Optional[str] = None
#     fecha_registro: Optional[datetime] = None
#     activo: Optional[bool] = True  # Nuevo campo importante
