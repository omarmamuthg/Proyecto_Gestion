#import pyodbc

# server = 'OMARLAPTOP'      # Nombre de tu servidor
# database = 'DB_SIGA'       # Base de datos correcta (¡no master!)
# username = 'DB_SIGA'       # Login del servidor
# password = 'db_siga'       # Contraseña del login

# try:
#     conn = pyodbc.connect(
#         f'DRIVER={{ODBC Driver 17 for SQL Server}};'  # Driver actualizado
#         f'SERVER={server};'
#         f'DATABASE={database};'
#         f'UID={username};'
#         f'PWD={password}'
#     )
#     print("✅ ¡Conexión exitosa a DB_SIGA!")
    
#     # Ejemplo: Consultar tablas para verificar acceso
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM sys.tables")
#     for table in cursor.fetchall():
#         print(f"Tabla encontrada: {table[0]}")

# except Exception as e:
#     print(f"❌ Error: {e}")
# finally:
#     if 'conn' in locals():
#         conn.close()

# Database/Conexion.py
import pyodbc
from typing import Optional

class Conexion:
    _instancia = None
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia
    
    def _inicializar(self):
        self.server = 'OMARLAPTOP'
        self.database = 'DB_SIGA'
        self.username = 'DB_SIGA'
        self.password = 'db_siga'
        self.conn = None
    
    def conectar(self) -> Optional[pyodbc.Connection]:
        try:
            self.conn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'UID={self.username};'
                f'PWD={self.password}'
            )
            return self.conn
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return None
    
    def cerrar(self):
        if self.conn:
            self.conn.close()
            self.conn = None

# Función de conveniencia para usar como singleton
def obtener_conexion():
    return Conexion().conectar()
































# me puedes ayudar por favor-> tengo estas clases #cotizacion clase

# from pydantic import BaseModel

# from datetime import datetime

# from typing import Optional



# class Cotizacion(BaseModel):

#     id_cotizacion: Optional[int] = None

#     id_cliente: int

#     fecha_creacion: Optional[datetime] = None

#     fecha_activacion: Optional[datetime] = None

#     fecha_finalizacion: Optional[datetime] = None

#     fecha_cancelacion: Optional[datetime] = None

#     observaciones: Optional[str] = None

#     usuario_creador: Optional[str] = None

#     nombre_cliente: Optional[str] = None

#     correo_cliente: Optional[str] = None

#     telefono_cliente: Optional[str] = None

#     tipo_cliente: Optional[str] = None

#     rfc_cliente: str

#     activo: bool = True

# #Cotizacion_servicio

# from pydantic import BaseModel

# from datetime import datetime

# from typing import Optional



# class CotizacionServicio(BaseModel):

#     id_cotizacion_servicio: Optional[int] = None

#     id_cotizacion: int

#     id_servicio: int

#     nombre_servicio: str

#     descripcion_servicio: Optional[str] = None

#     tipo_servicio: Optional[str] = None

#     costo_servicio: float

#     cantidad_servicio: Optional[float] = None

#     fecha_creacion_servicio: Optional[datetime] = None

#     activo: bool = True

#     usuario_creador_servicio: str

#     fecha_actualizacion_servicio: Optional[datetime] = None

# los siguientes repositorios y el siguiente controlador -> 

# # cotizacion_repository.py

# import pyodbc

# from datetime import datetime

# from typing import List, Optional, Dict, Any

# from Models.cotizacion import Cotizacion



# class CotizacionRepository:

#     def __init__(self, connection_string: str):

#         self.connection_string = connection_string



#     def _get_connection(self):

#         return pyodbc.connect(self.connection_string)



#     def _row_to_cotizacion(self, row) -> Cotizacion:

#         """

#         Convierte una fila de la base de datos a un objeto Cotizacion.

#         """

#         return Cotizacion(

#             id_cotizacion=row.id_cotizacion,

#             id_cliente=row.id_cliente,

#             fecha_creacion=row.fecha_creacion,

#             fecha_activacion=row.fecha_activacion,

#             fecha_finalizacion=row.fecha_finalizacion,

#             fecha_cancelacion=row.fecha_cancelacion,

#             observaciones=row.observaciones,

#             usuario_creador=row.usuario_creador,

#             nombre_cliente=row.nombre_cliente,

#             correo_cliente=row.correo_cliente,

#             telefono_cliente=row.telefono_cliente,

#             tipo_cliente=row.tipo_cliente,

#             rfc_cliente=row.rfc_cliente,

#             activo=bool(row.activo)

#         )



#     # Métodos CRUD básicos

#     def create_cotizacion(self, cotizacion: Cotizacion) -> Cotizacion:

#         """

#         Crea una nueva cotización en la base de datos.

#         """

#         query = """

#             INSERT INTO Cotizaciones (

#                 id_cliente, fecha_creacion, fecha_activacion, fecha_finalizacion,

#                 fecha_cancelacion, observaciones, usuario_creador, nombre_cliente,

#                 correo_cliente, telefono_cliente, tipo_cliente, rfc_cliente, activo

#             )

#             OUTPUT INSERTED.id_cotizacion

#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

#         """

#         params = (

#             cotizacion.id_cliente,

#             cotizacion.fecha_creacion or datetime.now(),

#             cotizacion.fecha_activacion,

#             cotizacion.fecha_finalizacion,

#             cotizacion.fecha_cancelacion,

#             cotizacion.observaciones,

#             cotizacion.usuario_creador,

#             cotizacion.nombre_cliente,

#             cotizacion.correo_cliente,

#             cotizacion.telefono_cliente,

#             cotizacion.tipo_cliente,

#             cotizacion.rfc_cliente,

#             cotizacion.activo

#         )



#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, params)

#             inserted_id = cursor.fetchone()[0]

#             conn.commit()

#             return self.get_cotizacion(inserted_id)



#     def get_cotizacion(self, id_cotizacion: int) -> Optional[Cotizacion]:

#         """

#         Obtiene una cotización por su ID.

#         """

#         query = "SELECT * FROM Cotizaciones WHERE id_cotizacion = ?"

#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, id_cotizacion)

#             row = cursor.fetchone()

#             return self._row_to_cotizacion(row) if row else None



#     def get_all_cotizaciones(self, activos_only: bool = True) -> List[Cotizacion]:

#         """

#         Obtiene todas las cotizaciones, opcionalmente filtrando por las activas.

#         """

#         query = "SELECT * FROM Cotizaciones" + (" WHERE activo = 1" if activos_only else "")

#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query)

#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]



#     def update_cotizacion(self, id_cotizacion: int, cotizacion: Cotizacion) -> Optional[Cotizacion]:

#         """

#         Actualiza los datos de una cotización existente.

#         """

#         query = """

#             UPDATE Cotizaciones

#             SET id_cliente = ?, fecha_creacion = ?, fecha_activacion = ?,

#                 fecha_finalizacion = ?, fecha_cancelacion = ?, observaciones = ?,

#                 usuario_creador = ?, nombre_cliente = ?, correo_cliente = ?,

#                 telefono_cliente = ?, tipo_cliente = ?, rfc_cliente = ?, activo = ?

#             WHERE id_cotizacion = ?

#         """

#         params = (

#             cotizacion.id_cliente, cotizacion.fecha_creacion, cotizacion.fecha_activacion,

#             cotizacion.fecha_finalizacion, cotizacion.fecha_cancelacion, cotizacion.observaciones,

#             cotizacion.usuario_creador, cotizacion.nombre_cliente, cotizacion.correo_cliente,

#             cotizacion.telefono_cliente, cotizacion.tipo_cliente, cotizacion.rfc_cliente,

#             cotizacion.activo, id_cotizacion

#         )



#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, params)

#             conn.commit()

#             return self.get_cotizacion(id_cotizacion) if cursor.rowcount > 0 else None



#     def delete_cotizacion(self, id_cotizacion: int) -> bool:

#         """

#         Elimina lógicamente una cotización (establece el campo 'activo' a 0).

#         """

#         query = "UPDATE Cotizaciones SET activo = 0 WHERE id_cotizacion = ?"

#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, id_cotizacion)

#             conn.commit()

#             return cursor.rowcount > 0



#     # Métodos de búsqueda y consultas especializadas

#     def get_cotizaciones_by_servicio_nombre(self, nombre_servicio: str) -> List[Cotizacion]:

#         """

#         Obtiene las cotizaciones que contienen un servicio con el nombre especificado.

#         """

#         query = """

#         SELECT DISTINCT c.* FROM Cotizaciones c

#         INNER JOIN Cotizacion_Servicio cs ON c.id_cotizacion = cs.id_cotizacion

#         WHERE cs.nombre_servicio LIKE ?

#         """

#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, f"%{nombre_servicio}%")

#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]



#     def get_cotizaciones_by_cliente(self, id_cliente: int, activos_only: bool = True) -> List[Cotizacion]:

#         """

#         Obtiene todas las cotizaciones de un cliente específico.

#         """

#         query = f"SELECT * FROM Cotizaciones WHERE id_cliente = ?{' AND activo = 1' if activos_only else ''}"

#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, id_cliente)

#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]



#     def get_cotizaciones_by_fecha_rango(

#         self, 

#         fecha_inicio: datetime, 

#         fecha_fin: datetime,

#         activos_only: bool = True

#     ) -> List[Cotizacion]:

#         """

#         Obtiene cotizaciones creadas en un rango de fechas.

#         """

#         query = f"""

#         SELECT * FROM Cotizaciones 

#         WHERE fecha_creacion BETWEEN ? AND ?{' AND activo = 1' if activos_only else ''}

#         """

#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, fecha_inicio, fecha_fin)

#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]



#     def get_cotizaciones_by_estado(self, estado: str) -> List[Cotizacion]:

#         """

#         Obtiene cotizaciones por estado (vigente, cancelada, finalizada).

#         """

#         if estado == 'vigente':

#             query = "SELECT * FROM Cotizaciones WHERE activo = 1 AND fecha_finalizacion IS NULL"

#         elif estado == 'cancelada':

#             query = "SELECT * FROM Cotizaciones WHERE activo = 0 AND fecha_cancelacion IS NOT NULL"

#         elif estado == 'finalizada':

#             query = "SELECT * FROM Cotizaciones WHERE fecha_finalizacion IS NOT NULL"

#         else:

#             raise ValueError("Estado no válido. Use 'vigente', 'cancelada' o 'finalizada'")

#         

#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query)

#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]



#     def get_ultimas_cotizaciones(self, limit: int = 5) -> List[Cotizacion]:

#         """

#         Obtiene las últimas cotizaciones creadas.

#         """

#         query = "SELECT TOP (?) * FROM Cotizaciones ORDER BY fecha_creacion DESC"

#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, limit)

#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]



#     # Métodos estadísticos y avanzados

#     def get_count_cotizaciones(self) -> Dict[str, int]:

#         """

#         Obtiene conteos estadísticos de cotizaciones.

#         """

#         query = """

#         SELECT 

#             COUNT(*) as total,

#             SUM(CASE WHEN activo = 1 THEN 1 ELSE 0 END) as activas,

#             SUM(CASE WHEN activo = 0 THEN 1 ELSE 0 END) as canceladas,

#             SUM(CASE WHEN fecha_finalizacion IS NOT NULL THEN 1 ELSE 0 END) as finalizadas

#         FROM Cotizaciones

#         """

#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query)

#             row = cursor.fetchone()

#             return {

#                 'total': row.total,

#                 'activas': row.activas,

#                 'canceladas': row.canceladas,

#                 'finalizadas': row.finalizadas

#             }



#     def buscar_cotizaciones(

#         self,

#         id_cliente: Optional[int] = None,

#         fecha_inicio: Optional[datetime] = None,

#         fecha_fin: Optional[datetime] = None,

#         estado: Optional[str] = None,

#         servicio: Optional[str] = None,

#         activos_only: bool = True

#     ) -> List[Cotizacion]:

#         """

#         Búsqueda avanzada de cotizaciones con múltiples filtros.

#         """

#         query = "SELECT DISTINCT c.* FROM Cotizaciones c"

#         conditions = []

#         params = []

#         

#         if servicio:

#             query += " INNER JOIN Cotizacion_Servicio cs ON c.id_cotizacion = cs.id_cotizacion"

#             conditions.append("cs.nombre_servicio LIKE ?")

#             params.append(f"%{servicio}%")

#         

#         if activos_only:

#             conditions.append("c.activo = 1")

#         

#         if id_cliente:

#             conditions.append("c.id_cliente = ?")

#             params.append(id_cliente)

#         

#         if fecha_inicio and fecha_fin:

#             conditions.append("c.fecha_creacion BETWEEN ? AND ?")

#             params.extend([fecha_inicio, fecha_fin])

#         

#         if estado:

#             if estado == 'vigente':

#                 conditions.append("c.activo = 1 AND c.fecha_finalizacion IS NULL")

#             elif estado == 'cancelada':

#                 conditions.append("c.activo = 0 AND c.fecha_cancelacion IS NOT NULL")

#             elif estado == 'finalizada':

#                 conditions.append("c.fecha_finalizacion IS NOT NULL")

#         

#         if conditions:

#             query += " WHERE " + " AND ".join(conditions)

#         

#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, params)

#             return [self._row_to_cotizacion(row) for row in cursor.fetchall()]



#     def get_cotizaciones_paginadas(

#         self, 

#         page: int = 1, 

#         per_page: int = 10,

#         activos_only: bool = True

#     ) -> Dict[str, Any]:

#         """

#         Obtiene cotizaciones con paginación.

#         """

#         offset = (page - 1) * per_page

#         base_query = "SELECT * FROM Cotizaciones"

#         count_query = "SELECT COUNT(*) FROM Cotizaciones"

#         

#         where_clause = " WHERE activo = 1" if activos_only else ""

#         order_clause = " ORDER BY fecha_creacion DESC"

#         pagination_clause = f" OFFSET {offset} ROWS FETCH NEXT {per_page} ROWS ONLY"

#         

#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             

#             # Obtener total de registros

#             cursor.execute(count_query + where_clause)

#             total = cursor.fetchone()[0]

#             

#             # Obtener datos paginados

#             cursor.execute(base_query + where_clause + order_clause + pagination_clause)

#             data = [self._row_to_cotizacion(row) for row in cursor.fetchall()]

#             

#             return {

#                 'data': data,

#                 'total': total,

#                 'pages': (total + per_page - 1) // per_page,

#                 'page': page

#             }



#     def create_cotizacion_with_servicios(

#         self, 

#         cotizacion: Cotizacion, 

#         servicios: List[Dict[str, Any]]

#     ) -> Cotizacion:

#         """

#         Crea una cotización junto con sus servicios en una transacción.

#         """

#         conn = self._get_connection()

#         cursor = conn.cursor()

#         try:

#             cursor.execute("BEGIN TRANSACTION")

#             

#             # Crear cotización

#             cotizacion_creada = self.create_cotizacion(cotizacion)

#             

#             # Insertar servicios

#             for servicio in servicios:

#                 cursor.execute(

#                     """INSERT INTO Cotizacion_Servicio 

#                     (id_cotizacion, nombre_servicio, cantidad, precio) 

#                     VALUES (?, ?, ?, ?)""",

#                     (cotizacion_creada.id_cotizacion, 

#                      servicio['nombre_servicio'],

#                      servicio['cantidad'], 

#                      servicio['precio'])

#                 )

#             

#             conn.commit()

#             return cotizacion_creada

#         except Exception as e:

#             conn.rollback()

#             raise e

#         finally:

#             conn.close()

#             

# #cotizacio_servicio_reporitory

# import pyodbc

# from datetime import datetime

# from typing import List, Optional

# from Models.cotizacion_servicio import CotizacionServicio  # Asegúrate de que la clase esté en este path



# class CotizacionServicioRepository:

#     def __init__(self, connection_string: str):

#         self.connection_string = connection_string



#     def _get_connection(self):

#         return pyodbc.connect(self.connection_string)



#     def create_cotizacion_servicio(self, cotizacion_servicio: CotizacionServicio) -> CotizacionServicio:

#         query = """

#         INSERT INTO Cotizacion_Servicio (

#             id_cotizacion, id_servicio, nombre_servicio, descripcion_servicio,

#             tipo_servicio, costo_servicio, cantidad_servicio, fecha_creacion_servicio,

#             activo, usuario_creador_servicio, fecha_actualizacion_servicio

#         )

#         OUTPUT INSERTED.id_cotizacion_servicio

#         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

#         """



#         params = (

#             cotizacion_servicio.id_cotizacion,

#             cotizacion_servicio.id_servicio,

#             cotizacion_servicio.nombre_servicio,

#             cotizacion_servicio.descripcion_servicio,

#             cotizacion_servicio.tipo_servicio,

#             cotizacion_servicio.costo_servicio,

#             cotizacion_servicio.cantidad_servicio,

#             cotizacion_servicio.fecha_creacion_servicio or datetime.now(),

#             cotizacion_servicio.activo,

#             cotizacion_servicio.usuario_creador_servicio,

#             cotizacion_servicio.fecha_actualizacion_servicio

#         )



#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, params)

#             inserted_id = cursor.fetchone()[0]

#             conn.commit()



#             return self.get_cotizacion_servicio(inserted_id)



#     def get_cotizacion_servicio(self, id_cotizacion_servicio: int) -> Optional[CotizacionServicio]:

#         query = "SELECT * FROM Cotizacion_Servicio WHERE id_cotizacion_servicio = ?"



#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, id_cotizacion_servicio)

#             row = cursor.fetchone()



#             if row:

#                 return self._row_to_cotizacion_servicio(row)

#             return None



#     def get_servicios_por_cotizacion(self, id_cotizacion: int, activos_only: bool = True) -> List[CotizacionServicio]:

#         query = "SELECT * FROM Cotizacion_Servicio WHERE id_cotizacion = ?"

#         if activos_only:

#             query += " AND activo = 1"



#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, id_cotizacion)

#             return [self._row_to_cotizacion_servicio(row) for row in cursor.fetchall()]



#     def update_cotizacion_servicio(self, id_cotizacion_servicio: int, cotizacion_servicio: CotizacionServicio) -> Optional[CotizacionServicio]:

#         query = """

#         UPDATE Cotizacion_Servicio

#         SET

#             id_cotizacion = ?,

#             id_servicio = ?,

#             nombre_servicio = ?,

#             descripcion_servicio = ?,

#             tipo_servicio = ?,

#             costo_servicio = ?,

#             cantidad_servicio = ?,

#             fecha_creacion_servicio = ?,

#             activo = ?,

#             usuario_creador_servicio = ?,

#             fecha_actualizacion_servicio = ?

#         WHERE id_cotizacion_servicio = ?

#         """



#         params = (

#             cotizacion_servicio.id_cotizacion,

#             cotizacion_servicio.id_servicio,

#             cotizacion_servicio.nombre_servicio,

#             cotizacion_servicio.descripcion_servicio,

#             cotizacion_servicio.tipo_servicio,

#             cotizacion_servicio.costo_servicio,

#             cotizacion_servicio.cantidad_servicio,

#             cotizacion_servicio.fecha_creacion_servicio,

#             cotizacion_servicio.activo,

#             cotizacion_servicio.usuario_creador_servicio,

#             cotizacion_servicio.fecha_actualizacion_servicio,

#             id_cotizacion_servicio

#         )



#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, params)

#             conn.commit()



#             if cursor.rowcount > 0:

#                 return self.get_cotizacion_servicio(id_cotizacion_servicio)

#             return None



#     def delete_cotizacion_servicio(self, id_cotizacion_servicio: int) -> bool:

#         # Marcamos como inactivo

#         query = "UPDATE Cotizacion_Servicio SET activo = 0 WHERE id_cotizacion_servicio = ?"



#         with self._get_connection() as conn:

#             cursor = conn.cursor()

#             cursor.execute(query, id_cotizacion_servicio)

#             conn.commit()

#             return cursor.rowcount > 0



#     def _row_to_cotizacion_servicio(self, row) -> CotizacionServicio:

#         return CotizacionServicio(

#             id_cotizacion_servicio=row.id_cotizacion_servicio,

#             id_cotizacion=row.id_cotizacion,

#             id_servicio=row.id_servicio,

#             nombre_servicio=row.nombre_servicio,

#             descripcion_servicio=row.descripcion_servicio,

#             tipo_servicio=row.tipo_servicio,

#             costo_servicio=row.costo_servicio,

#             cantidad_servicio=row.cantidad_servicio,

#             fecha_creacion_servicio=row.fecha_creacion_servicio,

#             activo=bool(row.activo),

#             usuario_creador_servicio=row.usuario_creador_servicio,

#             fecha_actualizacion_servicio=row.fecha_actualizacion_servicio

#         )



# y este controlador # Archivo: /siga_app/database/cotizacion_repo.py

# #cotizacion_control

# from typing import List, Optional

# from datetime import datetime

# from Models.cotizacion import Cotizacion

# from Repositorys.cotizacion_repository import CotizacionRepository



# class CotizacionController:

#     def init(self, connection_string: str):

#         self.repository = CotizacionRepository(connection_string)





#     def crear_cotizacion(self, cotizacion_data: dict) -> Cotizacion:

#         """

#         Crea una nueva cotización con validación básica de datos requeridos.

#         

#         Args:

#             cotizacion_data (dict): Datos de la cotización a crear.

#                 Debe incluir al menos 'id_cliente' y 'rfc_cliente'.

#             

#         Returns:

#             Cotizacion: La cotización creada con su ID asignado.

#             

#         Raises:

#             ValueError: Si faltan campos obligatorios.

#         """

#         if 'id_cliente' not in cotizacion_data or 'rfc_cliente' not in cotizacion_data:

#             raise ValueError("Los campos id_cliente y rfc_cliente son obligatorios")

#             

#         # Establecer fecha de creación si no se proporciona

#         if 'fecha_creacion' not in cotizacion_data:

#             cotizacion_data['fecha_creacion'] = datetime.now()

#             

#         cotizacion = Cotizacion(**cotizacion_data)

#         return self.repository.create_cotizacion(cotizacion)



#     def obtener_cotizacion(self, id_cotizacion: int) -> Optional[Cotizacion]:

#         """

#         Obtiene una cotización por su ID.

#         

#         Args:

#             id_cotizacion (int): ID de la cotización a buscar.

#             

#         Returns:

#             Optional[Cotizacion]: La cotización encontrada o None si no existe.

#         """

#         return self.repository.get_cotizacion(id_cotizacion)



#     def obtener_todas_cotizaciones(self, activas_only: bool = True) -> List[Cotizacion]:

#         """

#         Obtiene todas las cotizaciones, con opción de filtrar por activas.

#         

#         Args:

#             activas_only (bool): Si True (default), solo devuelve cotizaciones activas.

#             

#         Returns:

#             List[Cotizacion]: Lista de cotizaciones.

#         """

#         return self.repository.get_all_cotizaciones(activas_only)



#     def actualizar_cotizacion(self, id_cotizacion: int, cotizacion_data: dict) -> Optional[Cotizacion]:

#         """

#         Actualiza una cotización existente con los datos proporcionados.

#         

#         Args:

#             id_cotizacion (int): ID de la cotización a actualizar.

#             cotizacion_data (dict): Datos a actualizar (actualización parcial).

#             

#         Returns:

#             Optional[Cotizacion]: La cotización actualizada o None si no existe.

#         """

#         cotizacion_existente = self.repository.get_cotizacion(id_cotizacion)

#         if not cotizacion_existente:

#             return None

#             

#         # Combinar datos existentes con los nuevos

#         update_data = cotizacion_existente.dict()

#         update_data.update({k: v for k, v in cotizacion_data.items() if v is not None})

#         

#         cotizacion_actualizada = Cotizacion(**update_data)

#         return self.repository.update_cotizacion(id_cotizacion, cotizacion_actualizada)



#     def cancelar_cotizacion(self, id_cotizacion: int) -> bool:

#         """

#         Cancela una cotización (marca como inactiva y establece fecha de cancelación).

#         

#         Args:

#             id_cotizacion (int): ID de la cotización a cancelar.

#             

#         Returns:

#             bool: True si la operación fue exitosa, False en caso contrario.

#         """

#         cotizacion = self.repository.get_cotizacion(id_cotizacion)

#         if not cotizacion:

#             return False

#             

#         update_data = {

#             'activo': False,

#             'fecha_cancelacion': datetime.now()

#         }

#         

#         return self.actualizar_cotizacion(id_cotizacion, update_data) is not None



#     def activar_cotizacion(self, id_cotizacion: int) -> bool:

#         """

#         Reactiva una cotización cancelada previamente.

#         

#         Args:

#             id_cotizacion (int): ID de la cotización a reactivar.

#             

#         Returns:

#             bool: True si la operación fue exitosa, False en caso contrario.

#         """

#         cotizacion = self.repository.get_cotizacion(id_cotizacion)

#         if not cotizacion:

#             return False

#             

#         update_data = {

#             'activo': True,

#             'fecha_cancelacion': None,

#             'fecha_activacion': datetime.now()

#         }

#         

#         return self.actualizar_cotizacion(id_cotizacion, update_data) is not None



#     def buscar_por_cliente(self, id_cliente: int, solo_activas: bool = True) -> List[Cotizacion]:

#         """

#         Busca cotizaciones asociadas a un cliente específico.

#         

#         Args:

#             id_cliente (int): ID del cliente a buscar.

#             solo_activas (bool): Si True (default), solo devuelve cotizaciones activas.

#             

#         Returns:

#             List[Cotizacion]: Lista de cotizaciones del cliente.

#         """

#         todas = self.obtener_todas_cotizaciones(activas_only=False)

#         return [

#             c for c in todas 

#             if c.id_cliente == id_cliente and (not solo_activas or c.activo)

#         ]



#     def buscar_por_servicio(self, nombre_servicio: str, solo_activas: bool = True) -> List[Cotizacion]:

#         """

#         Busca cotizaciones que contengan un servicio con el nombre especificado.

#         

#         Args:

#             nombre_servicio (str): Nombre del servicio a buscar.

#             solo_activas (bool): Si True (default), solo devuelve cotizaciones activas.

#             

#         Returns:

#             List[Cotizacion]: Lista de cotizaciones que contienen el servicio.

#         """

#         resultados = self.repository.get_cotizaciones_by_servicio_nombre(nombre_servicio)

#         return [c for c in resultados if not solo_activas or c.activo]



#     def buscar_por_rango_fechas(

#         self, 

#         fecha_inicio: datetime, 

#         fecha_fin: datetime, 

#         solo_activas: bool = True

#     ) -> List[Cotizacion]:

#         """

#         Busca cotizaciones creadas en un rango de fechas específico.

#         

#         Args:

#             fecha_inicio (datetime): Fecha de inicio del rango.

#             fecha_fin (datetime): Fecha de fin del rango.

#             solo_activas (bool): Si True (default), solo devuelve cotizaciones activas.

#             

#         Returns:

#             List[Cotizacion]: Lista de cotizaciones en el rango de fechas.

#         """

#         todas = self.obtener_todas_cotizaciones(activas_only=False)

#         return [

#             c for c in todas 

#             if (c.fecha_creacion and fecha_inicio <= c.fecha_creacion <= fecha_fin)

#             and (not solo_activas or c.activo)

#         ]



#     def obtener_estadisticas(self) -> dict:

#         """

#         Obtiene estadísticas básicas de las cotizaciones.

#         

#         Returns:

#             dict: Diccionario con estadísticas como:

#                 {

#                     'total': int,

#                     'activas': int,

#                     'canceladas': int,

#                     'promedio_dias_vigencia': float

#                 }

#         """

#         cotizaciones = self.obtener_todas_cotizaciones(activas_only=False)

#         

#         if not cotizaciones:

#             return {

#                 'total': 0,

#                 'activas': 0,

#                 'canceladas': 0,

#                 'promedio_dias_vigencia': 0

#             }

#         

#         activas = sum(1 for c in cotizaciones if c.activo)

#         canceladas = len(cotizaciones) - activas

#         

#         # Calcular promedio de días de vigencia para cotizaciones finalizadas

#         vigentes = [

#             (c.fecha_finalizacion - c.fecha_creacion).days

#             for c in cotizaciones

#             if c.fecha_finalizacion and c.fecha_creacion

#         ]

#         promedio_vigencia = sum(vigentes) / len(vigentes) if vigentes else 0

#         

#         return {

#             'total': len(cotizaciones),

#             'activas': activas,

#             'canceladas': canceladas,

#             'promedio_dias_vigencia': promedio_vigencia

#         }  quiero que me ayudes por favor a hacer una opcion como esta pero de cotizaciones, que cree una cotizacion, que verifique a los clientes si existen  y sino que les diga que no existe y  vaya a la funcion de agregar cliente,( a agregar un servicio por favor y despues que termine pedir los datos de los servicios pida los materiales y que muestre los materiales que hay en la tabla materiales por favor )-> 