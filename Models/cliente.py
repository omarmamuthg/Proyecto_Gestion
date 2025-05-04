#ejemplo clase de clientes 
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Cliente(BaseModel):
    id_cliente: Optional[int] = None      # Opcional porque es autoincremental
    nombre: str                           # Campo obligatorio (NOT NULL en BD)
    correo: Optional[str] = None
    telefono: Optional[str] = None
    tipo_cliente: Optional[str] = None    # CHECK: 'Persona Física' o 'Persona Moral'
    direccion: Optional[str] = None
    rfc: Optional[str] = None             # RFC con longitud máxima de 13 caracteres
    fecha_registro: Optional[datetime] = None  # Se asignará automáticamente en la BD
    activo: bool = True                   # Valor por defecto True (1 en SQL Server)
    comentarios: Optional[str] = None     # Texto largo/observaciones