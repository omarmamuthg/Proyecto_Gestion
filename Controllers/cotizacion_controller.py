# # Archivo: /siga_app/database/cotizacion_repo.py
# #cotizacion_control
# from typing import List, Optional
# from datetime import datetime
# from Models.cotizacion import Cotizacion
# from Repositorys.cotizacion_repository import CotizacionRepository

# class CotizacionController:
#     def __init__(self, connection_string: str):
#         self.repository = CotizacionRepository(connection_string)


#     def crear_cotizacion(self, cotizacion_data: dict) -> Cotizacion:
#         """
#         Crea una nueva cotización con validación básica de datos requeridos.
        
#         Args:
#             cotizacion_data (dict): Datos de la cotización a crear.
#                 Debe incluir al menos 'id_cliente' y 'rfc_cliente'.
            
#         Returns:
#             Cotizacion: La cotización creada con su ID asignado.
            
#         Raises:
#             ValueError: Si faltan campos obligatorios.
#         """
#         if 'id_cliente' not in cotizacion_data or 'rfc_cliente' not in cotizacion_data:
#             raise ValueError("Los campos id_cliente y rfc_cliente son obligatorios")
            
#         # Establecer fecha de creación si no se proporciona
#         if 'fecha_creacion' not in cotizacion_data:
#             cotizacion_data['fecha_creacion'] = datetime.now()
            
#         cotizacion = Cotizacion(**cotizacion_data)
#         return self.repository.create_cotizacion(cotizacion)

#     def obtener_cotizacion(self, id_cotizacion: int) -> Optional[Cotizacion]:
#         """
#         Obtiene una cotización por su ID.
        
#         Args:
#             id_cotizacion (int): ID de la cotización a buscar.
            
#         Returns:
#             Optional[Cotizacion]: La cotización encontrada o None si no existe.
#         """
#         return self.repository.get_cotizacion(id_cotizacion)

#     def obtener_todas_cotizaciones(self, activas_only: bool = True) -> List[Cotizacion]:
#         """
#         Obtiene todas las cotizaciones, con opción de filtrar por activas.
        
#         Args:
#             activas_only (bool): Si True (default), solo devuelve cotizaciones activas.
            
#         Returns:
#             List[Cotizacion]: Lista de cotizaciones.
#         """
#         return self.repository.get_all_cotizaciones(activas_only)

#     def actualizar_cotizacion(self, id_cotizacion: int, cotizacion_data: dict) -> Optional[Cotizacion]:
#         """
#         Actualiza una cotización existente con los datos proporcionados.
        
#         Args:
#             id_cotizacion (int): ID de la cotización a actualizar.
#             cotizacion_data (dict): Datos a actualizar (actualización parcial).
            
#         Returns:
#             Optional[Cotizacion]: La cotización actualizada o None si no existe.
#         """
#         cotizacion_existente = self.repository.get_cotizacion(id_cotizacion)
#         if not cotizacion_existente:
#             return None
            
#         # Combinar datos existentes con los nuevos
#         update_data = cotizacion_existente.dict()
#         update_data.update({k: v for k, v in cotizacion_data.items() if v is not None})
        
#         cotizacion_actualizada = Cotizacion(**update_data)
#         return self.repository.update_cotizacion(id_cotizacion, cotizacion_actualizada)

#     def cancelar_cotizacion(self, id_cotizacion: int) -> bool:
#         """
#         Cancela una cotización (marca como inactiva y establece fecha de cancelación).
        
#         Args:
#             id_cotizacion (int): ID de la cotización a cancelar.
            
#         Returns:
#             bool: True si la operación fue exitosa, False en caso contrario.
#         """
#         cotizacion = self.repository.get_cotizacion(id_cotizacion)
#         if not cotizacion:
#             return False
            
#         update_data = {
#             'activo': False,
#             'fecha_cancelacion': datetime.now()
#         }
        
#         return self.actualizar_cotizacion(id_cotizacion, update_data) is not None

#     def activar_cotizacion(self, id_cotizacion: int) -> bool:
#         """
#         Reactiva una cotización cancelada previamente.
        
#         Args:
#             id_cotizacion (int): ID de la cotización a reactivar.
            
#         Returns:
#             bool: True si la operación fue exitosa, False en caso contrario.
#         """
#         cotizacion = self.repository.get_cotizacion(id_cotizacion)
#         if not cotizacion:
#             return False
            
#         update_data = {
#             'activo': True,
#             'fecha_cancelacion': None,
#             'fecha_activacion': datetime.now()
#         }
        
#         return self.actualizar_cotizacion(id_cotizacion, update_data) is not None

#     def buscar_por_cliente(self, id_cliente: int, solo_activas: bool = True) -> List[Cotizacion]:
#         """
#         Busca cotizaciones asociadas a un cliente específico.
        
#         Args:
#             id_cliente (int): ID del cliente a buscar.
#             solo_activas (bool): Si True (default), solo devuelve cotizaciones activas.
            
#         Returns:
#             List[Cotizacion]: Lista de cotizaciones del cliente.
#         """
#         todas = self.obtener_todas_cotizaciones(activas_only=False)
#         return [
#             c for c in todas 
#             if c.id_cliente == id_cliente and (not solo_activas or c.activo)
#         ]

#     def buscar_por_servicio(self, nombre_servicio: str, solo_activas: bool = True) -> List[Cotizacion]:
#         """
#         Busca cotizaciones que contengan un servicio con el nombre especificado.
        
#         Args:
#             nombre_servicio (str): Nombre del servicio a buscar.
#             solo_activas (bool): Si True (default), solo devuelve cotizaciones activas.
            
#         Returns:
#             List[Cotizacion]: Lista de cotizaciones que contienen el servicio.
#         """
#         resultados = self.repository.get_cotizaciones_by_servicio_nombre(nombre_servicio)
#         return [c for c in resultados if not solo_activas or c.activo]

#     def buscar_por_rango_fechas(
#         self, 
#         fecha_inicio: datetime, 
#         fecha_fin: datetime, 
#         solo_activas: bool = True
#     ) -> List[Cotizacion]:
#         """
#         Busca cotizaciones creadas en un rango de fechas específico.
        
#         Args:
#             fecha_inicio (datetime): Fecha de inicio del rango.
#             fecha_fin (datetime): Fecha de fin del rango.
#             solo_activas (bool): Si True (default), solo devuelve cotizaciones activas.
            
#         Returns:
#             List[Cotizacion]: Lista de cotizaciones en el rango de fechas.
#         """
#         todas = self.obtener_todas_cotizaciones(activas_only=False)
#         return [
#             c for c in todas 
#             if (c.fecha_creacion and fecha_inicio <= c.fecha_creacion <= fecha_fin)
#             and (not solo_activas or c.activo)
#         ]

#     def obtener_estadisticas(self) -> dict:
#         """
#         Obtiene estadísticas básicas de las cotizaciones.
        
#         Returns:
#             dict: Diccionario con estadísticas como:
#                 {
#                     'total': int,
#                     'activas': int,
#                     'canceladas': int,
#                     'promedio_dias_vigencia': float
#                 }
#         """
#         cotizaciones = self.obtener_todas_cotizaciones(activas_only=False)
        
#         if not cotizaciones:
#             return {
#                 'total': 0,
#                 'activas': 0,
#                 'canceladas': 0,
#                 'promedio_dias_vigencia': 0
#             }
        
#         activas = sum(1 for c in cotizaciones if c.activo)
#         canceladas = len(cotizaciones) - activas
        
#         # Calcular promedio de días de vigencia para cotizaciones finalizadas
#         vigentes = [
#             (c.fecha_finalizacion - c.fecha_creacion).days
#             for c in cotizaciones
#             if c.fecha_finalizacion and c.fecha_creacion
#         ]
#         promedio_vigencia = sum(vigentes) / len(vigentes) if vigentes else 0
        
#         return {
#             'total': len(cotizaciones),
#             'activas': activas,
#             'canceladas': canceladas,
#             'promedio_dias_vigencia': promedio_vigencia
#         }



# from typing import List, Optional
# from datetime import datetime
# from Models.cotizacion import Cotizacion
# from Repositorys.cotizacion_repository import CotizacionRepository

# class CotizacionController:
#     def __init__(self, connection_string: str):
#         self.repository = CotizacionRepository(connection_string)

#     def crear_cotizacion(self, cotizacion_data: dict) -> Cotizacion:
#         """
#         Crea una nueva cotización con validación básica de datos requeridos.

#         Args:
#             cotizacion_data (dict): Datos de la cotización a crear.
#                 Debe incluir al menos 'id_cliente' y 'rfc_cliente'.

#         Returns:
#             Cotizacion: La cotización creada con su ID asignado.

#         Raises:
#             ValueError: Si faltan campos obligatorios.
#         """
#         if 'id_cliente' not in cotizacion_data or 'rfc_cliente' not in cotizacion_data:
#             raise ValueError("Los campos id_cliente y rfc_cliente son obligatorios")

#         # Establecer fecha de creación si no se proporciona
#         if 'fecha_creacion' not in cotizacion_data:
#             cotizacion_data['fecha_creacion'] = datetime.now()

#         cotizacion = Cotizacion(**cotizacion_data)
#         return self.repository.create_cotizacion(cotizacion)

#     def obtener_cotizacion(self, id_cotizacion: int) -> Optional[Cotizacion]:
#         """
#         Obtiene una cotización por su ID.

#         Args:
#             id_cotizacion (int): ID de la cotización a buscar.

#         Returns:
#             Optional[Cotizacion]: La cotización encontrada o None si no existe.
#         """
#         return self.repository.get_cotizacion(id_cotizacion)

#     def obtener_todas_cotizaciones(self, activas_only: bool = True) -> List[Cotizacion]:
#         """
#         Obtiene todas las cotizaciones, con opción de filtrar por activas.

#         Args:
#             activas_only (bool): Si True (default), solo devuelve cotizaciones activas.

#         Returns:
#             List[Cotizacion]: Lista de cotizaciones.
#         """
#         return self.repository.get_all_cotizaciones(activas_only)

#     def actualizar_cotizacion(self, id_cotizacion: int, cotizacion_data: dict) -> Optional[Cotizacion]:
#         """
#         Actualiza una cotización existente con los datos proporcionados.

#         Args:
#             id_cotizacion (int): ID de la cotización a actualizar.
#             cotizacion_data (dict): Datos a actualizar (actualización parcial).

#         Returns:
#             Optional[Cotizacion]: La cotización actualizada o None si no existe.
#         """
#         cotizacion_existente = self.repository.get_cotizacion(id_cotizacion)
#         if not cotizacion_existente:
#             return None

#         # Combinar datos existentes con los nuevos
#         update_data = cotizacion_existente.dict()
#         update_data.update({k: v for k, v in cotizacion_data.items() if v is not None})

#         cotizacion_actualizada = Cotizacion(**update_data)
#         return self.repository.update_cotizacion(id_cotizacion, cotizacion_actualizada)

#     def cancelar_cotizacion(self, id_cotizacion: int) -> bool:
#         """
#         Cancela una cotización (marca como inactiva y establece fecha de cancelación).

#         Args:
#             id_cotizacion (int): ID de la cotización a cancelar.

#         Returns:
#             bool: True si la operación fue exitosa, False en caso contrario.
#         """
#         cotizacion = self.repository.get_cotizacion(id_cotizacion)
#         if not cotizacion:
#             return False

#         update_data = {
#             'activo': False,
#             'fecha_cancelacion': datetime.now()
#         }

#         return self.actualizar_cotizacion(id_cotizacion, update_data) is not None

#     def activar_cotizacion(self, id_cotizacion: int) -> bool:
#         """
#         Reactiva una cotización cancelada previamente.

#         Args:
#             id_cotizacion (int): ID de la cotización a reactivar.

#         Returns:
#             bool: True si la operación fue exitosa, False en caso contrario.
#         """
#         cotizacion = self.repository.get_cotizacion(id_cotizacion)
#         if not cotizacion:
#             return False

#         update_data = {
#             'activo': True,
#             'fecha_cancelacion': None,
#             'fecha_activacion': datetime.now()
#         }

#         return self.actualizar_cotizacion(id_cotizacion, update_data) is not None

#     def buscar_por_cliente(self, id_cliente: int, solo_activas: bool = True) -> List[Cotizacion]:
#         """
#         Busca cotizaciones asociadas a un cliente específico.

#         Args:
#             id_cliente (int): ID del cliente a buscar.
#             solo_activas (bool): Si True (default), solo devuelve cotizaciones activas.

#         Returns:
#             List[Cotizacion]: Lista de cotizaciones del cliente.
#         """
#         todas = self.obtener_todas_cotizaciones(activas_only=False)
#         return [
#             c for c in todas
#             if c.id_cliente == id_cliente and (not solo_activas or c.activo)
#         ]

#     def buscar_por_servicio(self, nombre_servicio: str, solo_activas: bool = True) -> List[Cotizacion]:
#         """
#         Busca cotizaciones que contengan un servicio con el nombre especificado.

#         Args:
#             nombre_servicio (str): Nombre del servicio a buscar.
#             solo_activas (bool): Si True (default), solo devuelve cotizaciones activas.

#         Returns:
#             List[Cotizacion]: Lista de cotizaciones que contienen el servicio.
#         """
#         resultados = self.repository.get_cotizaciones_by_servicio_nombre(nombre_servicio)
#         return [c for c in resultados if not solo_activas or c.activo]

#     def buscar_por_rango_fechas(
#         self,
#         fecha_inicio: datetime,
#         fecha_fin: datetime,
#         solo_activas: bool = True
#     ) -> List[Cotizacion]:
#         """
#         Busca cotizaciones creadas en un rango de fechas específico.

#         Args:
#             fecha_inicio (datetime): Fecha de inicio del rango.
#             fecha_fin (datetime): Fecha de fin del rango.
#             solo_activas (bool): Si True (default), solo devuelve cotizaciones activas.

#         Returns:
#             List[Cotizacion]: Lista de cotizaciones en el rango de fechas.
#         """
#         todas = self.obtener_todas_cotizaciones(activas_only=False)
#         return [
#             c for c in todas
#             if (c.fecha_creacion and fecha_inicio <= c.fecha_creacion <= fecha_fin)
#             and (not solo_activas or c.activo)
#         ]

#     def obtener_estadisticas(self) -> dict:
#         """
#         Obtiene estadísticas básicas de las cotizaciones.

#         Returns:
#             dict: Diccionario con estadísticas como:
#                 {
#                     'total': int,
#                     'activas': int,
#                     'canceladas': int,
#                     'promedio_dias_vigencia': float
#                 }
#         """
#         cotizaciones = self.obtener_todas_cotizaciones(activas_only=False)

#         if not cotizaciones:
#             return {
#                 'total': 0,
#                 'activas': 0,
#                 'canceladas': 0,
#                 'promedio_dias_vigencia': 0
#             }

#         activas = sum(1 for c in cotizaciones if c.activo)
#         canceladas = len(cotizaciones) - activas

#         # Calcular promedio de días de vigencia para cotizaciones finalizadas
#         vigentes = [
#             (c.fecha_finalizacion - c.fecha_creacion).days
#             for c in cotizaciones
#             if c.fecha_finalizacion and c.fecha_creacion
#         ]
#         promedio_vigencia = sum(vigentes) / len(vigentes) if vigentes else 0

#         return {
#             'total': len(cotizaciones),
#             'activas': activas,
#             'canceladas': canceladas,
#             'promedio_dias_vigencia': promedio_vigencia
#         }






# #cotizacion_control
from typing import List, Optional
from datetime import datetime
from Models.cotizacion import Cotizacion
from Repositorys.cotizacion_repository import CotizacionRepository

class CotizacionController:
    def __init__(self, connection_string: str):
        self.repository = CotizacionRepository(connection_string)

    def crear_cotizacion(self, cotizacion_data: dict) -> Cotizacion:
        """
        Crea una nueva cotización con validación básica de datos requeridos.

        Args:
            cotizacion_data (dict): Datos de la cotización a crear.
                Debe incluir al menos 'id_cliente' y 'rfc_cliente' con valores no nulos o vacíos.

        Returns:
            Cotizacion: La cotización creada con su ID asignado.

        Raises:
            ValueError: Si faltan campos obligatorios o si sus valores son nulos o vacíos.
        """
        if not cotizacion_data.get('id_cliente'):
            raise ValueError("El campo id_cliente es obligatorio")
        if not cotizacion_data.get('rfc_cliente'):
            raise ValueError("El campo rfc_cliente es obligatorio")

        # Establecer fecha de creación si no se proporciona
        if 'fecha_creacion' not in cotizacion_data:
            cotizacion_data['fecha_creacion'] = datetime.now()

        cotizacion = Cotizacion(**cotizacion_data)
        return self.repository.create_cotizacion(cotizacion)

    def obtener_cotizacion(self, id_cotizacion: int) -> Optional[Cotizacion]:
        """
        Obtiene una cotización por su ID.

        Args:
            id_cotizacion (int): ID de la cotización a buscar.

        Returns:
            Optional[Cotizacion]: La cotización encontrada o None si no existe.
        """
        return self.repository.get_cotizacion(id_cotizacion)

    def obtener_todas_cotizaciones(self, activas_only: bool = True) -> List[Cotizacion]:
        """
        Obtiene todas las cotizaciones, con opción de filtrar por activas.

        Args:
            activas_only (bool): Si True (default), solo devuelve cotizaciones activas.

        Returns:
            List[Cotizacion]: Lista de cotizaciones.
        """
        return self.repository.get_all_cotizaciones(activas_only)

    def actualizar_cotizacion(self, id_cotizacion: int, cotizacion_data: dict) -> Optional[Cotizacion]:
        """
        Actualiza una cotización existente con los datos proporcionados.

        Args:
            id_cotizacion (int): ID de la cotización a actualizar.
            cotizacion_data (dict): Datos a actualizar (actualización parcial).

        Returns:
            Optional[Cotizacion]: La cotización actualizada o None si no existe.
        """
        cotizacion_existente = self.repository.get_cotizacion(id_cotizacion)
        if not cotizacion_existente:
            return None

        # Combinar datos existentes con los nuevos
        update_data = cotizacion_existente.dict()
        update_data.update({k: v for k, v in cotizacion_data.items() if v is not None})

        cotizacion_actualizada = Cotizacion(**update_data)
        return self.repository.update_cotizacion(id_cotizacion, cotizacion_actualizada)

    def cancelar_cotizacion(self, id_cotizacion: int) -> bool:
        """
        Cancela una cotización (marca como inactiva y establece fecha de cancelación).

        Args:
            id_cotizacion (int): ID de la cotización a cancelar.

        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        cotizacion = self.repository.get_cotizacion(id_cotizacion)
        if not cotizacion:
            return False

        update_data = {
            'activo': False,
            'fecha_cancelacion': datetime.now()
        }

        return self.actualizar_cotizacion(id_cotizacion, update_data) is not None

    def activar_cotizacion(self, id_cotizacion: int) -> bool:
        """
        Reactiva una cotización cancelada previamente.

        Args:
            id_cotizacion (int): ID de la cotización a reactivar.

        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        cotizacion = self.repository.get_cotizacion(id_cotizacion)
        if not cotizacion:
            return False

        update_data = {
            'activo': True,
            'fecha_cancelacion': None,
            'fecha_activacion': datetime.now()
        }

        return self.actualizar_cotizacion(id_cotizacion, update_data) is not None

    def buscar_por_cliente(self, id_cliente: int, solo_activas: bool = True) -> List[Cotizacion]:
        """
        Busca cotizaciones asociadas a un cliente específico.

        Args:
            id_cliente (int): ID del cliente a buscar.
            solo_activas (bool): Si True (default), solo devuelve cotizaciones activas.

        Returns:
            List[Cotizacion]: Lista de cotizaciones del cliente.
        """
        todas = self.obtener_todas_cotizaciones(activas_only=False)
        return [
            c for c in todas
            if c.id_cliente == id_cliente and (not solo_activas or c.activo)
        ]

    def buscar_por_servicio(self, nombre_servicio: str, solo_activas: bool = True) -> List[Cotizacion]:
        """
        Busca cotizaciones que contengan un servicio con el nombre especificado.

        Args:
            nombre_servicio (str): Nombre del servicio a buscar.
            solo_activas (bool): Si True (default), solo devuelve cotizaciones activas.

        Returns:
            List[Cotizacion]: Lista de cotizaciones que contienen el servicio.
        """
        resultados = self.repository.get_cotizaciones_by_servicio_nombre(nombre_servicio)
        return [c for c in resultados if not solo_activas or c.activo]

    def buscar_por_rango_fechas(
        self,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        solo_activas: bool = True
    ) -> List[Cotizacion]:
        """
        Busca cotizaciones creadas en un rango de fechas específico.

        Args:
            fecha_inicio (datetime): Fecha de inicio del rango.
            fecha_fin (datetime): Fecha de fin del rango.
            solo_activas (bool): Si True (default), solo devuelve cotizaciones activas.

        Returns:
            List[Cotizacion]: Lista de cotizaciones en el rango de fechas.
        """
        todas = self.obtener_todas_cotizaciones(activas_only=False)
        return [
            c for c in todas
            if (c.fecha_creacion and fecha_inicio <= c.fecha_creacion <= fecha_fin)
            and (not solo_activas or c.activo)
        ]

    def obtener_estadisticas(self) -> dict:
        """
        Obtiene estadísticas básicas de las cotizaciones.

        Returns:
            dict: Diccionario con estadísticas como:
                {
                    'total': int,
                    'activas': int,
                    'canceladas': int,
                    'promedio_dias_vigencia': float
                }
        """
        cotizaciones = self.obtener_todas_cotizaciones(activas_only=False)

        if not cotizaciones:
            return {
                'total': 0,
                'activas': 0,
                'canceladas': 0,
                'promedio_dias_vigencia': 0
            }

        activas = sum(1 for c in cotizaciones if c.activo)
        canceladas = len(cotizaciones) - activas

        # Calcular promedio de días de vigencia para cotizaciones finalizadas
        vigentes = [
            (c.fecha_finalizacion - c.fecha_creacion).days
            for c in cotizaciones
            if c.fecha_finalizacion and c.fecha_creacion
        ]
        promedio_vigencia = sum(vigentes) / len(vigentes) if vigentes else 0

        return {
            'total': len(cotizaciones),
            'activas': activas,
            'canceladas': canceladas,
            'promedio_dias_vigencia': promedio_vigencia
        }
    