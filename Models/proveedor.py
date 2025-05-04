from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Proveedor(BaseModel):
    id_proveedor: Optional[int] = None  # Opcional porque es autoincremental
    nombre: str                         # Campo obligatorio (NOT NULL en BD)
    contacto: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    rfc: Optional[str] = None           # RFC con longitud máxima de 13 caracteres
    direccion: Optional[str] = None
    fecha_registro: Optional[datetime] = None  # Se asignará automáticamente en la BD
    activo: bool = True                 # Valor por defecto True (1 en SQL Server)