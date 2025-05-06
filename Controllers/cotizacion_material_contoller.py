# # control cotizacion_material
# from Repositorys.cotizacion_material_repository import CotizacionMaterialRepository
# from Repositorys.cotizacion_repository import CotizacionRepository
# from Repositorys.proveedor_material_repository import ProveedorMaterialRepository
# import pyodbc
# from decimal import Decimal

# from typing import Optional, List, Dict
# import pyodbc

# class CotizacionMaterialController:

#     def __init__(self, connection_string: str):
#         # Aquí ya no pasamos directamente la conexión, sino solo la cadena de conexión
#         self.cotizacion_material_repo = CotizacionMaterialRepository(connection_string)
#         self.cotizacion_repo = CotizacionRepository(connection_string)
#         self.proveedor_material_repo = ProveedorMaterialRepository(connection_string)

#     def __del__(self):
#         if hasattr(self, 'conn') and self.conn:
#             self.conn.close()

#     def agregar_material_a_cotizacion(
#         self, 
#         id_cotizacion: int, 
#         id_proveedor_material: Optional[int], 
#         cantidad: float
#     ) -> bool:
#         """Agrega un material a la cotización usando float"""
        
#         try:
#             # Validación de tipos y conversión
#             cantidad_float = float(cantidad)
#         except (ValueError, TypeError):
#             print("❌ La cantidad debe ser un número válido")
#             return False

#         # Validaciones de negocio
#         if cantidad_float <= 0:
#             print("❌ La cantidad debe ser mayor que cero")
#             return False

#         # Verificar si la cotización existe
#         if not self.cotizacion_repo.get_cotizacion(id_cotizacion):
#             print("❌ Cotización no encontrada")
#             return False

#         # Verificar la relación proveedor-material, si se proporciona
#         if id_proveedor_material and not self.proveedor_material_repo.obtener_vinculo(id_proveedor_material):
#             print("❌ Relación proveedor-material no encontrada")
#             return False

#         try:
#             # Guardar el material usando el repositorio adecuado
#             return self.cotizacion_material_repo.agregar_material(
#                 id_cotizacion=id_cotizacion,
#                 id_proveedor_material=id_proveedor_material,
#                 cantidad=cantidad_float
#             )
#         except Exception as e:
#             print(f"❌ Error inesperado al agregar material: {str(e)}")
#             return False


#     def obtener_materiales_de_cotizacion(self, id_cotizacion: int) -> Optional[List[Dict]]:
#         """Obtiene los materiales de una cotización"""
#         try:
#             if not self.cotizacion_repo.get_cotizacion(id_cotizacion):
#                 print("❌ Cotización no encontrada")
#                 return None
#             return self.repo.obtener_materiales_de_cotizacion(id_cotizacion)
#         except Exception as e:
#             print(f"❌ Error al obtener materiales: {str(e)}")
#             return None

#     def actualizar_cantidad_material(
#         self, 
#         id_cotizacion_material: int, 
#         nueva_cantidad: float
#     ) -> bool:
#         """Actualiza la cantidad de un material"""
#         try:
#             # Validación básica
#             if not self.repo.obtener_cotizacion_material(id_cotizacion_material):
#                 print("❌ Material no encontrado")
#                 return False

#             return self.repo.actualizar_cantidad(
#                 id_cotizacion_material=id_cotizacion_material,
#                 nueva_cantidad=nueva_cantidad
#             )
#         except Exception as e:
#             print(f"❌ Error al actualizar cantidad: {str(e)}")
#             return False

#     def eliminar_material_de_cotizacion(self, id_cotizacion_material: int) -> bool:
#         """Elimina un material de la cotización"""
#         try:
#             if not self.repo.obtener_cotizacion_material(id_cotizacion_material):
#                 print("❌ Material no encontrado")
#                 return False
#             return self.repo.eliminar_material(id_cotizacion_material)
#         except Exception as e:
#             print(f"❌ Error al eliminar material: {str(e)}")
#             return False



# Controllers/cotizacion_material_controller.py

from Repositorys.cotizacion_material_repository import CotizacionMaterialRepository
from Repositorys.cotizacion_repository import CotizacionRepository
from Repositorys.proveedor_material_repository import ProveedorMaterialRepository
import pyodbc
from decimal import Decimal
from typing import Optional, List, Dict

class CotizacionMaterialController:

    def __init__(self, connection_string: str):
        self.cotizacion_material_repo = CotizacionMaterialRepository(connection_string)
        self.cotizacion_repo = CotizacionRepository(connection_string)
        self.proveedor_material_repo = ProveedorMaterialRepository(connection_string)

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def agregar_material_a_cotizacion(
        self, 
        id_cotizacion: int, 
        id_proveedor_material: Optional[int], 
        cantidad: float
    ) -> bool:
        """Agrega un material a la cotización incluyendo el costo unitario"""

        try:
            cantidad_float = float(cantidad)
        except (ValueError, TypeError):
            print("❌ La cantidad debe ser un número válido")
            return False

        if cantidad_float <= 0:
            print("❌ La cantidad debe ser mayor que cero")
            return False

        if not self.cotizacion_repo.get_cotizacion(id_cotizacion):
            print("❌ Cotización no encontrada")
            return False

        if id_proveedor_material:
            proveedor_material = self.proveedor_material_repo.obtener_vinculo(id_proveedor_material)
            if not proveedor_material:
                print("❌ Relación proveedor-material no encontrada")
                return False
        else:
            print("❌ Debes proporcionar un id_proveedor_material válido")
            return False

        try:
            # Solo pasa lo necesario al repositorio
            return self.cotizacion_material_repo.agregar_material(
                id_cotizacion=id_cotizacion,
                id_proveedor_material=id_proveedor_material,
                cantidad=cantidad_float  # Solo pasamos estos tres
            )
        except Exception as e:
            print(f"❌ Error inesperado al agregar material: {str(e)}")
            return False

    def obtener_materiales_de_cotizacion(self, id_cotizacion: int) -> Optional[List[Dict]]:
        """Obtiene los materiales de una cotización"""
        try:
            if not self.cotizacion_repo.get_cotizacion(id_cotizacion):
                print("❌ Cotización no encontrada")
                return None
            return self.cotizacion_material_repo.obtener_materiales_de_cotizacion(id_cotizacion)
        except Exception as e:
            print(f"❌ Error al obtener materiales: {str(e)}")
            return None

    def actualizar_cantidad_material(
        self, 
        id_cotizacion_material: int, 
        nueva_cantidad: float
    ) -> bool:
        """Actualiza la cantidad de un material, recalculando subtotal"""

        try:
            cotizacion_material = self.cotizacion_material_repo.obtener_cotizacion_material(id_cotizacion_material)
            if not cotizacion_material:
                print("❌ Material no encontrado")
                return False

            nuevo_subtotal = nueva_cantidad * cotizacion_material['costo_unitario']

            return self.cotizacion_material_repo.actualizar_cantidad_y_subtotal(
                id_cotizacion_material=id_cotizacion_material,
                nueva_cantidad=nueva_cantidad,
                nuevo_subtotal=nuevo_subtotal
            )
        except Exception as e:
            print(f"❌ Error al actualizar cantidad: {str(e)}")
            return False

    def eliminar_material_de_cotizacion(self, id_cotizacion_material: int) -> bool:
        """Elimina un material de la cotización"""
        try:
            if not self.cotizacion_material_repo.obtener_cotizacion_material(id_cotizacion_material):
                print("❌ Material no encontrado")
                return False
            return self.cotizacion_material_repo.eliminar_material(id_cotizacion_material)
        except Exception as e:
            print(f"❌ Error al eliminar material: {str(e)}")
            return False
