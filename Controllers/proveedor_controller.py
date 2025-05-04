#cotrolador de proveedor 
from typing import List, Optional
from Models.proveedor import Proveedor
from Repositorys.proveedor_repository import ProveedorRepository

class ProveedorController:
    def __init__(self, connection_string: str):
        self.repository = ProveedorRepository(connection_string)

    def crear_proveedor(self, proveedor_data: dict) -> Proveedor:
        proveedor = Proveedor(**proveedor_data)
        return self.repository.create_proveedor(proveedor)

    def obtener_proveedor(self, id_proveedor: int) -> Optional[Proveedor]:
        return self.repository.get_proveedor(id_proveedor)

    def obtener_todos_proveedores(self, activos_only: bool = True) -> List[Proveedor]:
        return self.repository.get_all_proveedores(activos_only)

    def actualizar_proveedor(self, id_proveedor: int, proveedor_data: dict) -> Optional[Proveedor]:
        proveedor_existente = self.repository.get_proveedor(id_proveedor)
        if not proveedor_existente:
            return None
            
        # Actualizar solo los campos proporcionados
        update_data = proveedor_existente.dict()
        update_data.update(proveedor_data)
        
        proveedor_actualizado = Proveedor(**update_data)
        return self.repository.update_proveedor(id_proveedor, proveedor_actualizado)

    def eliminar_proveedor(self, id_proveedor: int) -> bool:
        return self.repository.delete_proveedor(id_proveedor)

    def buscar_por_nombre(self, nombre: str) -> List[Proveedor]:
        proveedores = self.repository.get_all_proveedores(activos_only=False)
        return [p for p in proveedores if nombre.lower() in p.nombre.lower()]