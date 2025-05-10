# #material repositorio
# import pyodbc
# from datetime import datetime
# from typing import List, Optional
# from decimal import Decimal
# from Models.material import Material  # Asegúrate de que la clase Material esté en este path

# class MaterialRepository:
#     def __init__(self, connection_string: str):
#         self.connection_string = connection_string

#     def _get_connection(self):
#         return pyodbc.connect(self.connection_string)

#     def create_material(self, material: Material) -> Material:
#         query = """
#         INSERT INTO Materiales (
#             nombre, descripcion, unidad_medida, marca, categoria, fecha_registro
#         )
#         OUTPUT INSERTED.id_material
#         VALUES (?, ?, ?, ?, ?, ?)
#         """

#         params = (
#             material.nombre,
#             material.descripcion,
#             material.unidad_medida,
#             material.marca,
#             material.categoria,
#             material.fecha_registro or datetime.now(),  # Si no viene, usa la fecha actual
#         )

#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, params)
#             inserted_id = cursor.fetchone()[0]
#             conn.commit()

#             # Retorna el material recién creado
#             return self.get_material(inserted_id)

#     def get_material(self, id_material: int) -> Optional[Material]:
#         query = "SELECT * FROM Materiales WHERE id_material = ?"
        
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, id_material)
#             row = cursor.fetchone()
            
#             if row:
#                 return self._row_to_material(row)
#             return None

#     # def get_all_materiales(self) -> List[Material]:
#     #     query = "SELECT * FROM Materiales"
            
#     #     with self._get_connection() as conn:
#     #         cursor = conn.cursor()
#     #         cursor.execute(query)
#     #         return [self._row_to_material(row) for row in cursor.fetchall()]
#     def get_all_materiales(self, activos_only: bool = True) -> List[Material]:
#         """
#         Obtiene todos los materiales de la base de datos
#         Args:
#             activos_only: Si True (por defecto), solo devuelve materiales activos
#         Returns:
#             List[Material]: Lista de objetos Material
#         """
#         query = "SELECT * FROM Materiales"
#         if activos_only:
#             query += " WHERE activo = 1"  # Asume que existe columna 'activo' en tu tabla
        
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query)
#             return [self._row_to_material(row) for row in cursor.fetchall()]

#     def update_material(self, id_material: int, material: Material) -> Optional[Material]:
#         query = """
#         UPDATE Materiales
#         SET
#             nombre = ?,
#             descripcion = ?,
#             unidad_medida = ?,
#             marca = ?,
#             categoria = ?
#         WHERE id_material = ?
#         """

#         params = (
#             material.nombre,
#             material.descripcion,
#             material.unidad_medida,
#             material.marca,
#             material.categoria,
#             id_material
#         )

#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, params)
#             conn.commit()

#             if cursor.rowcount > 0:
#                 return self.get_material(id_material)
#             return None

#     def delete_material(self, id_material: int) -> bool:
#         query = "DELETE FROM Materiales WHERE id_material = ?"
        
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, id_material)
#             conn.commit()
#             return cursor.rowcount > 0

#     def _row_to_material(self, row) -> Material:
#         return Material(
#             id_material=row.id_material,
#             nombre=row.nombre,
#             descripcion=row.descripcion,
#             unidad_medida=row.unidad_medida,
#             # costo_unitario=Decimal(str(row.costo_unitario)),  # Convertir a Decimal
#             marca=row.marca,
#             categoria=row.categoria,
#             fecha_registro=row.fecha_registro
#         )
    
#     # En MaterialRepository.py, agrega:
#     def obtener_por_id(self, id_material: int) -> Optional[Material]:
#         """Alias para compatibilidad"""
#         return self.get_material(id_material)  # O el método equivalente que ya exista
    

#     def obtener_material(self, id_material: int, incluir_inactivos: bool = False) -> Optional[Material]:
#         query = "SELECT * FROM Materiales WHERE id_material = ?"
#         params = [id_material]
        
#         if not incluir_inactivos:
#             query += " AND activo = 1"
            
#         # Ejecutar la consulta y retornar el resultado
    
#     def marcar_como_inactivo(self, id_material: int) -> bool:
#         """Marca un material como inactivo (eliminación lógica)"""
#         try:
#             with self.conn.cursor() as cursor:
#                 cursor.execute(
#                     "UPDATE Materiales SET activo = 0 WHERE id_material = ?",
#                     (id_material,)
#                 )
#                 self.conn.commit()
#                 return cursor.rowcount > 0  # True si afectó alguna fila
#         except pyodbc.Error as e:
#             print(f"Error de BD al desactivar material: {str(e)}")
#             self.conn.rollback()
#             return False
#         except Exception as e:
#             print(f"Error inesperado: {str(e)}")
#             return False
        
#     def obtener_todos_materiales(self, activos_only=True) -> List[Material]:
#         """Debe incluir TODOS los campos necesarios"""
#         return self.repository.get_all_materiales(activos_only)



# MaterialRepository
import pyodbc
from datetime import datetime
from typing import List, Optional
from Models.material import Material

class MaterialRepository:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.table_name = "Materiales"

    def _get_connection(self):
        return pyodbc.connect(self.connection_string)

    def create_material(self, material: Material) -> Material:
        query = """
        INSERT INTO Materiales (
            nombre, descripcion, unidad_medida, marca, categoria, fecha_registro, activo
        ) 
        OUTPUT INSERTED.id_material
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            material.nombre,
            material.descripcion,
            material.unidad_medida,
            material.marca,
            material.categoria,
            material.fecha_registro or datetime.now(),
            material.activo
        )

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            inserted_id = cursor.fetchone()[0]
            conn.commit()
            
            return self.get_material(inserted_id)

    def get_material(self, id_material: int) -> Optional[Material]:
        query = "SELECT * FROM Materiales WHERE id_material = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, id_material)
            row = cursor.fetchone()
            
            if row:
                return self._row_to_material(row)
            return None

    def get_all_materiales(self, activos_only: bool = True) -> List[Material]:
        query = "SELECT * FROM Materiales"
        if activos_only:
            query += " WHERE activo = 1"
            
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [self._row_to_material(row) for row in cursor.fetchall()]

    def update_material(self, id_material: int, material: Material) -> Optional[Material]:
        query = """
        UPDATE Materiales 
        SET 
            nombre = ?,
            descripcion = ?,
            unidad_medida = ?,
            marca = ?,
            categoria = ?,
            activo = ?
        WHERE id_material = ?
        """
        
        params = (
            material.nombre,
            material.descripcion,
            material.unidad_medida,
            material.marca,
            material.categoria,
            material.activo,
            id_material
        )

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            
            if cursor.rowcount > 0:
                return self.get_material(id_material)
            return None

    def delete_material(self, id_material: int) -> bool:
        query = "UPDATE Materiales SET activo = 0 WHERE id_material = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, id_material)
            conn.commit()
            return cursor.rowcount > 0

    def _row_to_material(self, row) -> Material:
        return Material(
            id_material=row.id_material,
            nombre=row.nombre,
            descripcion=row.descripcion,
            unidad_medida=row.unidad_medida,
            marca=row.marca,
            categoria=row.categoria,
            fecha_registro=row.fecha_registro,
            activo=bool(row.activo)
        )

    def obtener_material(self, id_material: int) -> Optional[Material]:
        """Alias en español para get_material"""
        return self.get_material(id_material)

    def obtener_materiales(self):
        """Obtiene todos los materiales activos"""
        try:
            sql = """
                SELECT id_material, nombre, descripcion, unidad_medida, 
                       marca, categoria, fecha_registro, activo
                FROM Materiales
                WHERE activo = 1
                ORDER BY nombre
            """
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                return [
                    {
                        "id_material": row.id_material,
                        "nombre": row.nombre,
                        "descripcion": row.descripcion,
                        "unidad_medida": row.unidad_medida,
                        "marca": row.marca,
                        "categoria": row.categoria,
                        "fecha_registro": row.fecha_registro,
                        "activo": row.activo
                    }
                    for row in rows
                ] if rows else []
        except Exception as e:
            print(f"❌ Error al obtener materiales: {str(e)}")
            return []

    def buscar_por_nombre(self, nombre: str) -> List[Material]:
        query = "SELECT * FROM Materiales WHERE nombre LIKE ? AND activo = 1"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (f"%{nombre}%",))
            rows = cursor.fetchall()
            return [self._row_to_material(row) for row in rows]