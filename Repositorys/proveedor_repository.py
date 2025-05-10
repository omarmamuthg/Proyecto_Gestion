#Repositorio proveedor
import pyodbc
from datetime import datetime
from typing import List, Optional
from Models.proveedor import Proveedor

class ProveedorRepository:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.table_name = "Proveedores"  # Agregamos el nombre de la tabla

    def _get_connection(self):
        return pyodbc.connect(self.connection_string)  # Corregimos para crear una conexión real

    def create_proveedor(self, proveedor: Proveedor) -> Proveedor:
        query = """
        INSERT INTO Proveedores (
            nombre, contacto, telefono, correo, rfc, direccion, fecha_registro, activo
        ) 
        OUTPUT INSERTED.id_proveedor
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            proveedor.nombre,
            proveedor.contacto,
            proveedor.telefono,
            proveedor.correo,
            proveedor.rfc,
            proveedor.direccion,
            proveedor.fecha_registro or datetime.now(),
            proveedor.activo
        )

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            inserted_id = cursor.fetchone()[0]
            conn.commit()
            
            # Obtener el proveedor recién creado
            return self.get_proveedor(inserted_id)

    def get_proveedor(self, id_proveedor: int) -> Optional[Proveedor]:
        query = "SELECT * FROM Proveedores WHERE id_proveedor = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, id_proveedor)
            row = cursor.fetchone()
            
            if row:
                return self._row_to_proveedor(row)
            return None

    def get_all_proveedores(self, activos_only: bool = True) -> List[Proveedor]:
        query = "SELECT * FROM Proveedores"
        if activos_only:
            query += " WHERE activo = 1"
            
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [self._row_to_proveedor(row) for row in cursor.fetchall()]

    def update_proveedor(self, id_proveedor: int, proveedor: Proveedor) -> Optional[Proveedor]:
        query = """
        UPDATE Proveedores 
        SET 
            nombre = ?,
            contacto = ?,
            telefono = ?,
            correo = ?,
            rfc = ?,
            direccion = ?,
            activo = ?
        WHERE id_proveedor = ?
        """
        
        params = (
            proveedor.nombre,
            proveedor.contacto,
            proveedor.telefono,
            proveedor.correo,
            proveedor.rfc,
            proveedor.direccion,
            proveedor.activo,
            id_proveedor
        )

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            
            if cursor.rowcount > 0:
                return self.get_proveedor(id_proveedor)
            return None

    def delete_proveedor(self, id_proveedor: int) -> bool:
        # En lugar de borrar físicamente, marcamos como inactivo
        query = "UPDATE Proveedores SET activo = 0 WHERE id_proveedor = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, id_proveedor)
            conn.commit()
            return cursor.rowcount > 0

    def _row_to_proveedor(self, row) -> Proveedor:
        return Proveedor(
            id_proveedor=row.id_proveedor,
            nombre=row.nombre,
            contacto=row.contacto,
            telefono=row.telefono,
            correo=row.correo,
            rfc=row.rfc,
            direccion=row.direccion,
            fecha_registro=row.fecha_registro,
            activo=bool(row.activo)
        )

    def obtener_proveedor(self, id_proveedor: int) -> Optional[Proveedor]:
        """Alias en español para get_proveedor"""
        return self.get_proveedor(id_proveedor)

    def obtener_proveedores(self):
        """Obtiene todos los proveedores activos"""
        try:
            sql = """
                SELECT id_proveedor, nombre, direccion, telefono, correo, rfc, activo
                FROM Proveedores
                WHERE activo = 1
                ORDER BY nombre
            """
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                rows = cursor.fetchall()
                return [
                    {
                        "id_proveedor": row.id_proveedor,
                        "nombre": row.nombre,
                        "direccion": row.direccion,
                        "telefono": row.telefono,
                        "email": row.correo,  # Cambiado de email a correo para coincidir con la base de datos
                        "rfc": row.rfc,
                        "activo": row.activo
                    }
                    for row in rows
                ] if rows else []
        except Exception as e:
            print(f"❌ Error al obtener proveedores: {str(e)}")
            return []