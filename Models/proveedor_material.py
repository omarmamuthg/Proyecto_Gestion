#clase proveedor_material 
from pydantic import BaseModel
from typing import Optional

class ProveedorMaterial(BaseModel):
    id_proveedor_material: Optional[int] = None  # Opcional si es autoincremental
    id_proveedor: int                             # Clave foránea a la tabla Proveedores (NOT NULL)
    id_material: int                              # Clave foránea a la tabla Materiales (NOT NULL)
    precio: float                                 # Precio del material ofrecido por el proveedor
    activo: bool = True