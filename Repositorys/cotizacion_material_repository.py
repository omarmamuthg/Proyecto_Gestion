# repositorio cotizacion_material
import pyodbc
from decimal import Decimal
from typing import Optional, List
from Models.cotizacion_material import CotizacionMaterial  # Asegúrate de que la ruta al modelo sea correcta

# class CotizacionMaterialRepository:

#     def __init__(self, conn: pyodbc.Connection):
#         self.conn = conn
#         self.cursor = self.conn.cursor()
#         self.table_name = "Cotizacion_Material"

#     # def agregar_material(self, id_cotizacion: int, id_proveedor_material: Optional[int], cantidad: Decimal) -> bool:
#     #     """Agrega un nuevo registro a la tabla Cotizacion_Material."""
#     #     try:
#     #         sql = f"""
#     #             INSERT INTO {self.table_name} (id_cotizacion, id_proveedor_material, cantidad)
#     #             VALUES (?, ?, ?)
#     #         """
#     #         self.cursor.execute(sql, id_cotizacion, id_proveedor_material, cantidad)
#     #         self.conn.commit()
#     #         return True
#     #     except pyodbc.Error as ex:
#     #         sqlstate = ex.args[0]
#     #         print(f"Error al agregar material a la cotización: {sqlstate}")
#     #         self.conn.rollback()
#     #         return False
#     def agregar_material(self, id_cotizacion: int, id_proveedor_material: Optional[int], cantidad: Decimal) -> bool:
#         """Agrega un nuevo registro a la tabla Cotizacion_Material."""
#         try:
#             # Convertir el Decimal a string primero
#             cantidad_str = str(cantidad)
            
#             sql = f"""
#                 INSERT INTO {self.table_name} (id_cotizacion, id_proveedor_material, cantidad)
#                 VALUES (?, ?, CONVERT(DECIMAL(18,2), ?))
#             """
#             # Ejecutar con los parámetros convertidos adecuadamente
#             params = (
#                 int(id_cotizacion),
#                 int(id_proveedor_material) if id_proveedor_material is not None else None,
#                 cantidad_str  # Enviar como string
#             )
            
#             self.cursor.execute(sql, params)
#             self.conn.commit()
#             return True
#         except pyodbc.Error as ex:
#             print(f"Error SQL al agregar material: {ex}")
#             self.conn.rollback()
#             return False
#         except Exception as ex:
#             print(f"Error inesperado al agregar material: {ex}")
#             self.conn.rollback()
#             return False

#     def obtener_cotizacion_material(self, id_cotizacion_material: int) -> Optional[dict]:
#         """Obtiene un registro de Cotizacion_Material por su ID."""
#         try:
#             sql = f"SELECT id_cotizacion_material, id_cotizacion, id_proveedor_material, cantidad FROM {self.table_name} WHERE id_cotizacion_material = ?"
#             self.cursor.execute(sql, id_cotizacion_material)
#             row = self.cursor.fetchone()
#             if row:
#                 return {
#                     "id_cotizacion_material": row[0],
#                     "id_cotizacion": row[1],
#                     "id_proveedor_material": row[2],
#                     "cantidad": row[3]
#                 }
#             return None
#         except pyodbc.Error as ex:
#             sqlstate = ex.args[0]
#             print(f"Error al obtener Cotizacion_Material: {sqlstate}")
#             return None

#     def obtener_materiales_de_cotizacion(self, id_cotizacion: int) -> Optional[List[dict]]:
#         """Obtiene todos los registros de Cotizacion_Material asociados a una cotización."""
#         try:
#             sql = f"SELECT id_cotizacion_material, id_cotizacion, id_proveedor_material, cantidad FROM {self.table_name} WHERE id_cotizacion = ?"
#             self.cursor.execute(sql, id_cotizacion)
#             rows = self.cursor.fetchall()
#             if rows:
#                 return [
#                     {
#                         "id_cotizacion_material": row[0],
#                         "id_cotizacion": row[1],
#                         "id_proveedor_material": row[2],
#                         "cantidad": row[3]
#                     }
#                     for row in rows
#                 ]
#             return None
#         except pyodbc.Error as ex:
#             sqlstate = ex.args[0]
#             print(f"Error al obtener materiales de la cotización: {sqlstate}")
#             return None

#     def actualizar_cantidad(self, id_cotizacion_material: int, nueva_cantidad: Decimal) -> bool:
#         """Actualiza la cantidad de un material en una cotización."""
#         try:
#             sql = f"UPDATE {self.table_name} SET cantidad = ? WHERE id_cotizacion_material = ?"
#             self.cursor.execute(sql, nueva_cantidad, id_cotizacion_material)
#             self.conn.commit()
#             return self.cursor.rowcount > 0
#         except pyodbc.Error as ex:
#             sqlstate = ex.args[0]
#             print(f"Error al actualizar la cantidad: {sqlstate}")
#             self.conn.rollback()
#             return False

#     def eliminar_material(self, id_cotizacion_material: int) -> bool:
#         """Elimina un registro de Cotizacion_Material por su ID."""
#         try:
#             sql = f"DELETE FROM {self.table_name} WHERE id_cotizacion_material = ?"
#             self.cursor.execute(sql, id_cotizacion_material)
#             self.conn.commit()
#             return self.cursor.rowcount > 0
#         except pyodbc.Error as ex:
#             sqlstate = ex.args[0]
#             print(f"Error al eliminar el material: {sqlstate}")
#             self.conn.rollback()
#             return False

#     # Puedes agregar más métodos según tus necesidades, como obtener por combinación de id_cotizacion e id_proveedor_material, etc.

# # Ejemplo de cómo podrías usar este repositorio (necesitarás una conexión a la base de datos):
# if __name__ == "__main__":
#     # Reemplaza con tu cadena de conexión real
#     connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tu_servidor;DATABASE=tu_base_de_datos;UID=tu_usuario;PWD=tu_contraseña"
#     try:
#         conn = pyodbc.connect(connection_string)
#         repo = CotizacionMaterialRepository(conn)

#         # Ejemplo de agregar un material
#         agregado = repo.agregar_material(id_cotizacion=1, id_proveedor_material=5, cantidad=Decimal("3.0"))
#         print(f"¿Material agregado?: {agregado}")

#         # Ejemplo de obtener materiales de una cotización
#         materiales = repo.obtener_materiales_de_cotizacion(id_cotizacion=1)
#         if materiales:
#             print("\nMateriales de la cotización 1:")
#             for material in materiales:
#                 print(material)

#         # Ejemplo de actualizar la cantidad
#         actualizado = repo.actualizar_cantidad(id_cotizacion_material=1, nueva_cantidad=Decimal("4.5"))
#         print(f"\n¿Cantidad actualizada?: {actualizado}")

#         # Ejemplo de obtener un registro por ID
#         detalle = repo.obtener_cotizacion_material(id_cotizacion_material=1)
#         if detalle:
#             print("\nDetalle de Cotizacion_Material con ID 1:")
#             print(detalle)

#         # Ejemplo de eliminar un material
#         eliminado = repo.eliminar_material(id_cotizacion_material=1)
#         print(f"\n¿Material eliminado?: {eliminado}")

#     except pyodbc.Error as ex:
#         sqlstate = ex.args[0]
#         print(f"Error de conexión: {sqlstate}")
#     finally:
#         if 'conn' in locals() and conn:
#             conn.close()


import pyodbc
from typing import Optional, List, Dict

class CotizacionMaterialRepository:
    # def __init__(self, db_connection: pyodbc.Connection):
    #     """Inicializa el repositorio con una conexión pyodbc existente"""
    #     if not isinstance(db_connection, pyodbc.Connection):
    #         raise ValueError("Se requiere una conexión pyodbc válida")
        
    #     self.conn = db_connection

    # def __init__(self, connection_string: str):
    #     if not connection_string:
    #         raise ValueError("Se requiere una conexión pyodbc válida")
    #     self.connection_string = connection_string


    def __init__(self, connection_string: str):
        if not connection_string:
            raise ValueError("Se requiere una conexión pyodbc válida")
        self.connection_string = connection_string
        self.conn = self._get_connection()  # Inicializa la conexión
        self.table_name = "Cotizacion_Material"  # Define el nombre de la tabla si lo necesitas

    # def _get_connection(self):
    #     # Crear la conexión con la cadena de conexión
    #     print(f"Conectando con: {self.connection_string}")
    #     return pyodbc.connect(self.connection_string)

    def _get_connection(self):
        print(f"Intentando conectar con connection_string: {self.connection_string}")
        return pyodbc.connect(self.connection_string)


    def agregar_material(self, id_cotizacion: int, id_proveedor_material: Optional[int], cantidad: float) -> bool:
        """Agrega un nuevo registro usando float"""
        try:
            # Redondeamos a 2 decimales para consistencia
            cantidad_redondeada = round(float(cantidad), 2)
            
            sql = f"""
                INSERT INTO {self.table_name} 
                (id_cotizacion, id_proveedor_material, cantidad)
                VALUES (?, ?, ?)
            """
            params = (
                int(id_cotizacion),
                int(id_proveedor_material) if id_proveedor_material is not None else None,
                cantidad_redondeada
            )
            
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params)
                self.conn.commit()
                return True
                
        except pyodbc.Error as ex:
            print(f"Error SQL al agregar material: {ex}")
            self.conn.rollback()
            return False
        except Exception as ex:
            print(f"Error inesperado al agregar material: {ex}")
            self.conn.rollback()
            return False

    def obtener_cotizacion_material(self, id_cotizacion_material: int) -> Optional[Dict]:
        """Obtiene un registro por su ID"""
        try:
            sql = f"""
                SELECT id_cotizacion_material, id_cotizacion, 
                       id_proveedor_material, cantidad 
                FROM {self.table_name} 
                WHERE id_cotizacion_material = ?
            """
            with self.conn.cursor() as cursor:
                cursor.execute(sql, id_cotizacion_material)
                row = cursor.fetchone()
                if row:
                    return {
                        "id_cotizacion_material": row.id_cotizacion_material,
                        "id_cotizacion": row.id_cotizacion,
                        "id_proveedor_material": row.id_proveedor_material,
                        "cantidad": float(row.cantidad)  # Convertimos a float
                    }
                return None
        except Exception as ex:
            print(f"Error al obtener registro: {ex}")
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
                cursor.execute(sql, id_cotizacion)
                rows = cursor.fetchall()
                return [
                    {
                        "id_cotizacion_material": row.id_cotizacion_material,
                        "id_cotizacion": row.id_cotizacion,
                        "id_proveedor_material": row.id_proveedor_material,
                        "cantidad": float(row.cantidad)  # Convertimos a float
                    }
                    for row in rows
                ] if rows else None
        except Exception as ex:
            print(f"Error al obtener materiales: {ex}")
            return None

    def actualizar_cantidad(self, id_cotizacion_material: int, nueva_cantidad: float) -> bool:
        """Actualiza la cantidad de un material"""
        try:
            # Redondeamos a 2 decimales
            cantidad_redondeada = round(float(nueva_cantidad), 2)
            
            sql = f"""
                UPDATE {self.table_name} 
                SET cantidad = ? 
                WHERE id_cotizacion_material = ?
            """
            with self.conn.cursor() as cursor:
                cursor.execute(sql, cantidad_redondeada, id_cotizacion_material)
                self.conn.commit()
                return cursor.rowcount > 0
        except Exception as ex:
            print(f"Error al actualizar cantidad: {ex}")
            self.conn.rollback()
            return False

    def eliminar_material(self, id_cotizacion_material: int) -> bool:
        """Elimina un material de la cotización"""
        try:
            sql = f"DELETE FROM {self.table_name} WHERE id_cotizacion_material = ?"
            with self.conn.cursor() as cursor:
                cursor.execute(sql, id_cotizacion_material)
                self.conn.commit()
                return cursor.rowcount > 0
        except Exception as ex:
            print(f"Error al eliminar material: {ex}")
            self.conn.rollback()
            return False