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

    # def obtener_materiales_por_cotizacion(self, id_cotizacion):
    #     """
    #     Obtiene todos los materiales asociados a una cotización
    #     """
    #     try:
    #         cursor = self.conn.cursor()
    #         try:
    #             cursor.execute(
    #                 """
    #                 SELECT cm.*, m.nombre as nombre_material, m.unidad_medida, 
    #                     pm.precio as precio_unitario
    #                 FROM Cotizacion_Material cm
    #                 JOIN Materiales m ON cm.id_material = m.id_material
    #                 LEFT JOIN Proveedor_Material pm ON cm.id_proveedor_material = pm.id_proveedor_material
    #                 WHERE cm.id_cotizacion = ?
    #                 """,
    #                 (id_cotizacion,)
    #             )
                
    #             materiales = []
    #             columns = [column[0] for column in cursor.description]
                
    #             for row in cursor.fetchall():
    #                 material = {}
    #                 for i, value in enumerate(row):
    #                     material[columns[i]] = value
    #                 materiales.append(material)
                    
    #             return materiales
    #         finally:
    #             cursor.close()
    #     except Exception as e:
    #         print(f"❌ Error al obtener materiales de cotización: {str(e)}")
    #         return []
    # def obtener_materiales_por_cotizacion(self, id_cotizacion):
    #     """
    #     Obtiene todos los materiales asociados a una cotización
    #     """
    #     try:
    #         cursor = self.conn.cursor()
    #         try:
    #             cursor.execute(
    #                 """
    #                 SELECT cm.*, m.nombre as nombre_material, m.unidad_medida, 
    #                     pm.precio as precio_unitario, m.id_material
    #                 FROM Cotizacion_Material cm
    #                 JOIN Materiales m ON cm.id_material = m.id_material
    #                 LEFT JOIN Proveedor_Material pm ON cm.id_proveedor_material = pm.id_proveedor_material
    #                 WHERE cm.id_cotizacion = ?
    #                 """,
    #                 (id_cotizacion,)
    #             )
                
    #             materiales = []
    #             columns = [column[0] for column in cursor.description]
                
    #             for row in cursor.fetchall():
    #                 material = {}
    #                 for i, value in enumerate(row):
    #                     material[columns[i]] = value
    #                 materiales.append(material)
                    
    #             return materiales
    #         finally:
    #             cursor.close()
    #     except Exception as e:
    #         print(f"❌ Error al obtener materiales de cotización: {str(e)}")
    #         return []




    # def obtener_materiales_por_cotizacion(self, id_cotizacion):
    #     """
    #     Obtiene todos los materiales asociados a una cotización
    #     """
    #     try:
    #         cursor = self.conn.cursor()
    #         try:
    #             cursor.execute(
    #                 """
    #                 SELECT 
    #                     cm.id_cotizacion_material,
    #                     cm.id_cotizacion,
    #                     cm.id_material,
    #                     cm.cantidad,
    #                     cm.id_proveedor_material,
    #                     m.nombre as nombre_material,
    #                     m.unidad_medida,
    #                     m.descripcion as descripcion_material,
    #                     pm.precio as precio_unitario,
    #                     p.nombre as nombre_proveedor
    #                 FROM Cotizacion_Material cm
    #                 JOIN Materiales m ON cm.id_material = m.id_material
    #                 LEFT JOIN Proveedor_Material pm ON cm.id_proveedor_material = pm.id_proveedor_material
    #                 LEFT JOIN Proveedores p ON pm.id_proveedor = p.id_proveedor
    #                 WHERE cm.id_cotizacion = ?
    #                 """,
    #                 (id_cotizacion,)
    #             )
                
    #             materiales = []
    #             columns = [column[0] for column in cursor.description]
                
    #             for row in cursor.fetchall():
    #                 material = {}
    #                 for i, value in enumerate(row):
    #                     material[columns[i]] = value
    #                 materiales.append(material)
                    
    #             return materiales
    #         finally:
    #             cursor.close()
    #     except Exception as e:
    #         print(f"❌ Error al obtener materiales de cotización: {str(e)}")
    #         return []
    # def obtener_materiales_por_cotizacion(self, id_cotizacion):
    #     """
    #     Obtiene todos los materiales asociados a una cotización
    #     """
    #     try:
    #         cursor = self.conn.cursor()
    #         try:
    #             cursor.execute(
    #                 """
    #                 SELECT 
    #                     cm.id_cotizacion_material,
    #                     cm.id_cotizacion,
    #                     cm.id_material,
    #                     cm.cantidad,
    #                     cm.id_proveedor_material,
    #                     m.nombre as nombre_material,
    #                     m.unidad_medida,
    #                     pm.precio as precio_unitario
    #                 FROM Cotizacion_Material cm
    #                 JOIN Materiales m ON cm.id_material = m.id_material
    #                 LEFT JOIN Proveedor_Material pm ON cm.id_proveedor_material = pm.id_proveedor_material
    #                 WHERE cm.id_cotizacion = ?
    #                 """,
    #                 (id_cotizacion,)
    #             )
                
    #             materiales = []
    #             columns = [column[0] for column in cursor.description]
                
    #             for row in cursor.fetchall():
    #                 material = {}
    #                 for i, value in enumerate(row):
    #                     material[columns[i]] = value
    #                 materiales.append(material)
                
    #             # Depuración
    #             print(f"Materiales encontrados: {len(materiales)}")
    #             for m in materiales:
    #                 print(f"Material: {m.get('nombre_material')}, Cantidad: {m.get('cantidad')}, Precio: {m.get('precio_unitario')}")
                    
    #             return materiales
    #         finally:
    #             cursor.close()
    #     except Exception as e:
    #         print(f"❌ Error al obtener materiales de cotización: {str(e)}")
    #         return []

    def obtener_materiales_por_cotizacion(self, id_cotizacion):
        """
        Obtiene todos los materiales asociados a una cotización
        """
        try:
            # Imprimir para depuración
            print(f"Buscando materiales para la cotización ID: {id_cotizacion}")
            
            cursor = self.conn.cursor()
            try:
                # Consulta SQL mejorada con INNER JOIN para asegurar que obtenemos todos los datos necesarios
                query = """
                SELECT 
                    cm.id_cotizacion_material,
                    cm.id_cotizacion,
                    cm.cantidad,
                    cm.id_proveedor_material,
                    m.id_material,
                    m.nombre as nombre_material,
                    m.unidad_medida,
                    m.descripcion,
                    pm.precio as precio_unitario,
                    p.nombre as nombre_proveedor
                FROM Cotizacion_Material cm
                INNER JOIN Proveedor_Material pm ON cm.id_proveedor_material = pm.id_proveedor_material
                INNER JOIN Materiales m ON pm.id_material = m.id_material
                INNER JOIN Proveedores p ON pm.id_proveedor = p.id_proveedor
                WHERE cm.id_cotizacion = ?
                """
                
                # Imprimir la consulta para depuración
                print(f"Ejecutando consulta: {query}")
                
                cursor.execute(query, (id_cotizacion,))
                
                # Obtener los nombres de las columnas
                columns = [column[0] for column in cursor.description]
                print(f"Columnas encontradas: {columns}")
                
                # Obtener todas las filas
                rows = cursor.fetchall()
                print(f"Número de filas encontradas: {len(rows)}")
                
                materiales = []
                for row in rows:
                    material = {}
                    for i, value in enumerate(row):
                        material[columns[i]] = value
                    materiales.append(material)
                    print(f"Material agregado: {material}")
                
                return materiales
            finally:
                cursor.close()
        except Exception as e:
            print(f"❌ Error al obtener materiales de cotización: {str(e)}")
            import traceback
            traceback.print_exc()
            return []