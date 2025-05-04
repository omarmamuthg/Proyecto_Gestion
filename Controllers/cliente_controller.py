
#ciente controller
from typing import List, Optional
from Models.cliente import Cliente
from Repositorys.cliente_repository import ClienteRepository

class ClienteController:
    def __init__(self, connection_string: str):
        self.repository = ClienteRepository(connection_string)

    def crear_cliente(self, cliente_data: dict) -> Cliente:
        """Crea un nuevo cliente validando el tipo_cliente y RFC."""
        cliente = Cliente(**cliente_data)
        return self.repository.create_cliente(cliente)

    def obtener_cliente(self, id_cliente: int) -> Optional[Cliente]:
        """Obtiene un cliente por su ID (activo o inactivo)."""
        return self.repository.get_cliente(id_cliente)

    def obtener_todos_clientes(self, activos_only: bool = True) -> List[Cliente]:
        """Lista clientes, con filtro opcional por estado activo."""
        return self.repository.get_all_clientes(activos_only)

    def actualizar_cliente(self, id_cliente: int, cliente_data: dict) -> Optional[Cliente]:
        """Actualiza parcialmente un cliente existente."""
        cliente_existente = self.repository.get_cliente(id_cliente)
        if not cliente_existente:
            return None
            
        # Combinar datos existentes con los nuevos (actualización parcial)
        update_data = cliente_existente.dict()
        update_data.update(cliente_data)
        
        cliente_actualizado = Cliente(**update_data)
        return self.repository.update_cliente(id_cliente, cliente_actualizado)

    def eliminar_cliente(self, id_cliente: int) -> bool:
        """Eliminación lógica (marca como inactivo)."""
        return self.repository.delete_cliente(id_cliente)

    def buscar_por_nombre(self, nombre: str) -> List[Cliente]:
        """Busca clientes por coincidencia en el nombre (case-insensitive)."""
        clientes = self.repository.get_all_clientes(activos_only=False)
        return [c for c in clientes if nombre.lower() in c.nombre.lower()]

    def buscar_por_rfc(self, rfc: str) -> Optional[Cliente]:
        """Busca un cliente por RFC exacto (útil para validaciones)."""
        clientes = self.repository.get_all_clientes(activos_only=False)
        return next((c for c in clientes if c.rfc and c.rfc.lower() == rfc.lower()), None)