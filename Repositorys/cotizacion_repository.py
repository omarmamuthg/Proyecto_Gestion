# #cotizacion_repository
# import pyodbc
# from datetime import datetime
# from typing import List, Optional
# from Models.cotizacion import Cotizacion  # Asegúrate de que la clase Cotizacion esté en este path

# class CotizacionRepository:
#     def __init__(self, connection_string: str):
#         self.connection_string = connection_string

#     def _get_connection(self):
#         return pyodbc.connect(self.connection_string)

#     def create_cotizacion(self, cotizacion: Cotizacion) -> Cotizacion:
#         """
#         Crea una nueva cotización en la base de datos.

#         Args:
#             cotizacion (Cotizacion): Objeto Cotizacion con los datos a insertar.

#         Returns:
#             Cotizacion: La cotización recién creada, incluyendo el ID asignado por la base de datos.
#         """
#         query = """
#             INSERT INTO Cotizaciones (
#                 id_cliente, fecha_creacion, fecha_activacion, fecha_finalizacion,
#                 fecha_cancelacion, observaciones, usuario_creador, nombre_cliente,
#                 correo_cliente, telefono_cliente, tipo_cliente, rfc_cliente, activo
#             )
#             OUTPUT INSERTED.id_cotizacion
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """

#         params = (
#             cotizacion.id_cliente,
#             cotizacion.fecha_creacion or datetime.now(),
#             cotizacion.fecha_activacion,
#             cotizacion.fecha_finalizacion,
#             cotizacion.fecha_cancelacion,
#             cotizacion.observaciones,
#             cotizacion.usuario_creador,
#             cotizacion.nombre_cliente,
#             cotizacion.correo_cliente,
#             cotizacion.telefono_cliente,
#             cotizacion.tipo_cliente,
#             cotizacion.rfc_cliente,
#             cotizacion.activo
#         )

#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, params)
#             inserted_id = cursor.fetchone()[0]
#             conn.commit()

#             return self.get_cotizacion(inserted_id)

#     def get_cotizacion(self, id_cotizacion: int) -> Optional[Cotizacion]:
#         """
#         Obtiene una cotización por su ID.

#         Args:
#             id_cotizacion (int): El ID de la cotización a buscar.

#         Returns:
#             Optional[Cotizacion]: La cotización encontrada, o None si no existe.
#         """
#         query = "SELECT * FROM Cotizaciones WHERE id_cotizacion = ?"

#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, id_cotizacion)
#             row = cursor.fetchone()

#             if row:
#                 return self._row_to_cotizacion(row)
#             return None

#     def get_all_cotizaciones(self, activos_only: bool = True) -> List[Cotizacion]:
#         """
#         Obtiene todas las cotizaciones, opcionalmente filtrando por las activas.

#         Args:
#             activos_only (bool, optional): Indica si se deben obtener solo las cotizaciones activas.
#                 Por defecto, True.

#         Returns:
#             List[Cotizacion]: Una lista de objetos Cotizacion.
#         """
#         query = "SELECT * FROM Cotizaciones"
#         if activos_only:
#             query += " WHERE activo = 1"

#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query)
#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]

#     def update_cotizacion(self, id_cotizacion: int, cotizacion: Cotizacion) -> Optional[Cotizacion]:
#         """
#         Actualiza los datos de una cotización existente.

#         Args:
#             id_cotizacion (int): El ID de la cotización a actualizar.
#             cotizacion (Cotizacion): Objeto Cotizacion con los nuevos datos.

#         Returns:
#             Optional[Cotizacion]: La cotización actualizada, o None si no se encontró.
#         """
#         query = """
#             UPDATE Cotizaciones
#             SET
#                 id_cliente = ?,
#                 fecha_creacion = ?,
#                 fecha_activacion = ?,
#                 fecha_finalizacion = ?,
#                 fecha_cancelacion = ?,
#                 observaciones = ?,
#                 usuario_creador = ?,
#                 nombre_cliente = ?,
#                 correo_cliente = ?,
#                 telefono_cliente = ?,
#                 tipo_cliente = ?,
#                 rfc_cliente = ?,
#                 activo = ?
#             WHERE id_cotizacion = ?
#         """

#         params = (
#             cotizacion.id_cliente,
#             cotizacion.fecha_creacion,
#             cotizacion.fecha_activacion,
#             cotizacion.fecha_finalizacion,
#             cotizacion.fecha_cancelacion,
#             cotizacion.observaciones,
#             cotizacion.usuario_creador,
#             cotizacion.nombre_cliente,
#             cotizacion.correo_cliente,
#             cotizacion.telefono_cliente,
#             cotizacion.tipo_cliente,
#             cotizacion.rfc_cliente,
#             cotizacion.activo,
#             id_cotizacion
#         )

#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, params)
#             conn.commit()

#             if cursor.rowcount > 0:
#                 return self.get_cotizacion(id_cotizacion)
#             return None

#     def delete_cotizacion(self, id_cotizacion: int) -> bool:
#         """
#         Elimina lógicamente una cotización (establece el campo 'activo' a 0).

#         Args:
#             id_cotizacion (int): El ID de la cotización a eliminar.

#         Returns:
#             bool: True si la eliminación fue exitosa, False en caso contrario.
#         """
#         query = "UPDATE Cotizaciones SET activo = 0 WHERE id_cotizacion = ?"

#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, id_cotizacion)
#             conn.commit()
#             return cursor.rowcount > 0

#     def _row_to_cotizacion(self, row) -> Cotizacion:
#         """
#         Convierte una fila de la base de datos a un objeto Cotizacion.

#         Args:
#             row: La fila de la base de datos (resultado de cursor.fetchone()).

#         Returns:
#             Cotizacion: Un objeto Cotizacion con los datos de la fila.
#         """
#         return Cotizacion(
#             id_cotizacion=row.id_cotizacion,
#             id_cliente=row.id_cliente,
#             fecha_creacion=row.fecha_creacion,
#             fecha_activacion=row.fecha_activacion,
#             fecha_finalizacion=row.fecha_finalizacion,
#             fecha_cancelacion=row.fecha_cancelacion,
#             observaciones=row.observaciones,
#             usuario_creador=row.usuario_creador,
#             nombre_cliente=row.nombre_cliente,
#             correo_cliente=row.correo_cliente,
#             telefono_cliente=row.telefono_cliente,
#             tipo_cliente=row.tipo_cliente,
#             rfc_cliente=row.rfc_cliente,
#             activo=bool(row.activo)
#         )

#     def get_cotizaciones_by_servicio_nombre(self, nombre_servicio: str) -> List[Cotizacion]:
#         """
#         Obtiene las cotizaciones que contienen un servicio con el nombre especificado.

#         Args:
#             nombre_servicio (str): El nombre del servicio a buscar.

#         Returns:
#             List[Cotizacion]: Una lista de objetos Cotizacion que contienen el servicio.
#         """
#         query = """
#         SELECT DISTINCT c.*
#         FROM Cotizaciones c
#         INNER JOIN Cotizacion_Servicio cs ON c.id_cotizacion = cs.id_cotizacion
#         WHERE cs.nombre_servicio LIKE ?
#         """
#         # Usamos el comodín '%' para buscar coincidencias parciales
#         params = (f"%{nombre_servicio}%",)

#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, params)
#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]

#     # Añade estos métodos a tu CotizacionRepository

#     def get_cotizaciones_by_cliente(self, id_cliente: int, activos_only: bool = True) -> List[Cotizacion]:
#         """
#         Obtiene todas las cotizaciones de un cliente específico.
        
#         Args:
#             id_cliente (int): ID del cliente
#             activos_only (bool): Si True, solo devuelve cotizaciones activas
        
#         Returns:
#             List[Cotizacion]: Lista de cotizaciones del cliente
#         """
#         query = "SELECT * FROM Cotizaciones WHERE id_cliente = ?"
#         if activos_only:
#             query += " AND activo = 1"
        
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, id_cliente)
#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]

#     def get_cotizaciones_by_fecha_rango(
#         self, 
#         fecha_inicio: datetime, 
#         fecha_fin: datetime,
#         activos_only: bool = True
#     ) -> List[Cotizacion]:
#         """
#         Obtiene cotizaciones creadas en un rango de fechas.
        
#         Args:
#             fecha_inicio (datetime): Fecha de inicio
#             fecha_fin (datetime): Fecha de fin
#             activos_only (bool): Si True, solo devuelve cotizaciones activas
        
#         Returns:
#             List[Cotizacion]: Lista de cotizaciones en el rango
#         """
#         query = """
#         SELECT * FROM Cotizaciones 
#         WHERE fecha_creacion BETWEEN ? AND ?
#         """
#         if activos_only:
#             query += " AND activo = 1"
        
#         params = (fecha_inicio, fecha_fin)
        
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, params)
#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]

#     def get_cotizaciones_by_estado(self, estado: str) -> List[Cotizacion]:
#         """
#         Obtiene cotizaciones por estado (vigente, cancelada, finalizada).
        
#         Args:
#             estado (str): 'vigente', 'cancelada' o 'finalizada'
        
#         Returns:
#             List[Cotizacion]: Lista de cotizaciones en el estado especificado
#         """
#         query = "SELECT * FROM Cotizaciones WHERE "
        
#         if estado == 'vigente':
#             query += "activo = 1 AND fecha_finalizacion IS NULL"
#         elif estado == 'cancelada':
#             query += "activo = 0 AND fecha_cancelacion IS NOT NULL"
#         elif estado == 'finalizada':
#             query += "fecha_finalizacion IS NOT NULL"
#         else:
#             raise ValueError("Estado no válido. Use 'vigente', 'cancelada' o 'finalizada'")
        
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query)
#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]

#     def get_count_cotizaciones(self) -> dict:
#         """
#         Obtiene conteos estadísticos de cotizaciones.
        
#         Returns:
#             dict: Diccionario con conteos por estado
#         """
#         query = """
#         SELECT 
#             COUNT(*) as total,
#             SUM(CASE WHEN activo = 1 THEN 1 ELSE 0 END) as activas,
#             SUM(CASE WHEN activo = 0 THEN 1 ELSE 0 END) as canceladas,
#             SUM(CASE WHEN fecha_finalizacion IS NOT NULL THEN 1 ELSE 0 END) as finalizadas
#         FROM Cotizaciones
#         """
        
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query)
#             row = cursor.fetchone()
#             return {
#                 'total': row.total,
#                 'activas': row.activas,
#                 'canceladas': row.canceladas,
#                 'finalizadas': row.finalizadas
#             }

#     def get_ultimas_cotizaciones(self, limit: int = 5) -> List[Cotizacion]:
#         """
#         Obtiene las últimas cotizaciones creadas.
        
#         Args:
#             limit (int): Número máximo de cotizaciones a devolver
        
#         Returns:
#             List[Cotizacion]: Lista de las últimas cotizaciones
#         """
#         query = """
#         SELECT TOP (?) * 
#         FROM Cotizaciones 
#         ORDER BY fecha_creacion DESC
#         """
        
#         with self._get_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(query, limit)
#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]




# cotizacion_repository.py
import pyodbc
from datetime import datetime
from typing import List, Optional, Dict, Any
from Models.cotizacion import Cotizacion

class CotizacionRepository:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    # def _get_connection(self):
    #     return pyodbc.connect(self.connection_string)
    def _get_connection(self):
        # print(f"Intentando conectar con connection_string: {self.connection_string}")
        return pyodbc.connect(self.connection_string)


    def _row_to_cotizacion(self, row) -> Cotizacion:
        """
        Convierte una fila de la base de datos a un objeto Cotizacion.
        """
        return Cotizacion(
            id_cotizacion=row.id_cotizacion,
            id_cliente=row.id_cliente,
            fecha_creacion=row.fecha_creacion,
            fecha_activacion=row.fecha_activacion,
            fecha_finalizacion=row.fecha_finalizacion,
            fecha_cancelacion=row.fecha_cancelacion,
            observaciones=row.observaciones,
            usuario_creador=row.usuario_creador,
            nombre_cliente=row.nombre_cliente,
            correo_cliente=row.correo_cliente,
            telefono_cliente=row.telefono_cliente,
            tipo_cliente=row.tipo_cliente,
            rfc_cliente=row.rfc_cliente,
            activo=bool(row.activo)
        )

    # Métodos CRUD básicos
    def create_cotizacion(self, cotizacion: Cotizacion) -> Optional[Cotizacion]:
        """
        Crea una nueva cotización en la base de datos.
        """
        query = """
            INSERT INTO Cotizaciones (
                id_cliente, fecha_creacion, fecha_activacion, fecha_finalizacion,
                fecha_cancelacion, observaciones, usuario_creador, nombre_cliente,
                correo_cliente, telefono_cliente, tipo_cliente, rfc_cliente, activo
            )
            OUTPUT INSERTED.id_cotizacion
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            cotizacion.id_cliente,  # <--- Recibes el id_cliente aquí
            cotizacion.fecha_creacion or datetime.now(),
            cotizacion.fecha_activacion,
            cotizacion.fecha_finalizacion,
            cotizacion.fecha_cancelacion,
            cotizacion.observaciones,
            cotizacion.usuario_creador,
            cotizacion.nombre_cliente,
            cotizacion.correo_cliente,
            cotizacion.telefono_cliente,
            cotizacion.tipo_cliente,
            cotizacion.rfc_cliente,
            cotizacion.activo
        )

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            inserted_id = cursor.fetchone()[0]
            conn.commit()
            return self.get_cotizacion(inserted_id)


    def get_cotizacion(self, id_cotizacion: int) -> Optional[Cotizacion]:
        """
        Obtiene una cotización por su ID.
        """
        query = "SELECT * FROM Cotizaciones WHERE id_cotizacion = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # cursor.execute(query, id_cotizacion)
            cursor.execute(query, (id_cotizacion,))
            row = cursor.fetchone()
            return self._row_to_cotizacion(row) if row else None

    def get_all_cotizaciones(self, activos_only: bool = True) -> List[Cotizacion]:
        """
        Obtiene todas las cotizaciones, opcionalmente filtrando por las activas.
        """
        query = "SELECT * FROM Cotizaciones" + (" WHERE activo = 1" if activos_only else "")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [self._row_to_cotizacion(row) for row in cursor.fetchall()]

    def update_cotizacion(self, id_cotizacion: int, cotizacion: Cotizacion) -> Optional[Cotizacion]:
        """
        Actualiza los datos de una cotización existente.
        """
        query = """
            UPDATE Cotizaciones
            SET id_cliente = ?, fecha_creacion = ?, fecha_activacion = ?,
                fecha_finalizacion = ?, fecha_cancelacion = ?, observaciones = ?,
                usuario_creador = ?, nombre_cliente = ?, correo_cliente = ?,
                telefono_cliente = ?, tipo_cliente = ?, rfc_cliente = ?, activo = ?
            WHERE id_cotizacion = ?
        """
        params = (
            cotizacion.id_cliente, cotizacion.fecha_creacion, cotizacion.fecha_activacion,
            cotizacion.fecha_finalizacion, cotizacion.fecha_cancelacion, cotizacion.observaciones,
            cotizacion.usuario_creador, cotizacion.nombre_cliente, cotizacion.correo_cliente,
            cotizacion.telefono_cliente, cotizacion.tipo_cliente, cotizacion.rfc_cliente,
            cotizacion.activo, id_cotizacion
        )

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return self.get_cotizacion(id_cotizacion) if cursor.rowcount > 0 else None

    def delete_cotizacion(self, id_cotizacion: int) -> bool:
        """
        Elimina lógicamente una cotización (establece el campo 'activo' a 0).
        """
        query = "UPDATE Cotizaciones SET activo = 0 WHERE id_cotizacion = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, id_cotizacion)
            conn.commit()
            return cursor.rowcount > 0

    # Métodos de búsqueda y consultas especializadas
    def get_cotizaciones_by_servicio_nombre(self, nombre_servicio: str) -> List[Cotizacion]:
        """
        Obtiene las cotizaciones que contienen un servicio con el nombre especificado.
        """
        query = """
        SELECT DISTINCT c.* FROM Cotizaciones c
        INNER JOIN Cotizacion_Servicio cs ON c.id_cotizacion = cs.id_cotizacion
        WHERE cs.nombre_servicio LIKE ?
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, f"%{nombre_servicio}%")
            return [self._row_to_cotizacion(row) for row in cursor.fetchall()]

    def get_cotizaciones_by_cliente(self, id_cliente: int, activos_only: bool = True) -> List[Cotizacion]:
        """
        Obtiene todas las cotizaciones de un cliente específico.
        """
        query = f"SELECT * FROM Cotizaciones WHERE id_cliente = ?{' AND activo = 1' if activos_only else ''}"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, id_cliente)
            return [self._row_to_cotizacion(row) for row in cursor.fetchall()]

    def get_cotizaciones_by_fecha_rango(
        self, 
        fecha_inicio: datetime, 
        fecha_fin: datetime,
        activos_only: bool = True
    ) -> List[Cotizacion]:
        """
        Obtiene cotizaciones creadas en un rango de fechas.
        """
        query = f"""
        SELECT * FROM Cotizaciones 
        WHERE fecha_creacion BETWEEN ? AND ?{' AND activo = 1' if activos_only else ''}
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, fecha_inicio, fecha_fin)
            return [self._row_to_cotizacion(row) for row in cursor.fetchall()]

    def get_cotizaciones_by_estado(self, estado: str) -> List[Cotizacion]:
        """
        Obtiene cotizaciones por estado (vigente, cancelada, finalizada).
        """
        if estado == 'vigente':
            query = "SELECT * FROM Cotizaciones WHERE activo = 1 AND fecha_finalizacion IS NULL"
        elif estado == 'cancelada':
            query = "SELECT * FROM Cotizaciones WHERE activo = 0 AND fecha_cancelacion IS NOT NULL"
        elif estado == 'finalizada':
            query = "SELECT * FROM Cotizaciones WHERE fecha_finalizacion IS NOT NULL"
        else:
            raise ValueError("Estado no válido. Use 'vigente', 'cancelada' o 'finalizada'")
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [self._row_to_cotizacion(row) for row in cursor.fetchall()]

    def get_ultimas_cotizaciones(self, limit: int = 5) -> List[Cotizacion]:
        """
        Obtiene las últimas cotizaciones creadas.
        """
        query = "SELECT TOP (?) * FROM Cotizaciones ORDER BY fecha_creacion DESC"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, limit)
            return [self._row_to_cotizacion(row) for row in cursor.fetchall()]

    # Métodos estadísticos y avanzados
    def get_count_cotizaciones(self) -> Dict[str, int]:
        """
        Obtiene conteos estadísticos de cotizaciones.
        """
        query = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN activo = 1 THEN 1 ELSE 0 END) as activas,
            SUM(CASE WHEN activo = 0 THEN 1 ELSE 0 END) as canceladas,
            SUM(CASE WHEN fecha_finalizacion IS NOT NULL THEN 1 ELSE 0 END) as finalizadas
        FROM Cotizaciones
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            return {
                'total': row.total,
                'activas': row.activas,
                'canceladas': row.canceladas,
                'finalizadas': row.finalizadas
            }

    def buscar_cotizaciones(
        self,
        id_cliente: Optional[int] = None,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        estado: Optional[str] = None,
        servicio: Optional[str] = None,
        activos_only: bool = True
    ) -> List[Cotizacion]:
        """
        Búsqueda avanzada de cotizaciones con múltiples filtros.
        """
        query = "SELECT DISTINCT c.* FROM Cotizaciones c"
        conditions = []
        params = []
        
        if servicio:
            query += " INNER JOIN Cotizacion_Servicio cs ON c.id_cotizacion = cs.id_cotizacion"
            conditions.append("cs.nombre_servicio LIKE ?")
            params.append(f"%{servicio}%")
        
        if activos_only:
            conditions.append("c.activo = 1")
        
        if id_cliente:
            conditions.append("c.id_cliente = ?")
            params.append(id_cliente)
        
        if fecha_inicio and fecha_fin:
            conditions.append("c.fecha_creacion BETWEEN ? AND ?")
            params.extend([fecha_inicio, fecha_fin])
        
        if estado:
            if estado == 'vigente':
                conditions.append("c.activo = 1 AND c.fecha_finalizacion IS NULL")
            elif estado == 'cancelada':
                conditions.append("c.activo = 0 AND c.fecha_cancelacion IS NOT NULL")
            elif estado == 'finalizada':
                conditions.append("c.fecha_finalizacion IS NOT NULL")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [self._row_to_cotizacion(row) for row in cursor.fetchall()]

    def get_cotizaciones_paginadas(
        self, 
        page: int = 1, 
        per_page: int = 10,
        activos_only: bool = True
    ) -> Dict[str, Any]:
        """
        Obtiene cotizaciones con paginación.
        """
        offset = (page - 1) * per_page
        base_query = "SELECT * FROM Cotizaciones"
        count_query = "SELECT COUNT(*) FROM Cotizaciones"
        
        where_clause = " WHERE activo = 1" if activos_only else ""
        order_clause = " ORDER BY fecha_creacion DESC"
        pagination_clause = f" OFFSET {offset} ROWS FETCH NEXT {per_page} ROWS ONLY"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Obtener total de registros
            cursor.execute(count_query + where_clause)
            total = cursor.fetchone()[0]
            
            # Obtener datos paginados
            cursor.execute(base_query + where_clause + order_clause + pagination_clause)
            data = [self._row_to_cotizacion(row) for row in cursor.fetchall()]
            
            return {
                'data': data,
                'total': total,
                'pages': (total + per_page - 1) // per_page,
                'page': page
            }

    def create_cotizacion_with_servicios(
        self, 
        cotizacion: Cotizacion, 
        servicios: List[Dict[str, Any]]
    ) -> Cotizacion:
        """
        Crea una cotización junto con sus servicios en una transacción.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("BEGIN TRANSACTION")
            
            # Crear cotización
            cotizacion_creada = self.create_cotizacion(cotizacion)
            
            # Insertar servicios
            for servicio in servicios:
                cursor.execute(
                    """INSERT INTO Cotizacion_Servicio 
                    (id_cotizacion, nombre_servicio, cantidad, precio) 
                    VALUES (?, ?, ?, ?)""",
                    (cotizacion_creada.id_cotizacion, 
                     servicio['nombre_servicio'],
                     servicio['cantidad'], 
                     servicio['precio'])
                )
            
            conn.commit()
            return cotizacion_creada
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    # En CotizacionRepository, agregar este método (puede ser un alias):
    def obtener_cotizacion(self, id_cotizacion: int) -> Optional[Cotizacion]:
        """Alias en español para get_cotizacion"""
        return self.get_cotizacion(id_cotizacion)