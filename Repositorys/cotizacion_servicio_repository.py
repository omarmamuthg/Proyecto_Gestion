import pyodbc
from datetime import datetime
from typing import List, Optional
from Models.cotizacion_servicio import CotizacionServicio  # Asegúrate de que la clase esté en este path

class CotizacionServicioRepository:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def _get_connection(self):
        return pyodbc.connect(self.connection_string)

    def create_cotizacion_servicio(self, cotizacion_servicio: CotizacionServicio) -> CotizacionServicio:
        query = """
        INSERT INTO Cotizacion_Servicio (
            id_cotizacion, nombre_servicio, descripcion_servicio,
            tipo_servicio, costo_servicio, cantidad_servicio, fecha_creacion_servicio,
            activo, usuario_creador_servicio, fecha_actualizacion_servicio
        )
        OUTPUT INSERTED.id_cotizacion_servicio
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        params = (
            cotizacion_servicio.id_cotizacion,
            cotizacion_servicio.nombre_servicio,
            cotizacion_servicio.descripcion_servicio,
            cotizacion_servicio.tipo_servicio,
            cotizacion_servicio.costo_servicio,
            cotizacion_servicio.cantidad_servicio,
            cotizacion_servicio.fecha_creacion_servicio or datetime.now(),
            cotizacion_servicio.activo,
            cotizacion_servicio.usuario_creador_servicio,
            cotizacion_servicio.fecha_actualizacion_servicio
        )

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            inserted_id = cursor.fetchone()[0]
            conn.commit()

            return self.get_cotizacion_servicio(inserted_id)

    def get_cotizacion_servicio(self, id_cotizacion_servicio: int) -> Optional[CotizacionServicio]:
        query = "SELECT * FROM Cotizacion_Servicio WHERE id_cotizacion_servicio = ?"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, id_cotizacion_servicio)
            row = cursor.fetchone()

            if row:
                return self._row_to_cotizacion_servicio(row)
            return None

    def get_servicios_por_cotizacion(self, id_cotizacion: int, activos_only: bool = True) -> List[CotizacionServicio]:
        query = "SELECT * FROM Cotizacion_Servicio WHERE id_cotizacion = ?"
        if activos_only:
            query += " AND activo = 1"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, id_cotizacion)
            return [self._row_to_cotizacion_servicio(row) for row in cursor.fetchall()]

    def update_cotizacion_servicio(self, id_cotizacion_servicio: int, cotizacion_servicio: CotizacionServicio) -> Optional[CotizacionServicio]:
        query = """
        UPDATE Cotizacion_Servicio
        SET
            id_cotizacion = ?,
            nombre_servicio = ?,
            descripcion_servicio = ?,
            tipo_servicio = ?,
            costo_servicio = ?,
            cantidad_servicio = ?,
            fecha_creacion_servicio = ?,
            activo = ?,
            usuario_creador_servicio = ?,
            fecha_actualizacion_servicio = ?
        WHERE id_cotizacion_servicio = ?
        """

        params = (
            cotizacion_servicio.id_cotizacion,
            cotizacion_servicio.nombre_servicio,
            cotizacion_servicio.descripcion_servicio,
            cotizacion_servicio.tipo_servicio,
            cotizacion_servicio.costo_servicio,
            cotizacion_servicio.cantidad_servicio,
            cotizacion_servicio.fecha_creacion_servicio,
            cotizacion_servicio.activo,
            cotizacion_servicio.usuario_creador_servicio,
            cotizacion_servicio.fecha_actualizacion_servicio,
            id_cotizacion_servicio
        )

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            if cursor.rowcount > 0:
                return self.get_cotizacion_servicio(id_cotizacion_servicio)
            return None

    def delete_cotizacion_servicio(self, id_cotizacion_servicio: int) -> bool:
        query = "UPDATE Cotizacion_Servicio SET activo = 0 WHERE id_cotizacion_servicio = ?"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, id_cotizacion_servicio)
            conn.commit()
            return cursor.rowcount > 0

    def _row_to_cotizacion_servicio(self, row) -> CotizacionServicio:
        return CotizacionServicio(
            id_cotizacion_servicio=row.id_cotizacion_servicio,
            id_cotizacion=row.id_cotizacion,
            nombre_servicio=row.nombre_servicio,
            descripcion_servicio=row.descripcion_servicio,
            tipo_servicio=row.tipo_servicio,
            costo_servicio=row.costo_servicio,
            cantidad_servicio=row.cantidad_servicio,
            fecha_creacion_servicio=row.fecha_creacion_servicio,
            activo=bool(row.activo),
            usuario_creador_servicio=row.usuario_creador_servicio,
            fecha_actualizacion_servicio=row.fecha_actualizacion_servicio
        )




# #deepseek
# import pyodbc
# from datetime import datetime
# from typing import List, Optional
# from Models.cotizacion_servicio import CotizacionServicio

# class CotizacionServicioRepository:
#     def __init__(self, connection_string: str):
#         self.connection_string = connection_string

#     def _get_connection(self):
#         return pyodbc.connect(self.connection_string)

#     def add_servicio_to_cotizacion(self, cotizacion_servicio: CotizacionServicio) -> CotizacionServicio:
#         query = """
#         INSERT INTO CotizacionServicios (
#             id_cotizacion, id_servicio, nombre_servicio, descripcion_servicio,
#             tipo_servicio, costo_servicio, cantidad_servicio, fecha_creacion_servicio,
#             activo, usuario_creador_servicio, fecha_actualizacion_servicio
#         ) 
#         OUTPUT INSERTED.id_cotizacion_servicio
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """
        
#         params = (
#             cotizacion_servicio.id_cotizacion,
#             cotizacion_servicio.id_servicio,
#             cotizacion_servicio.nombre_servicio,
#             cotizacion_servicio.descripcion_servicio,
#             cotizacion_servicio.tipo_servicio,
#             cotizacion_servicio.costo_servicio,
#             cotizacion_servicio.cantidad_servicio or 1.0,
#             cotizacion_servicio.fecha_creacion_servicio or datetime.now(),
#             cotizacion_servicio.activo,
#             cotizacion_servicio.usuario_creador_servicio,
#             cotizacion_servicio.fecha_actualizacion_servicio
#         )

#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, params)
#             inserted_id = cursor.fetchone()[0]
#             conn.commit()
            
#             return self.get_servicio_by_id(inserted_id)

#     def get_servicio_by_id(self, id_cotizacion_servicio: int) -> Optional[CotizacionServicio]:
#         query = "SELECT * FROM CotizacionServicios WHERE id_cotizacion_servicio = ?"
        
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, id_cotizacion_servicio)
#             row = cursor.fetchone()
            
#             if row:
#                 return self._row_to_cotizacion_servicio(row)
#             return None

#     def get_servicios_by_cotizacion(self, id_cotizacion: int, activos_only: bool = True) -> List[CotizacionServicio]:
#         query = "SELECT * FROM CotizacionServicios WHERE id_cotizacion = ?"
#         if activos_only:
#             query += " AND activo = 1"
            
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, id_cotizacion)
#             return [self._row_to_cotizacion_servicio(row) for row in cursor.fetchall()]

#     def update_servicio(self, id_cotizacion_servicio: int, cotizacion_servicio: CotizacionServicio) -> Optional[CotizacionServicio]:
#         query = """
#         UPDATE CotizacionServicios 
#         SET 
#             nombre_servicio = ?,
#             descripcion_servicio = ?,
#             tipo_servicio = ?,
#             costo_servicio = ?,
#             cantidad_servicio = ?,
#             activo = ?,
#             fecha_actualizacion_servicio = ?
#         WHERE id_cotizacion_servicio = ?
#         """
        
#         params = (
#             cotizacion_servicio.nombre_servicio,
#             cotizacion_servicio.descripcion_servicio,
#             cotizacion_servicio.tipo_servicio,
#             cotizacion_servicio.costo_servicio,
#             cotizacion_servicio.cantidad_servicio,
#             cotizacion_servicio.activo,
#             datetime.now(),
#             id_cotizacion_servicio
#         )

#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, params)
#             conn.commit()
            
#             if cursor.rowcount > 0:
#                 return self.get_servicio_by_id(id_cotizacion_servicio)
#             return None

#     def remove_servicio(self, id_cotizacion_servicio: int) -> bool:
#         query = "UPDATE CotizacionServicios SET activo = 0 WHERE id_cotizacion_servicio = ?"
        
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, id_cotizacion_servicio)
#             conn.commit()
#             return cursor.rowcount > 0

#     def _row_to_cotizacion_servicio(self, row) -> CotizacionServicio:
#         return CotizacionServicio(
#             id_cotizacion_servicio=row.id_cotizacion_servicio,
#             id_cotizacion=row.id_cotizacion,
#             id_servicio=row.id_servicio,
#             nombre_servicio=row.nombre_servicio,
#             descripcion_servicio=row.descripcion_servicio,
#             tipo_servicio=row.tipo_servicio,
#             costo_servicio=float(row.costo_servicio),
#             cantidad_servicio=float(row.cantidad_servicio) if row.cantidad_servicio else None,
#             fecha_creacion_servicio=row.fecha_creacion_servicio,
#             activo=bool(row.activo),
#             usuario_creador_servicio=row.usuario_creador_servicio,
#             fecha_actualizacion_servicio=row.fecha_actualizacion_servicio
#         )