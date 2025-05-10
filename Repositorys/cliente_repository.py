
#cliente repository
import pyodbc
from datetime import datetime
from typing import List, Optional
from Models.cliente import Cliente  # Asegúrate de que la clase Cliente esté en este path

class ClienteRepository:
    # def __init__(self, connection_string: str):
    #     self.connection_string = connection_string

    # def _get_connection(self):
    #     return pyodbc.connect(self.connection_string)
    def __init__(self, connection):
        self.connection = connection

    def _get_connection(self):
        return self.connection

    def create_cliente(self, cliente: Cliente) -> Cliente:
        query = """
        INSERT INTO Clientes (
            nombre, correo, telefono, tipo_cliente, direccion, rfc, fecha_registro, activo, comentarios
        ) 
        OUTPUT INSERTED.id_cliente
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        params = (
            cliente.nombre,
            cliente.correo,
            cliente.telefono,
            cliente.tipo_cliente,
            cliente.direccion,
            cliente.rfc,
            cliente.fecha_registro or datetime.now(),  # Si no viene, usa la fecha actual
            cliente.activo,
            cliente.comentarios
        )

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            inserted_id = cursor.fetchone()[0]
            conn.commit()
            
            # Retorna el cliente recién creado
            return self.get_cliente(inserted_id)

    def get_cliente(self, id_cliente: int) -> Optional[Cliente]:
        query = "SELECT * FROM Clientes WHERE id_cliente = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, id_cliente)
            row = cursor.fetchone()
            
            if row:
                return self._row_to_cliente(row)
            return None

    def get_all_clientes(self, activos_only: bool = True) -> List[Cliente]:
        query = "SELECT * FROM Clientes"
        if activos_only:
            query += " WHERE activo = 1"
            
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [self._row_to_cliente(row) for row in cursor.fetchall()]

    def update_cliente(self, id_cliente: int, cliente: Cliente) -> Optional[Cliente]:
        query = """
        UPDATE Clientes 
        SET 
            nombre = ?,
            correo = ?,
            telefono = ?,
            tipo_cliente = ?,
            direccion = ?,
            rfc = ?,
            activo = ?,
            comentarios = ?
        WHERE id_cliente = ?
        """
        
        params = (
            cliente.nombre,
            cliente.correo,
            cliente.telefono,
            cliente.tipo_cliente,
            cliente.direccion,
            cliente.rfc,
            cliente.activo,
            cliente.comentarios,
            id_cliente
        )

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            
            if cursor.rowcount > 0:
                return self.get_cliente(id_cliente)
            return None

    def delete_cliente(self, id_cliente: int) -> bool:
        # Marcamos como inactivo en lugar de borrar físicamente
        query = "UPDATE Clientes SET activo = 0 WHERE id_cliente = ?"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, id_cliente)
            conn.commit()
            return cursor.rowcount > 0

    def _row_to_cliente(self, row) -> Cliente:
        return Cliente(
            id_cliente=row.id_cliente,
            nombre=row.nombre,
            correo=row.correo,
            telefono=row.telefono,
            tipo_cliente=row.tipo_cliente,
            direccion=row.direccion,
            rfc=row.rfc,
            fecha_registro=row.fecha_registro,
            activo=bool(row.activo),
            comentarios=row.comentarios
        )