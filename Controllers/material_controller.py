# #material controller
# from typing import List, Optional
# from Models.material import Material
# from Repositorys.material_repository import MaterialRepository
# from decimal import Decimal

# class MaterialController:
#     def __init__(self, connection_string: str):
#         self.repository = MaterialRepository(connection_string)

#     def crear_material(self, material_data: dict) -> Material:
#         """Crea un nuevo material."""
#         material = Material(**material_data)
#         return self.repository.create_material(material)

#     def obtener_material(self, id_material: int) -> Optional[Material]:
#         """Obtiene un material por su ID."""
#         return self.repository.get_material(id_material)

#     def obtener_todos_materiales(self, activos_only: bool = True) -> List[Material]:
#         """Lista materiales, con filtro opcional por estado activo."""
#         return self.repository.get_all_materiales(activos_only)

#     def actualizar_material(self, id_material: int, material_data: dict) -> Optional[Material]:
#         """Actualiza parcialmente un material existente."""
#         material_existente = self.repository.get_material(id_material)
#         if not material_existente:
#             return None
            
#         update_data = material_existente.dict()
#         update_data.update(material_data)
        
#         material_actualizado = Material(**update_data)
#         return self.repository.update_material(id_material, material_actualizado)

#     # def eliminar_material(self, id_material: int) -> bool:
#     #     """Eliminación lógica (marca como inactivo)."""
#     #     return self.repository.delete_material(id_material)

#     # def eliminar_material(self, id_material: int) -> bool:
#     #     try:
#     #         # Verificar que existe primero
#     #         if not self.repository.obtener_material(id_material):
#     #             return False
                
#     #         return self.repository.marcar_como_inactivo(id_material)
#     #     except:
#     #         return False

#     # def buscar_por_nombre(self, nombre: str) -> List[Material]:
#     #     """Busca materiales por coincidencia en el nombre."""
#     #     materiales = self.repository.get_all_materiales(activos_only=False)
#     #     return [m for m in materiales if nombre.lower() in m.nombre.lower()]

#     def eliminar_material(self, id_material: int) -> bool:
#         """Eliminación lógica de un material"""
#         try:
#             # Verificar que el material existe y está activo
#             material = self.repository.obtener_material(id_material)
#             if not material:
#                 print("❌ El material no existe")
#                 return False
                
#             if not material.activo:
#                 print("⚠️ El material ya está inactivo")
#                 return False
                
#             # Intentar desactivar
#             if self.repository.marcar_como_inactivo(id_material):
#                 print("✅ Material desactivado (eliminación lógica)")
#                 return True
                
#             print("❌ No se pudo desactivar el material")
#             return False
            
#         except Exception as e:
#             print(f"❌ Error inesperado: {str(e)}")
#             return False
#     def get_all_materiales(self, activos_only=True) -> List[Material]:
#         """Consulta que realmente trae todos los datos"""
#         query = "SELECT id_material, nombre, unidad_medida, categoria, marca FROM Materiales"
#         if activos_only:
#             query += " WHERE activo = 1"
#         # Ejecutar consulta y mapear resultados
        

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