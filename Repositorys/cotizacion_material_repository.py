# # repositorio cotizacion_material
# import pyodbc
# from decimal import Decimal
# from typing import Optional, List
# from Models.cotizacion_material import CotizacionMaterial  # Asegúrate de que la ruta al modelo sea correcta



# import pyodbc
# from typing import Optional, List, Dict

# class CotizacionMaterialRepository:
#     # def __init__(self, db_connection: pyodbc.Connection):
#     #     """Inicializa el repositorio con una conexión pyodbc existente"""
#     #     if not isinstance(db_connection, pyodbc.Connection):
#     #         raise ValueError("Se requiere una conexión pyodbc válida")
        
#     #     self.conn = db_connection

#     # def __init__(self, connection_string: str):
#     #     if not connection_string:
#     #         raise ValueError("Se requiere una conexión pyodbc válida")
#     #     self.connection_string = connection_string


#     def __init__(self, connection_string: str):
#         if not connection_string:
#             raise ValueError("Se requiere una conexión pyodbc válida")
#         self.connection_string = connection_string
#         self.conn = self._get_connection()  # Inicializa la conexión
#         self.table_name = "Cotizacion_Material"  # Define el nombre de la tabla si lo necesitas

#     # def _get_connection(self):
#     #     # Crear la conexión con la cadena de conexión
#     #     print(f"Conectando con: {self.connection_string}")
#     #     return pyodbc.connect(self.connection_string)

#     def _get_connection(self):
#         # print(f"Intentando conectar con connection_string: {self.connection_string}")
#         return pyodbc.connect(self.connection_string)


#     def agregar_material(self, id_cotizacion: int, id_proveedor_material: Optional[int], cantidad: float) -> bool:
#         """Agrega un nuevo registro usando float"""
#         try:
#             # Redondeamos a 2 decimales para consistencia
#             cantidad_redondeada = round(float(cantidad), 2)
            
#             sql = f"""
#                 INSERT INTO {self.table_name} 
#                 (id_cotizacion, id_proveedor_material, cantidad)
#                 VALUES (?, ?, ?)
#             """
#             params = (
#                 int(id_cotizacion),
#                 int(id_proveedor_material) if id_proveedor_material is not None else None,
#                 cantidad_redondeada
#             )
            
#             with self.conn.cursor() as cursor:
#                 cursor.execute(sql, params)
#                 self.conn.commit()
#                 return True
                
#         except pyodbc.Error as ex:
#             print(f"Error SQL al agregar material: {ex}")
#             self.conn.rollback()
#             return False
#         except Exception as ex:
#             print(f"Error inesperado al agregar material: {ex}")
#             self.conn.rollback()
#             return False

#     def obtener_cotizacion_material(self, id_cotizacion_material: int) -> Optional[Dict]:
#         """Obtiene un registro por su ID"""
#         try:
#             sql = f"""
#                 SELECT id_cotizacion_material, id_cotizacion, 
#                        id_proveedor_material, cantidad 
#                 FROM {self.table_name} 
#                 WHERE id_cotizacion_material = ?
#             """
#             with self.conn.cursor() as cursor:
#                 cursor.execute(sql, id_cotizacion_material)
#                 row = cursor.fetchone()
#                 if row:
#                     return {
#                         "id_cotizacion_material": row.id_cotizacion_material,
#                         "id_cotizacion": row.id_cotizacion,
#                         "id_proveedor_material": row.id_proveedor_material,
#                         "cantidad": float(row.cantidad)  # Convertimos a float
#                     }
#                 return None
#         except Exception as ex:
#             print(f"Error al obtener registro: {ex}")
#             return None

#     def obtener_materiales_de_cotizacion(self, id_cotizacion: int) -> Optional[List[Dict]]:
#         """Obtiene todos los materiales de una cotización"""
#         try:
#             sql = f"""
#                 SELECT id_cotizacion_material, id_cotizacion, 
#                        id_proveedor_material, cantidad 
#                 FROM {self.table_name} 
#                 WHERE id_cotizacion = ?
#             """
#             with self.conn.cursor() as cursor:
#                 cursor.execute(sql, id_cotizacion)
#                 rows = cursor.fetchall()
#                 return [
#                     {
#                         "id_cotizacion_material": row.id_cotizacion_material,
#                         "id_cotizacion": row.id_cotizacion,
#                         "id_proveedor_material": row.id_proveedor_material,
#                         "cantidad": float(row.cantidad)  # Convertimos a float
#                     }
#                     for row in rows
#                 ] if rows else None
#         except Exception as ex:
#             print(f"Error al obtener materiales: {ex}")
#             return None

#     def actualizar_cantidad(self, id_cotizacion_material: int, nueva_cantidad: float) -> bool:
#         """Actualiza la cantidad de un material"""
#         try:
#             # Redondeamos a 2 decimales
#             cantidad_redondeada = round(float(nueva_cantidad), 2)
            
#             sql = f"""
#                 UPDATE {self.table_name} 
#                 SET cantidad = ? 
#                 WHERE id_cotizacion_material = ?
#             """
#             with self.conn.cursor() as cursor:
#                 cursor.execute(sql, cantidad_redondeada, id_cotizacion_material)
#                 self.conn.commit()
#                 return cursor.rowcount > 0
#         except Exception as ex:
#             print(f"Error al actualizar cantidad: {ex}")
#             self.conn.rollback()
#             return False

#     def eliminar_material(self, id_cotizacion_material: int) -> bool:
#         """Elimina un material de la cotización"""
#         try:
#             sql = f"DELETE FROM {self.table_name} WHERE id_cotizacion_material = ?"
#             with self.conn.cursor() as cursor:
#                 cursor.execute(sql, id_cotizacion_material)
#                 self.conn.commit()
#                 return cursor.rowcount > 0
#         except Exception as ex:
#             print(f"Error al eliminar material: {ex}")
#             self.conn.rollback()
#             return False




# cotizacion_material_repository.py
import pyodbc
from decimal import Decimal
from typing import Optional, List, Dict
from Models.cotizacion_material import CotizacionMaterial  # Asegúrate que esta ruta sea correcta

class CotizacionMaterialRepository:
    def __init__(self, connection_string: str):
        """Inicializa el repositorio con la cadena de conexión"""
        if not connection_string:
            raise ValueError("Se requiere una conexión pyodbc válida")
        self.connection_string = connection_string
        self.conn = self._get_connection()
        self.table_name = "Cotizacion_Material"

    def _get_connection(self):
        """Crea y devuelve la conexión con la base de datos"""
        return pyodbc.connect(self.connection_string)

    def agregar_material(self, id_cotizacion: int, id_proveedor_material: Optional[int], cantidad: float) -> bool:
        """Agrega un nuevo material a una cotización"""
        try:
            cantidad_redondeada = round(float(cantidad), 2)
            sql = f"""
                INSERT INTO {self.table_name} 
                (id_cotizacion, id_proveedor_material, cantidad)
                VALUES (?, ?, ?)
            """
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (
                    int(id_cotizacion),
                    int(id_proveedor_material) if id_proveedor_material is not None else None,
                    cantidad_redondeada
                ))
                self.conn.commit()
                return True
        except Exception as e:
            print(f"❌ Error al agregar material: {str(e)}")
            self.conn.rollback()
            return False

    def obtener_cotizacion_material(self, id_cotizacion_material: int) -> Optional[Dict]:
        """Obtiene un material de cotización por su ID"""
        try:
            sql = f"""
                SELECT id_cotizacion_material, id_cotizacion, 
                       id_proveedor_material, cantidad 
                FROM {self.table_name} 
                WHERE id_cotizacion_material = ?
            """
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (id_cotizacion_material,))
                row = cursor.fetchone()
                if row:
                    return {
                        "id_cotizacion_material": row.id_cotizacion_material,
                        "id_cotizacion": row.id_cotizacion,
                        "id_proveedor_material": row.id_proveedor_material,
                        "cantidad": float(row.cantidad)
                    }
                return None
        except Exception as e:
            print(f"❌ Error al obtener cotización material: {str(e)}")
            return None

    def obtener_materiales_de_cotizacion(self, id_cotizacion: int) -> Optional[List[Dict]]:
        """Obtiene todos los materiales de una cotización"""
        try:
            sql = f"""
                SELECT id_cotizacion_material, id_cotizacion, 
                       id_proveedor_material, cantidad 
                FROM {self.table_name} 
                WHERE id_cotizacion = ?
            """
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (id_cotizacion,))
                rows = cursor.fetchall()
                if rows:
                    return [
                        {
                            "id_cotizacion_material": row.id_cotizacion_material,
                            "id_cotizacion": row.id_cotizacion,
                            "id_proveedor_material": row.id_proveedor_material,
                            "cantidad": float(row.cantidad)
                        }
                        for row in rows
                    ]
                return None
        except Exception as e:
            print(f"❌ Error al obtener materiales de cotización: {str(e)}")
            return None

    def actualizar_cantidad(self, id_cotizacion_material: int, nueva_cantidad: float) -> bool:
        """Actualiza la cantidad de un material en cotización"""
        try:
            cantidad_redondeada = round(float(nueva_cantidad), 2)
            sql = f"""
                UPDATE {self.table_name} 
                SET cantidad = ? 
                WHERE id_cotizacion_material = ?
            """
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (cantidad_redondeada, id_cotizacion_material))
                self.conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"❌ Error al actualizar cantidad: {str(e)}")
            self.conn.rollback()
            return False

    def eliminar_material(self, id_cotizacion_material: int) -> bool:
        """Elimina un material de la cotización"""
        try:
            sql = f"DELETE FROM {self.table_name} WHERE id_cotizacion_material = ?"
            with self.conn.cursor() as cursor:
                cursor.execute(sql, (id_cotizacion_material,))
                self.conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"❌ Error al eliminar material: {str(e)}")
            self.conn.rollback()
            return False
