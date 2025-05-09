
#material_controller
from typing import List, Optional
from Models.material import Material
from Repositorys.material_repository import MaterialRepository

class MaterialController:
    def __init__(self, connection_string: str):
        self.repository = MaterialRepository(connection_string)

    def crear_material(self, material_data: dict) -> Material:
        material = Material(**material_data)
        return self.repository.create_material(material)

    def obtener_material(self, id_material: int, incluir_inactivos: bool = False) -> Optional[Material]:
        return self.repository.get_material(id_material, incluir_inactivos)

    def obtener_todos_materiales(self, activos_only: bool = True) -> List[Material]:
        return self.repository.get_all_materiales(activos_only)

    def actualizar_material(self, id_material: int, material_data: dict) -> Optional[Material]:
        material = self.repository.get_material(id_material)
        if not material:
            return None
            
        # Actualizar solo campos proporcionados
        for key, value in material_data.items():
            if hasattr(material, key):
                setattr(material, key, value)
                
        return self.repository.update_material(id_material, material)

    def eliminar_material(self, id_material: int) -> bool:
        """Eliminación lógica (marca como inactivo)"""
        try:
            # Verificar que existe y está activo
            material = self.repository.get_material(id_material)
            if not material:
                print("❌ Material no encontrado")
                return False
                
            if not getattr(material, 'activo', True):
                print("⚠️ El material ya está inactivo")
                return False
                
            return self.repository.marcar_como_inactivo(id_material)
            
        except Exception as e:
            print(f"❌ Error al eliminar material: {str(e)}")
            return False