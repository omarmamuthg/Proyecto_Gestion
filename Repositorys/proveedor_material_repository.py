# Repositorio proveedor_material
import pyodbc
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import List, Dict, Union
from typing import  Optional


class ProveedorMaterialRepository:

    # def __init__(self, connection):
    #     self.conn = connection  # ✅ Usa directamente la conexión ya creada
    #     self.table_name = "Proveedor_Material"
        

    # # def _get_connection(self):
    # #     """Crea y devuelve la conexión con la base de datos"""
    # #     # print(f"Conectando con: {self.connection_string}")
    # #     return pyodbc.connect(self.connection_string)
    # def _get_connection(self):
    #     """Devuelve la conexión ya establecida"""
    #     return self.conn  # Devuelve la conexión existente


    # def obtener_vinculo(self, id_proveedor_material: int):
    #     query = "SELECT * FROM Proveedor_Material WHERE id_proveedor_material = ?"
        
    #     cursor = self.conn.cursor()  # Usamos la conexión existente
    #     cursor.execute(query, (id_proveedor_material,))
    #     result = cursor.fetchone()
    #     cursor.close()
    #     return result

    # def _normalizar_precio(self, valor) -> float:
    #     """Convierte cualquier valor a tipo float"""
    #     if isinstance(valor, Decimal):
    #         return float(valor)
    #     return float(valor)  # Para otros tipos como str o int


    # def vincular_material_a_proveedor(self, id_proveedor, id_material, precio):
    #     try:
    #         id_proveedor_int = int(id_proveedor)
    #         id_material_int = int(id_material)

    #         if isinstance(precio, Decimal):
    #             precio_float = float(str(precio))
    #         elif isinstance(precio, str):
    #             precio_float = float(precio.replace(',', '.'))
    #         else:
    #             precio_float = float(precio)
                
    #         precio_float = round(precio_float, 2)

    #         conn = self._get_connection()  # Obtener la conexión
    #         cursor = conn.cursor()
    #         cursor.execute(
    #             """
    #             INSERT INTO Proveedor_Material 
    #             (id_proveedor, id_material, precio, activo) 
    #             VALUES (?, ?, ?, ?)
    #             """,
    #             (id_proveedor_int, id_material_int, precio_float, 1)
    #         )
    #         conn.commit()
    #         cursor.close()
    #         conn.close()
    #         return True
    #     except Exception as e:
    #         print(f"❌ Error inesperado: {str(e)}")
    #         conn.rollback()
    #         cursor.close()
    #         conn.close()
    #         return False

    def __init__(self, connection):
        self.conn = connection  # Usa directamente la conexión ya creada
        self.table_name = "Proveedor_Material"

    def _get_connection(self):
        """Devuelve la conexión ya establecida"""
        return self.conn  # Devuelve la conexión existente

    def obtener_vinculo(self, id_proveedor_material: int):
        query = "SELECT * FROM Proveedor_Material WHERE id_proveedor_material = ?"
        
        cursor = self.conn.cursor()  # Usamos la conexión existente
        cursor.execute(query, (id_proveedor_material,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def _normalizar_precio(self, valor) -> float:
        """Convierte cualquier valor a tipo float"""
        if isinstance(valor, Decimal):
            return float(valor)
        return float(valor)  # Para otros tipos como str o int

    def vincular_material_a_proveedor(self, id_proveedor, id_material, precio):
        try:
            id_proveedor_int = int(id_proveedor)
            id_material_int = int(id_material)

            if isinstance(precio, Decimal):
                precio_float = float(str(precio))
            elif isinstance(precio, str):
                precio_float = float(precio.replace(',', '.'))
            else:
                precio_float = float(precio)
                
            precio_float = round(precio_float, 2)

            cursor = self.conn.cursor()  # Obtener la conexión
            cursor.execute(
                """
                INSERT INTO Proveedor_Material 
                (id_proveedor, id_material, precio, activo) 
                VALUES (?, ?, ?, ?)
                """,
                (id_proveedor_int, id_material_int, precio_float, 1)
            )
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            self.conn.rollback()
            cursor.close()
            return False



    def obtener_materiales_de_proveedor(self, id_proveedor: int) -> List[Dict]:
        """Obtiene todos los materiales asociados a un proveedor"""
        try:
            cursor = self.conn.cursor()
            try:
                cursor.execute(
                    """
                    SELECT m.*, pm.precio AS precio_proveedor
                    FROM Materiales m
                    JOIN Proveedor_Material pm ON m.id_material = pm.id_material
                    WHERE pm.id_proveedor = ? AND pm.activo = 1
                    """,
                    (int(id_proveedor),)
                )

                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            finally:
                cursor.close()

        except pyodbc.Error as e:
            print(f"❌ Error al obtener materiales: {str(e)}")
            return []
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return []

    def obtener_proveedores_de_material(self, id_material: int) -> List[Dict]:
        """Obtiene todos los proveedores que ofrecen un material específico"""
        try:
            cursor = self.conn.cursor()
            try:
                cursor.execute(
                    """
                    SELECT 
                        pm.id_proveedor_material,
                        p.nombre,
                        pm.precio,
                        p.id_proveedor
                    FROM Proveedores p
                    JOIN Proveedor_Material pm ON p.id_proveedor = pm.id_proveedor
                    WHERE pm.id_material = ? AND pm.activo = 1 AND p.activo = 1
                    ORDER BY p.nombre
                    """,
                    (int(id_material),)
                )

                columns = [column[0] for column in cursor.description]
                results = []
                for row in cursor.fetchall():
                    result = dict(zip(columns, row))
                    # Asegurarse de que el precio sea un float
                    if 'precio' in result:
                        result['precio'] = float(result['precio'])
                    results.append(result)
                return results
            finally:
                cursor.close()

        except pyodbc.Error as e:
            print(f"❌ Error al obtener proveedores: {str(e)}")
            return []
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return []

    def desvincular_material_proveedor(self, id_proveedor: int, id_material: int) -> bool:
        """Desvincula un material de un proveedor (marca como inactivo)"""
        try:
            cursor = self.conn.cursor()
            try:
                cursor.execute(
                    """
                    UPDATE Proveedor_Material 
                    SET activo = 0 
                    WHERE id_proveedor = ? AND id_material = ?
                    """,
                    (int(id_proveedor), int(id_material))
                )
                self.conn.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()

        except pyodbc.Error as e:
            print(f"❌ Error al desvincular: {str(e)}")
            self.conn.rollback()
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            self.conn.rollback()
            return False

    def actualizar_precio_material(self, id_proveedor: int, id_material: int, nuevo_precio: Union[float, Decimal]) -> bool:
        """Actualiza el precio de un material para un proveedor específico"""
        try:
            cursor = self.conn.cursor()
            try:
                cursor.execute(
                    """
                    UPDATE Proveedor_Material 
                    SET precio = ? 
                    WHERE id_proveedor = ? AND id_material = ? AND activo = 1
                    """,
                    (
                        self._normalizar_precio(nuevo_precio),
                        int(id_proveedor),
                        int(id_material)
                    )
                )
                self.conn.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()

        except pyodbc.Error as e:
            print(f"❌ Error al actualizar precio: {str(e)}")
            self.conn.rollback()
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            self.conn.rollback()
            return False
        
    def obtener_vinculo(self, id_proveedor_material):
        """
        Obtiene un vínculo específico entre proveedor y material por su ID
        """
        try:
            query = """
            SELECT * FROM Proveedor_Material
            WHERE id_proveedor_material = ?
            """
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (id_proveedor_material,))
                row = cursor.fetchone()
                
                if row:
                    from Models.proveedor_material import ProveedorMaterial
                    return ProveedorMaterial(
                        id_proveedor_material=row.id_proveedor_material,
                        id_proveedor=row.id_proveedor,
                        id_material=row.id_material,
                        precio=row.precio,
                        activo=bool(row.activo)
                    )
                return None
        except Exception as e:
            print(f"❌ Error al obtener vínculo proveedor-material: {str(e)}")
            return None