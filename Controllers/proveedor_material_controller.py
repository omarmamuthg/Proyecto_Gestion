# # En controllers/proveedor_material_controller.py

# class ProveedorMaterialController:
#     def __init__(self, proveedor_material_repo, proveedor_repo, material_repo):
#         self.proveedor_material_repo = proveedor_material_repo
#         self.proveedor_repo = proveedor_repo
#         self.material_repo = material_repo

#     def vincular_material(self, id_proveedor, id_material, precio):
#         # Validar que el proveedor y el material existan (usando proveedor_repo y material_repo)
#         if not self.proveedor_repo.obtener_por_id(id_proveedor):
#             raise ValueError("Proveedor no encontrado")
#         if not self.material_repo.obtener_por_id(id_material):
#             raise ValueError("Material no encontrado")

#         # Validar el precio
#         if precio is None or precio <= 0:
#             raise ValueError("El precio debe ser un valor positivo")

#         # Llamar al repositorio para crear la vinculación
#         self.proveedor_material_repo.vincular_material_a_proveedor(id_proveedor, id_material, precio)

#     def obtener_materiales_de_proveedor(self, id_proveedor):
#         # Validar que el proveedor exista
#         if not self.proveedor_repo.obtener_por_id(id_proveedor):
#             raise ValueError("Proveedor no encontrado")

#         # Llamar al repositorio para obtener los materiales
#         materiales = self.proveedor_material_repo.obtener_materiales_de_proveedor(id_proveedor)
#         return materiales

#     # Métodos similares para obtener proveedores de un material, etc.





# from Repositorys.proveedor_material_repository import ProveedorMaterialRepository
# from Repositorys.proveedor_repository import ProveedorRepository
# from Repositorys.material_repository import MaterialRepository

# class ProveedorMaterialController:
#     def __init__(self, connection_string):
#         self.proveedor_material_repo = ProveedorMaterialRepository(connection_string)
#         self.proveedor_repo = ProveedorRepository(connection_string)
#         self.material_repo = MaterialRepository(connection_string)
    
#     def vincular_material(self, id_proveedor, id_material, precio):
#         try:
#             # Validar que existan el proveedor y el material
#             if not self.proveedor_repo.obtener_por_id(id_proveedor):
#                 print("❌ Proveedor no encontrado")
#                 return False
            
#             if not self.material_repo.obtener_por_id(id_material):
#                 print("❌ Material no encontrado")
#                 return False
            
#             # Validar el precio
#             if precio <= 0:
#                 print("❌ El precio debe ser mayor que cero")
#                 return False
            
#             # Intentar la vinculación
#             return self.proveedor_material_repo.vincular_material_a_proveedor(
#                 id_proveedor, 
#                 id_material, 
#                 precio
#             )
            
#         except Exception as e:
#             print(f"❌ Error al vincular material: {str(e)}")
#             return False
    
#     def obtener_materiales_de_proveedor(self, id_proveedor):
#         return self.proveedor_material_repo.obtener_materiales_de_proveedor(id_proveedor)
    
#     def obtener_proveedores_de_material(self, id_material):
#         return self.proveedor_material_repo.obtener_proveedores_de_material(id_material)




# from Repositorys.proveedor_material_repository import ProveedorMaterialRepository
# from Repositorys.proveedor_repository import ProveedorRepository
# from Repositorys.material_repository import MaterialRepository
# import pyodbc

# class ProveedorMaterialController:
#     def __init__(self, connection_string):
#         self.connection_string = connection_string
#         self.conn = pyodbc.connect(connection_string)
#         self.proveedor_material_repo = ProveedorMaterialRepository(self.conn)
#         self.proveedor_repo = ProveedorRepository(self.conn)
#         self.material_repo = MaterialRepository(self.conn)

#     def __del__(self):
#         if hasattr(self, 'conn') and self.conn:
#             self.conn.close()

#     def vincular_material(self, id_proveedor, id_material, precio):
#         try:
#             # Validar que existan el proveedor y el material
#             if not self.proveedor_repo.obtener_por_id(id_proveedor):
#                 print("❌ Proveedor no encontrado")
#                 return False

#             if not self.material_repo.obtener_por_id(id_material):
#                 print("❌ Material no encontrado")
#                 return False

#             # Validar el precio
#             if precio <= 0:
#                 print("❌ El precio debe ser mayor que cero")
#                 return False

#             # Intentar la vinculación
#             return self.proveedor_material_repo.vincular_material_a_proveedor(
#                 id_proveedor,
#                 id_material,
#                 precio
#             )

#         except pyodbc.Error as e:
#             print(f"❌ Error al vincular material (Controlador): {e}")
#             return False

#     def obtener_materiales_de_proveedor(self, id_proveedor):
#         return self.proveedor_material_repo.obtener_materiales_de_proveedor(id_proveedor)

#     def obtener_proveedores_de_material(self, id_material):
#         return self.proveedor_material_repo.obtener_proveedores_de_material(id_material)}






















# from Repositorys.proveedor_material_repository import ProveedorMaterialRepository
# from Repositorys.proveedor_repository import ProveedorRepository
# from Repositorys.material_repository import MaterialRepository
# import pyodbc

# class ProveedorMaterialController:
#     def __init__(self, connection_string):
#         self.connection_string = connection_string
#         self.conn = pyodbc.connect(connection_string)
#         self.proveedor_material_repo = ProveedorMaterialRepository(self.conn)
#         self.proveedor_repo = ProveedorRepository(self.conn)
#         self.material_repo = MaterialRepository(self.conn)

#     def __del__(self):
#         if hasattr(self, 'conn') and self.conn:
#             self.conn.close()

#     def vincular_material(self, id_proveedor, id_material, precio):
#         try:
#             # Validar que existan el proveedor y el material
#             # Cambio realizado aquí: usar get_proveedor en lugar de obtener_por_id
#             if not self.proveedor_repo.get_proveedor(id_proveedor):
#                 print("❌ Proveedor no encontrado")
#                 return False

#             if not self.material_repo.obtener_por_id(id_material):
#                 print("❌ Material no encontrado")
#                 return False

#             # Validar el precio
#             if precio <= 0:
#                 print("❌ El precio debe ser mayor que cero")
#                 return False
#             # Intentar la vinculación
#             return self.proveedor_material_repo.vincular_material_a_proveedor(
#                 id_proveedor,
#                 id_material,
#                 precio
#             )

#         except pyodbc.Error as e:
#             print(f"❌ Error al vincular material (Controlador): {e}")
#             return False

#     def obtener_materiales_de_proveedor(self, id_proveedor):
#         return self.proveedor_material_repo.obtener_materiales_de_proveedor(id_proveedor)

#     def obtener_proveedores_de_material(self, id_material):
#         return self.proveedor_material_repo.obtener_proveedores_de_material(id_material)




#controlador_proveedor_material}
# from Repositorys.proveedor_material_repository import ProveedorMaterialRepository
# from Repositorys.proveedor_repository import ProveedorRepository
# from Repositorys.material_repository import MaterialRepository
# import pyodbc



















#proveedor_material_controlador
# from Repositorys.proveedor_material_repository import ProveedorMaterialRepository
# from Repositorys.proveedor_repository import ProveedorRepository
# from Repositorys.material_repository import MaterialRepository
# import pyodbc
# from decimal import Decimal

# class ProveedorMaterialController:
    # def __init__(self, connection_string):
    #     self.connection_string = connection_string
    #     self.proveedor_material_repo = ProveedorMaterialRepository(connection_string)
    #     self.proveedor_repo = ProveedorRepository(connection_string)
    #     self.material_repo = MaterialRepository(connection_string)

    # def __del__(self):
    #     if hasattr(self, 'conn') and self.conn:
    #         self.conn.close()


    # def vincular_material(self, id_proveedor: int, id_material: int, precio) -> bool:
    #     """Versión corregida con manejo de errores mejorado"""
    #     try:
    #         # Validaciones
    #         if not self.proveedor_repo.obtener_proveedor(int(id_proveedor)):
    #             print("❌ Proveedor no encontrado")
    #             return False

    #         if not self.material_repo.obtener_por_id(int(id_material)):
    #             print("❌ Material no encontrado")
    #             return False

    #         # Conversión segura del precio
    #         try:
    #             precio_float = float(Decimal(str(precio)))
    #             if precio_float <= 0:
    #                 print("❌ El precio debe ser positivo")
    #                 return False
    #         except:
    #             print("❌ Precio inválido")
    #             return False

    #         # Operación de vinculación
    #         return self.proveedor_material_repo.vincular_material_a_proveedor(
    #             int(id_proveedor),
    #             int(id_material),
    #             precio_float
    #         )
    #     except Exception as e:
    #         print(f"❌ Error en controlador: {str(e)}")
    #         return False
from Repositorys.proveedor_material_repository import ProveedorMaterialRepository
from Repositorys.proveedor_repository import ProveedorRepository
from Repositorys.material_repository import MaterialRepository
import pyodbc
from decimal import Decimal

class ProveedorMaterialController:

    def __init__(self, connection_string):
        # Establece la conexión principal
        self.conn = pyodbc.connect(connection_string)
        
        # Pasa la conexión establecida a los repositorios
        self.proveedor_material_repo = ProveedorMaterialRepository(self.conn)
        self.proveedor_repo = ProveedorRepository(connection_string)  # O usa self.conn si también lo modificas
        self.material_repo = MaterialRepository(connection_string)    # O usa self.conn si también lo modificas

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    
    def vincular_material(self, id_proveedor: int, id_material: int, precio) -> bool:
        """Versión corregida con manejo de conexiones adecuado"""
        try:
            # Validaciones
            if not self.proveedor_repo.obtener_proveedor(int(id_proveedor)):
                print("❌ Proveedor no encontrado")
                return False

            if not self.material_repo.get_material(int(id_material)):  # Asegúrate que se llame igual en MaterialRepository
                print("❌ Material no encontrado")
                return False

            # Conversión segura del precio
            try:
                precio_float = float(Decimal(str(precio)))
                if precio_float <= 0:
                    print("❌ El precio debe ser positivo")
                    return False
            except:
                print("❌ Precio inválido")
                return False

            # Operación de vinculación
            return self.proveedor_material_repo.vincular_material_a_proveedor(
                int(id_proveedor),
                int(id_material),
                precio_float
            )
        except Exception as e:
            print(f"❌ Error en controlador: {str(e)}")
            return False

    def obtener_materiales_de_proveedor(self, id_proveedor):
        return self.proveedor_material_repo.obtener_materiales_de_proveedor(id_proveedor)

    def obtener_proveedores_de_material(self, id_material):
        return self.proveedor_material_repo.obtener_proveedores_de_material(id_material)
