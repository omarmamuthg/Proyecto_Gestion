# menu/main.py
import sys
from pathlib import Path
from datetime import datetime
import uuid 
from pdf import generar_pdf_cotizacion

# Esto permite que Python encuentre tus módulos
sys.path.append(str(Path(__file__).parent.parent))

# Importaciones corregidas
# from funciones_menu import Logo_siga, menu_principal, menu_clientes, pedir_opcion_menu, pedir_opcion_submenu, menu_cotizaciones, menu_proveedores,limpiar_pantalla,SubMenuInput, MenuInput,menu_materiales
# from typing import Literal
# import os
# from pydantic import BaseModel, ValidationError
# from Controllers.proveedor_controller import ProveedorController
# from Controllers.cliente_controller import ClienteController
# from Controllers.material_controller import MaterialController
# from datetime import datetime
# from decimal import Decimal
# from Controllers.cotizacion_controller import CotizacionController
# from Repositorys.cotizacion_repository import CotizacionRepository
# from Repositorys.cotizacion_servicio_repository import CotizacionServicioRepository
# from Models.cotizacion import Cotizacion
# # from Models.cotizacion_servicio import CotizacionServicioRepository
# from Repositorys.cotizacion_servicio_repository import CotizacionServicioRepository
# from Models.cotizacion_servicio import CotizacionServicio
# from Repositorys.cotizacion_servicio_repository import CotizacionServicioRepository
# from Repositorys.cotizacion_servicio_repository import CotizacionServicioRepository
# from Models.cotizacion_servicio import CotizacionServicio
# from Models.cotizacion_servicio import CotizacionServicio
# from Repositorys.cotizacion_servicio_repository import CotizacionServicioRepository
# from Repositorys.proveedor_material_repository import ProveedorMaterialRepository
from funciones_menu import Logo_siga, menu_principal, menu_clientes, pedir_opcion_menu, pedir_opcion_submenu, pedir_opcion_submenu_coti, menu_cotizaciones, menu_proveedores, limpiar_pantalla, SubMenuInput, MenuInput, menu_materiales
from typing import Literal
import os
from pydantic import BaseModel, ValidationError
from Controllers.proveedor_controller import ProveedorController
from Controllers.cliente_controller import ClienteController
from Controllers.material_controller import MaterialController
from datetime import datetime
from decimal import Decimal
from Controllers.cotizacion_controller import CotizacionController
from Repositorys.cotizacion_repository import CotizacionRepository
from Repositorys.cotizacion_servicio_repository import CotizacionServicioRepository
from Models.cotizacion import Cotizacion
from Models.cotizacion_servicio import CotizacionServicio
from Repositorys.proveedor_material_repository import ProveedorMaterialRepository
from Controllers.proveedor_material_controller import ProveedorMaterialController
from Controllers.cotizacion_material_contoller import CotizacionMaterialController
from Repositorys.cotizacion_material_repository import CotizacionMaterialRepository


# Cadena de conexión (la misma que ya tienes)
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=OMARLAPTOP;'
    'DATABASE=DB_SIGA;'
    'UID=DB_SIGA;'
    'PWD=db_siga'
)


# # Clase que valida que solo se pueda ingresar una de las opciones válidas del menú (1, 2 o 3)
# class MenuInput(BaseModel):
#     opcion: Literal["1", "2", "3"]  # Solo acepta estas tres cadenas como entrada


# # Clase que valida que solo se pueda ingresar una de las opciones válidas del menú (1, 2 o 3)
# class SubMenuInput(BaseModel):
#     opcionSub: Literal["1", "2", "3", "4", "5", "6"]  # Solo acepta estas tres cadenas como entrada


# # Función que limpia la pantalla del sistema (solo funciona en Windows por el 'cls')
# def limpiar_pantalla():
#     os.system("cls")

# Bucle principal que mantiene el programa corriendo hasta que se indique salir (con break)
while True:
    # Muestra el logo y el menú principal
    Logo_siga()
    menu_principal()

    # Pide al usuario que seleccione una opción del menú
    entrada = pedir_opcion_menu()

    # Limpia la pantalla después de elegir una opción
    limpiar_pantalla()

    # Si el usuario elige "1", se accede al menú de Clientes
    if entrada.opcion == "1":
        while True:
            print("Has seleccionado Cliente.")
            menu_clientes()  # Muestra las opciones relacionadas con Clientes
            entrada_cliente = pedir_opcion_submenu()  # Pide la siguiente opción del submenú
            limpiar_pantalla()

            # Sub-opciones del menú Cliente
            if entrada_cliente.opcionSub == "1":
                while True:
                    print("\n=== Agregar Cliente ===")
                    print("Los campos marcados con (*) son obligatorios")
                    print("Ingrese '0' en el nombre para cancelar y volver al menú anterior\n")
                    controller = ClienteController(connection_string)
                    
                    datos_cliente = {}
                    errores = []

                    def validar_campo(valor, campo, tipo="texto", longitud=None, obligatorio=True):
                        valor = valor.strip() if valor else ""
                        if obligatorio and not valor:
                            errores.append(f"- El campo {campo} es obligatorio")
                            return False
                            
                        if tipo == "nombre":
                            if valor.isdigit():
                                errores.append(f"- El campo {campo} no puede ser solo números")
                                return False
                                
                        if tipo == "telefono":
                            if valor and not valor.isdigit():
                                errores.append(f"- El teléfono solo debe contener números")
                                return False
                            if valor and len(valor) != 10:
                                errores.append(f"- El teléfono debe tener exactamente 10 dígitos")
                                return False
                                
                        if tipo == "email" and valor:
                            if "@" not in valor or "." not in valor:
                                errores.append(f"- Formato de email inválido (debe contener @ y dominio)")
                                return False
                                
                        if tipo == "rfc" and valor and len(valor) != 13:
                            errores.append(f"- El RFC debe tener exactamente 13 caracteres")
                            return False
                            
                        if tipo == "tipo_cliente" and valor not in ["Persona Fisica", "Persona Moral"]:
                            errores.append(f"- Tipo de cliente inválido (debe ser 'Persona Fisica' o 'Persona Moral')")
                            return False
                            
                        return True

                    try:
                        # Solo el primer campo tiene opción de cancelación
                        datos_cliente["nombre"] = input("Nombre/Razón Social (*): ").upper()
                        if datos_cliente["nombre"] == "0":
                            print("\nOperación cancelada por el usuario")
                            limpiar_pantalla()
                            break
                            
                        # Resto de campos sin opción de cancelación
                        datos_cliente["tipo_cliente"] = input("Tipo de cliente (Persona Física/Persona Moral) (*): ").title()
                        datos_cliente["rfc"] = input("RFC (13 caracteres) (*): ").upper()
                        datos_cliente["telefono"] = input("Teléfono (10 dígitos) (*): ").upper()
                        datos_cliente["correo"] = input("Correo electrónico [Opcional]: ").lower()
                        datos_cliente["direccion"] = input("Dirección [Opcional]: ").upper()
                        datos_cliente["comentarios"] = input("Comentarios/Notas [Opcional]: ").capitalize()
                        
                        # Validaciones
                        validar_campo(datos_cliente["nombre"], "Nombre/Razón Social", tipo="nombre", obligatorio=True)
                        validar_campo(datos_cliente["tipo_cliente"], "Tipo de cliente", tipo="tipo_cliente", obligatorio=True)
                        validar_campo(datos_cliente["rfc"], "RFC", tipo="rfc", obligatorio=True)
                        validar_campo(datos_cliente["telefono"], "Teléfono", tipo="telefono", obligatorio=True)
                        validar_campo(datos_cliente["correo"], "Correo", tipo="email", obligatorio=False)
                        
                        if errores:
                            print("\n❌ Errores encontrados:")
                            print("\n".join(errores))
                            input("\nPresione Enter para corregir los datos...")
                            limpiar_pantalla()
                            continue

                        # Mostrar resumen
                        print("\n" + "="*40)
                        print("📋 RESUMEN DEL CLIENTE A REGISTRAR")
                        print("="*40)
                        print(f"🔹 Nombre/Razón Social: {datos_cliente['nombre']}")
                        print(f"🔹 Tipo de Cliente: {datos_cliente['tipo_cliente']}")
                        print(f"🔹 RFC: {datos_cliente['rfc']}")
                        print(f"🔹 Teléfono: {datos_cliente['telefono'] or 'No especificado'}")
                        print(f"🔹 Correo: {datos_cliente['correo'] or 'No especificado'}")
                        print(f"🔹 Dirección: {datos_cliente['direccion'] or 'No especificado'}")
                        print(f"🔹 Comentarios: {datos_cliente['comentarios'] or 'Ninguno'}")
                        print("="*40)
                        
                        confirmar = input("\n¿Confirmar creación de cliente? (s/n): ").lower()
                        if confirmar != 's':
                            print("❌ Operación cancelada")
                            limpiar_pantalla()
                            break
                        
                        # Crear el cliente
                        cliente_creado = controller.crear_cliente({
                            'nombre': datos_cliente['nombre'].strip(),
                            'tipo_cliente': datos_cliente['tipo_cliente'].strip(),
                            'rfc': datos_cliente['rfc'].strip(),
                            'telefono': datos_cliente['telefono'].strip() if datos_cliente['telefono'] else None,
                            'correo': datos_cliente['correo'].strip() if datos_cliente['correo'] else None,
                            'direccion': datos_cliente['direccion'].strip() if datos_cliente['direccion'] else None,
                            'comentarios': datos_cliente['comentarios'].strip() if datos_cliente['comentarios'] else None
                        })
                        
                        if cliente_creado:
                            print(f"\n✅ Cliente creado exitosamente con ID: {cliente_creado.id_cliente}")
                            input("\nPresione Enter para continuar...")
                            limpiar_pantalla()
                            break
                        else:
                            print("\n❌ Error al crear el cliente")
                            
                    except Exception as e:
                        print(f"\n❌ Error inesperado: {str(e)}")
                        input("\nPresione Enter para continuar...")



            elif entrada_cliente.opcionSub == "2":
                while True:
                    print("\n=== Editar Cliente ===")
                    controller = ClienteController(connection_string)  # Instancia local del controlador
                    
                    try:
                        # Obtener lista de clientes activos
                        clientes = controller.obtener_todos_clientes(activos_only=True)
                        
                        if not clientes:
                            print("\n❌ No hay clientes activos registrados")
                        else:
                            print("\nClientes disponibles (ACTIVOS):")
                            for c in clientes:
                                print(f"ID: {c.id_cliente} - {c.nombre}")
                            
                            # Validación del ID
                            try:
                                id_editar = int(input("\nIngrese el ID del cliente a editar (0 para cancelar): "))
                                if id_editar == 0:
                                    limpiar_pantalla()
                                    print("Operación cancelada")
                                    break
                                else:
                                    cliente = controller.obtener_cliente(id_editar)
                                    
                                    if not cliente:
                                        print("\n❌ No existe un cliente con ese ID o está inactivo")
                                    else:
                                        print("\nDatos actuales del cliente:")
                                        print(f"1. Nombre/Razón Social: {cliente.nombre}")
                                        print(f"2. Tipo de Cliente: {cliente.tipo_cliente}")
                                        print(f"3. Teléfono: {cliente.telefono}")
                                        print(f"4. Correo: {cliente.correo}")
                                        print(f"5. RFC: {cliente.rfc}")
                                        print(f"6. Dirección: {cliente.direccion}")
                                        print(f"7. Comentarios: {cliente.comentarios}")
                                        
                                        # Diccionario para almacenar cambios
                                        updates = {}
                                        errores = []
                                        
                                        # Función de validación
                                        def validar_campo(valor, campo, tipo="texto", longitud=None):
                                            valor = valor.strip()
                                            if valor:  # Solo validar si hay valor (campos opcionales)
                                                if tipo == "telefono":
                                                    if not valor.isdigit():
                                                        errores.append(f"El teléfono debe contener solo números")
                                                        return False
                                                    if len(valor) != 10:
                                                        errores.append(f"El teléfono debe tener 10 dígitos")
                                                        return False
                                                elif tipo == "email":
                                                    if "@" not in valor or "." not in valor:
                                                        errores.append(f"Formato de email inválido")
                                                        return False
                                                elif tipo == "rfc" and len(valor) != 13:
                                                    errores.append(f"El RFC debe tener 13 caracteres")
                                                    return False
                                                elif tipo == "tipo_cliente":
                                                    if valor not in ["Persona Fisica", "Persona Moral"]:
                                                        errores.append(f"Tipo de cliente inválido")
                                                        return False
                                            return True
                                        
                                        # Función para corregir el tipo de cliente
                                        def formatear_tipo_cliente(texto: str) -> str:
                                            texto = texto.strip().title()
                                            if "Fisica" in texto:
                                                return "Persona Fisica"
                                            return texto
                                        
                                        # Recoger nuevos valores
                                        nuevos_datos = {
                                            "nombre": input("\nNuevo nombre (ENTER para mantener actual): ").strip().upper(),
                                            "tipo_cliente": formatear_tipo_cliente(input("Nuevo tipo (Persona Fisica/Persona Moral, ENTER para mantener actual): ")),
                                            "telefono": input("Nuevo teléfono (10 dígitos, ENTER para mantener actual): ").strip(),
                                            "correo": input("Nuevo correo (ENTER para mantener actual): ").strip().lower(),
                                            "rfc": input("Nuevo RFC (13 caracteres, ENTER para mantener actual): ").strip().upper(),
                                            "direccion": input("Nueva dirección (ENTER para mantener actual): ").strip().upper(),
                                            "comentarios": input("Nuevos comentarios (ENTER para mantener actual): ").strip().capitalize()
                                        }
                                        
                                        # Validar campos modificados
                                        if nuevos_datos["telefono"]:
                                            validar_campo(nuevos_datos["telefono"], "teléfono", "telefono")
                                        if nuevos_datos["correo"]:
                                            validar_campo(nuevos_datos["correo"], "correo", "email")
                                        if nuevos_datos["rfc"]:
                                            validar_campo(nuevos_datos["rfc"], "RFC", "rfc")
                                        if nuevos_datos["tipo_cliente"]:
                                            validar_campo(nuevos_datos["tipo_cliente"], "tipo_cliente", "tipo_cliente")
                                        
                                        if errores:
                                            print("\n❌ Errores encontrados:")
                                            for error in errores:
                                                print(f"- {error}")
                                        else:
                                            # Preparar datos para actualizar (solo campos modificados)
                                            updates = {k: v for k, v in nuevos_datos.items() if v}
                                            
                                            if updates:
                                                # Mostrar resumen de cambios
                                                print("\nResumen de cambios:")
                                                for campo, valor in updates.items():
                                                    print(f"{campo}: {valor}")
                                                
                                                confirmar = input("\n¿Confirmar cambios? (s/n): ").lower()
                                                if confirmar == 's':
                                                    resultado = controller.actualizar_cliente(id_editar, updates)
                                                    if resultado:
                                                        print("\n✅ Cliente actualizado exitosamente")
                                                        break
                                                    else:
                                                        print("\n❌ Error al actualizar el cliente")
                                                else:
                                                    print("Cambios cancelados")
                                            else:
                                                print("\n⚠️ No se realizaron cambios")
                            
                            except ValueError:
                                print("\n❌ Error: Debe ingresar un ID numérico válido")
                    
                    except Exception as e:
                        print(f"\n❌ Error inesperado: {str(e)}")
                    
                    input("\nPresione ENTER para continuar...")
                    limpiar_pantalla()
            elif entrada_cliente.opcionSub == "3":
                while True:
                    print("\n=== Eliminar Cliente (Marcar como Inactivo) ===")
                    controller = ClienteController(connection_string)  # Instancia local del controlador
                    
                    try:
                        # Obtener solo clientes activos
                        clientes = controller.obtener_todos_clientes(activos_only=True)
                        
                        if not clientes:
                            print("\nℹ️ No hay clientes activos registrados")
                        else:
                            print("\nClientes ACTIVOS disponibles:")
                            for c in clientes:
                                print(f"ID: {c.id_cliente} - {c.nombre} ({c.tipo_cliente})")
                            
                            # Validación del ID
                            try:
                                id_eliminar = input("\nIngrese el ID del cliente a eliminar (0 para cancelar): ").strip()
                                
                                if id_eliminar == "0":
                                    print("Operación cancelada")
                                    input("\nPresione ENTER para continuar...")
                                    limpiar_pantalla()
                                    break
                                else:
                                    id_eliminar = int(id_eliminar)  # Conversión a entero
                                    cliente = controller.obtener_cliente(id_eliminar)
                                    
                                    if not cliente or not cliente.activo:
                                        print("\n❌ No existe un cliente activo con ese ID")
                                    else:
                                        # Confirmación con detalles
                                        print("\n⚠️ ATENCIÓN: Esta acción marcará al cliente como INACTIVO")
                                        print(f"ID: {cliente.id_cliente}")
                                        print(f"Nombre/Razón Social: {cliente.nombre}")
                                        print(f"Tipo: {cliente.tipo_cliente}")
                                        print(f"RFC: {cliente.rfc}")
                                        
                                        confirmar = input("\n¿ESTÁ SEGURO que desea continuar? (s/n): ").lower()
                                        if confirmar == 's':
                                            if controller.eliminar_cliente(id_eliminar):
                                                print("\n✅ Cliente marcado como inactivo correctamente")
                                                # Mostrar datos del cliente eliminado
                                                cliente_eliminado = controller.obtener_cliente(id_eliminar)
                                                print(f"\nDetalles del cliente inactivado:")
                                                print(f"Estado actual: {'ACTIVO' if cliente_eliminado.activo else 'INACTIVO'}")
                                            else:
                                                print("\n❌ Error al marcar el cliente como inactivo")
                                        else:
                                            print("Operación cancelada por el usuario")
                                            limpiar_pantalla()
                                            # break
                            
                            except ValueError:
                                print("\n❌ Error: Debe ingresar un número válido")
                            except Exception as e:
                                print(f"\n❌ Error al procesar el ID: {str(e)}")
                    
                    except Exception as e:
                        print(f"\n❌ Error inesperado: {str(e)}")
                
    
                    input("\nPresione ENTER para continuar...")
                    limpiar_pantalla()
            elif entrada_cliente.opcionSub == "4":
                while True:
                    print("\n=== Buscar Cliente ===")
                    print("Ingrese '0' para cancelar y volver al menú anterior\n")
                    controller = ClienteController(connection_string)  # Instancia local del controlador
                    
                    try:
                        criterio = input("Ingrese ID, nombre, RFC o tipo (Fisica/Moral) del cliente: ").strip()
                        
                        if criterio == "0":
                            print("Operacion cancelada ")
                        elif not criterio:
                            print("\n❌ Debe ingresar un criterio de búsqueda")
                        else:
                            clientes = []
                            
                            # Búsqueda por ID si es numérico
                            if criterio.isdigit():
                                cliente = controller.obtener_cliente(int(criterio))
                                if cliente:
                                    clientes = [cliente]
                            else:
                                # Búsqueda por nombre, RFC o tipo en todos los clientes
                                todos_clientes = controller.obtener_todos_clientes(activos_only=False)
                                criterio_lower = criterio.lower()
                                clientes = [
                                    c for c in todos_clientes
                                    if (criterio_lower in c.nombre.lower() or
                                        (c.rfc and criterio_lower in c.rfc.lower()) or
                                        criterio_lower in c.tipo_cliente.lower())
                                ]
                            
                            if not clientes:
                                print("\n🔍 No se encontraron clientes con ese criterio")
                            else:
                                print(f"\n🔎 Resultados encontrados ({len(clientes)}):")
                                for c in clientes:
                                    estado = "ACTIVO" if c.activo else "INACTIVO"
                                    print(f"\nID: {c.id_cliente} ({estado})")
                                    print(f"Nombre/Razón Social: {c.nombre}")
                                    print(f"Tipo: {c.tipo_cliente}")
                                    print(f"Teléfono: {c.telefono or 'No especificado'}")
                                    print(f"Correo: {c.correo or 'No especificado'}")
                                    print(f"RFC: {c.rfc}")
                                    print(f"Dirección: {c.direccion or 'No especificado'}")
                                    print(f"Comentarios: {c.comentarios or 'Ninguno'}")
                                    print("-" * 40)
                    
                    except ValueError:
                        print("\n❌ El ID debe ser un número válido")
                    except Exception as e:
                        print(f"\n❌ Error inesperado: {str(e)}")
                    
                    input("\nPresione ENTER para continuar...")
                    limpiar_pantalla()
                    break

            elif entrada_cliente.opcionSub == "5":
                while True:
                    print("\n=== Listado Completo de Clientes ===")
                    controller = ClienteController(connection_string)  # Instancia local del controlador

                    try:
                        # Validar entrada del usuario
                        
                        opcion = input("¿Mostrar clientes inactivos? (s/n) o 0 para cancelar: ").lower()

                        if not opcion in ['s', 'n', '0']:
                            print("⚠️ Opción no válida. Ingrese 's', 'n' o '0'.")
                            input("\nPresione ENTER para continuar...")
                            limpiar_pantalla()
                            continue

                        if opcion == '0':
                            print("\n🚫 Operación cancelada por el usuario.")
                            input("\nPresione ENTER para continuar...")
                            limpiar_pantalla()
                            break  # Salir del ciclo while

                        mostrar_inactivos = opcion == 's'

                        # Obtener clientes según filtro
                        clientes = controller.obtener_todos_clientes(activos_only=not mostrar_inactivos)

                        if not clientes:
                            estado = "activos" if not mostrar_inactivos else "registrados"
                            print(f"\nℹ️ No hay clientes {estado} en el sistema")
                        else:
                            estado = "ACTIVOS" if not mostrar_inactivos else "TODOS (activos e inactivos)"
                            print(f"\n📋 Listado de clientes ({estado}) - Total: {len(clientes)}")
                            print("=" * 60)

                            for c in clientes:
                                estado = "ACTIVO" if c.activo else "INACTIVO"
                                print(f"\nID: {c.id_cliente} ({estado})")
                                print(f"Nombre/Razón Social: {c.nombre}")
                                print(f"Tipo: {c.tipo_cliente}")
                                print(f"Teléfono: {c.telefono or 'No especificado'}")
                                print(f"Correo: {c.correo or 'No especificado'}")
                                print(f"RFC: {c.rfc}")
                                print(f"Dirección: {c.direccion or 'No especificado'}")
                                print(f"Fecha Registro: {c.fecha_registro.strftime('%d/%m/%Y') if c.fecha_registro else 'No registrada'}")
                                print(f"Comentarios: {c.comentarios or 'Ninguno'}")
                                print("-" * 60)

                    except Exception as e:
                        print(f"\n❌ Error al obtener clientes: {str(e)}")

                    input("\nPresione ENTER para continuar...")
                    limpiar_pantalla()
                    break

            
            elif entrada_cliente.opcionSub == "6":   
                # input("\nPresione ENTER para continuar...")
                limpiar_pantalla()
                break


    # elif entrada.opcion == "2":
    #     while True:  # Bucle principal de cotizaciones
    #         print("Has seleccionado Cotizaciones.")
    #         menu_cotizaciones()
    #         entrada_cotizacion = pedir_opcion_submenu()
    #         limpiar_pantalla()
    #         if entrada_cotizacion.opcionSub == "1":
    #             print("Has seleccionado agregar una cotizacion.")
    #             controller_cotizacion = CotizacionController(connection_string)

    #             # Parte 1: Información del Cliente
    #             cliente_seleccionado = None
    #             while True:
    #                 print("\n=== Información del Cliente ===")
    #                 controller = ClienteController(connection_string)
    #                 id_cliente_input = input("Ingrese el ID del cliente ('0' para buscar): ").strip()

    #                 if id_cliente_input == '0':
    #                     print("\nOperación cancelada por el usuario")
    #                     input("\nPresione ENTER para continuar...")
    #                     limpiar_pantalla()
    #                     break
    #                 elif id_cliente_input.isdigit():
    #                     cliente_seleccionado = controller.obtener_cliente(int(id_cliente_input))
    #                     if cliente_seleccionado:
    #                         print(f"Cliente encontrado: {cliente_seleccionado.nombre}")
    #                         break  # Sale del bucle de selección de cliente
    #                     else:
    #                         print(f"El cliente con ID {id_cliente_input} no existe.")
    #                         opcion_cliente = input("¿Desea ir a la opción de cliente para agregarlo? (s/n): ").lower()
    #                         if opcion_cliente == 's':
    #                             print("Redirigiendo a la opción de cliente...")
    #                             limpiar_pantalla()
    #                             break  # Sale para redirigir (volverá al menú principal y el usuario elegirá '1')
    #                         else:
    #                             input("\nPresione ENTER para continuar...")
    #                             limpiar_pantalla()
    #                             break  # Vuelve a pedir ID
    #                 else:
    #                     print("Por favor, ingrese un ID de cliente válido o '0' para buscar.")
    #                     input("\nPresione ENTER para continuar...")
    #                     limpiar_pantalla()
    #                     continue  # Vuelve a pedir ID

    #             if not cliente_seleccionado:
    #                 continue  # Vuelve al menú de cotizaciones

    #             # Parte 2: Datos de Cotización
    #             print("\n=== Datos del Cliente para la Cotización ===")
    #             print(f"Nombre: {cliente_seleccionado.nombre}")
    #             print(f"Correo: {cliente_seleccionado.correo or 'No especificado'}")
    #             print(f"Teléfono: {cliente_seleccionado.telefono or 'No especificado'}")
    #             print(f"Tipo de Cliente: {cliente_seleccionado.tipo_cliente}")
    #             print(f"RFC: {cliente_seleccionado.rfc or 'No especificado'}")

    #             fecha_creacion = datetime.today()
    #             fecha_creacion_str = fecha_creacion.strftime('%Y-%m-%d')
    #             print(f"Fecha de Creación: {fecha_creacion_str}")

    #             fecha_activacion_str = input("Ingrese la fecha de activación (YYYY-MM-DD): ").strip()
    #             observaciones = input("Ingrese las observaciones de la cotización: ").strip()
    #             usuario_creador = input("Ingrese el usuario creador: ").strip()

    #             cotizacion_data = {
    #                 "id_cliente": cliente_seleccionado.id_cliente,
    #                 "fecha_creacion": fecha_creacion,
    #                 "fecha_activacion": datetime.strptime(fecha_activacion_str, '%Y-%m-%d') if fecha_activacion_str else None,
    #                 "fecha_finalizacion": None,
    #                 "fecha_cancelacion": None,
    #                 "observaciones": observaciones,
    #                 "usuario_creador": usuario_creador,
    #                 "nombre_cliente": cliente_seleccionado.nombre,
    #                 "correo_cliente": cliente_seleccionado.correo or "",
    #                 "telefono_cliente": cliente_seleccionado.telefono,
    #                 "tipo_cliente": cliente_seleccionado.tipo_cliente,
    #                 "rfc_cliente": cliente_seleccionado.rfc or "",
    #                 "activo": True
    #             }

    #             # Parte 3: Servicios
    #             servicios_seleccionados = []
    #             while True:
    #                 print("\n=== Información del Servicio ===")
    #                 nombre_servicio = input("Ingrese el nombre del servicio (o '0' para terminar): ").strip()

    #                 if nombre_servicio == '0':
    #                     if not servicios_seleccionados:
    #                         confirmar = input("No ha agregado servicios. ¿Desea cancelar? (s/n): ").lower()
    #                         if confirmar == 's':
    #                             print("\nOperación cancelada por el usuario")
    #                             input("\nPresione ENTER para continuar...")
    #                             limpiar_pantalla()
    #                             break  # Sale del bucle de servicios y vuelve al menú principal de cotizaciones
    #                         else:
    #                             continue  # Vuelve a pedir servicio
    #                     else:
    #                         break  # Sale del bucle de recolección de servicios

    #                 descripcion_servicio = input("Ingrese la descripción del servicio (opcional): ").strip() or None
    #                 tipo_servicio = input("Ingrese el tipo de servicio (opcional): ").strip() or None

    #                 try:
    #                     costo_servicio = float(input("Ingrese el costo del servicio: ").strip())
    #                     cantidad_servicio_input = input("Ingrese la cantidad del servicio (opcional): ").strip()
    #                     cantidad_servicio = float(cantidad_servicio_input) if cantidad_servicio_input else None

    #                     servicios_seleccionados.append({
    #                         "nombre_servicio": nombre_servicio,
    #                         "descripcion_servicio": descripcion_servicio,
    #                         "tipo_servicio": tipo_servicio,
    #                         "costo_servicio": costo_servicio,
    #                         "cantidad_servicio": cantidad_servicio,
    #                         "fecha_creacion_servicio": datetime.today(),
    #                         "usuario_creador_servicio": usuario_creador,
    #                         "activo": True,
    #                         "fecha_actualizacion_servicio": None
    #                     })
    #                     print(f"✅ Servicio '{nombre_servicio}' agregado a la lista.")

    #                 except ValueError:
    #                     print("❌ Error: Ingrese valores numéricos válidos")
    #                     continue  # Vuelve a pedir datos del servicio

    #             # Si salimos del bucle sin servicios, volvemos al menú principal de cotizaciones
    #             if not servicios_seleccionados:
    #                 continue

    #             # --- Opción para Agregar Materiales ---
    #             materiales_seleccionados = []
    #             while True:
    #                 agregar_material = input("\n¿Desea agregar materiales a esta cotización? (si/no): ")
    #                 if agregar_material.lower() == 'si':
    #                     print("\n--- Materiales Disponibles ---")
    #                     material_controller = MaterialController(connection_string)
    #                     cotizacion_material_controller = CotizacionMaterialController(connection_string)
    #                     materiales_disponibles = material_controller.obtener_todos_materiales()
    #                     if materiales_disponibles:
    #                         for material in materiales_disponibles:
    #                             # print(f"ID: {material['id_material']}, Nombre: {material['nombre']}, Descripción: {material['descripcion']}")
    #                             print(f"ID: {material.id_material}, Nombre: {material.nombre}, Descripción: {material.descripcion}")
    #                         try:
    #                             id_material_seleccionado = int(input("Ingrese el ID del material que desea agregar (o 0 para volver): "))
    #                             if id_material_seleccionado == 0:
    #                                 break

    #                             # Lógica para obtener o solicitar el id_proveedor_material
    #                             id_proveedor_material_seleccionado = input("Ingrese el ID del Proveedor-Material (opcional, deje vacío si no aplica): ")
    #                             id_proveedor_material = int(id_proveedor_material_seleccionado) if id_proveedor_material_seleccionado else None

    #                             cantidad_material = Decimal(input("Ingrese la cantidad del material: "))

    #                             material_info = next((m for m in materiales_disponibles if m.id_material == id_material_seleccionado), None)
   
    #                             if material_info:
    #                                 materiales_seleccionados.append({
    #                                     "id_material": id_material_seleccionado,
    #                                     "nombre_material": material_info.nombre,  # Corrección aquí
    #                                     "cantidad": cantidad_material,
    #                                     "id_proveedor_material": id_proveedor_material  # Agrega esta línea
    #                                 })
    #                                 print(f"✅ Material '{material_info.nombre}' agregado a la lista.")
    #                             else:
    #                                 print("❌ El ID del material ingresado no es válido.")

    #                         except ValueError:
    #                             print("❌ ID de material o cantidad inválido.")
    #                     else:
    #                         print("No hay materiales disponibles en este momento.")

    #                 elif agregar_material.lower() == 'no':
    #                     break
    #                 else:
    #                     print("Por favor, ingrese 'si' o 'no'.")

    #             # Mostrar resumen de servicios y materiales antes de guardar
    #             print("\n" + "="*40)
    #             print("📋 RESUMEN DE LA COTIZACIÓN A CREAR")
    #             print("="*40)
    #             print("=== Servicios ===")
    #             total_servicios = 0
    #             if servicios_seleccionados:
    #                 for i, servicio in enumerate(servicios_seleccionados, 1):
    #                     subtotal = servicio["costo_servicio"] * (servicio["cantidad_servicio"] or 1)
    #                     total_servicios += subtotal
    #                     print(f"🔹 {i}. {servicio['nombre_servicio']} - {servicio['cantidad_servicio'] or 1} x ${servicio['costo_servicio']:.2f} = ${subtotal:.2f}")
    #                 print(f"\nTotal de Servicios: ${total_servicios:.2f}")
    #             else:
    #                 print("No se agregaron servicios.")

    #             print("\n=== Materiales ===")
    #             if materiales_seleccionados:
    #                 for i, material in enumerate(materiales_seleccionados, 1):
    #                     print(f"🔸 {i}. {material['nombre_material']} - Cantidad: {material['cantidad']}")
    #                 print(f"\nTotal de Materiales: (El costo se calculará al guardar)") # Nota importante
    #             else:
    #                 print("No se agregaron materiales.")

    #             print("="*40)

    #             # Confirmación final
    #             while True:
    #                 confirmar = input("\n¿Confirmar creación de cotización con estos servicios y materiales? (s/n): ").lower().strip()
    #                 if confirmar in ['s', 'n']:
    #                     break
    #                 print("❌ Por favor ingrese 's' para confirmar o 'n' para cancelar")


    #             if confirmar == 's':
    #                 # Guardar cotización
    #                 # try:
    #                 nueva_cotizacion = controller_cotizacion.crear_cotizacion(cotizacion_data)
    #                 print(f"\n✅ Cotización creada con ID: {nueva_cotizacion.id_cotizacion}")

    #                 repository_cotizacion_servicio = CotizacionServicioRepository(connection_string)
    #                 for servicio_data in servicios_seleccionados:
    #                     nueva_cotizacion_servicio = CotizacionServicio(
    #                         id_cotizacion=nueva_cotizacion.id_cotizacion,
    #                         id_servicio=0,
    #                         nombre_servicio=servicio_data["nombre_servicio"],
    #                         descripcion_servicio=servicio_data["descripcion_servicio"],
    #                         tipo_servicio=servicio_data["tipo_servicio"],
    #                         costo_servicio=servicio_data["costo_servicio"],
    #                         cantidad_servicio=servicio_data["cantidad_servicio"],
    #                         fecha_creacion_servicio=servicio_data["fecha_creacion_servicio"],
    #                         activo=servicio_data["activo"],
    #                         usuario_creador_servicio=servicio_data["usuario_creador_servicio"],
    #                         fecha_actualizacion_servicio=servicio_data["fecha_actualizacion_servicio"]
    #                     )
    #                     repository_cotizacion_servicio.create_cotizacion_servicio(nueva_cotizacion_servicio)
    #                     print(f"✅ Servicio '{servicio_data['nombre_servicio']}' agregado a la cotización.")

    #                 # Guardar materiales en Cotizacion_Material
    #                 cotizacion_material_controller = CotizacionMaterialController(connection_string)
    #                 for material in materiales_seleccionados:
    #                     cotizacion_material_controller.agregar_material_a_cotizacion(
    #                         id_cotizacion=nueva_cotizacion.id_cotizacion,
    #                         id_proveedor_material=material['id_proveedor_material'],
    #                         cantidad=material['cantidad']
    #                     )
    #                     print(f"✅ Material '{material['nombre_material']}' agregado a la cotización.")

    #                 # except Exception as e:
    #                 #     print(f"\n❌ Error al guardar la cotización: {str(e)}")
    #                 #     input("\nPresione Enter para continuar...")
    #                 #     limpiar_pantalla()
    #                 #     continue  # Vuelve al menú principal de cotizaciones

    #             else:
    #                 print("❌ Operación cancelada")
    #                 input("\nPresione Enter para continuar...")
    #                 limpiar_pantalla()
    #                 continue  # Vuelve al menú principal de cotizaciones

    #             input("\nPresione Enter para continuar...")
    #             limpiar_pantalla()
    #             break  # Vuelve al menú principal de cotizaciones
                    



    elif entrada.opcion == "2":
        while True:  # Bucle principal de cotizaciones
            print("Has seleccionado Cotizaciones.")
            menu_cotizaciones()
            entrada_cotizacion = pedir_opcion_submenu_coti()
            limpiar_pantalla()
            if entrada_cotizacion.opcionSub == "1":
                print("Has seleccionado agregar una cotizacion.")
                controller_cotizacion = CotizacionController(connection_string)

                # Parte 1: Información del Cliente
                cliente_seleccionado = None
                while True:
                    print("\n=== Información del Cliente ===")
                    controller = ClienteController(connection_string)
                    id_cliente_input = input("Ingrese el ID del cliente ('0' para buscar): ").strip()

                    if id_cliente_input == '0':
                        print("\nOperación cancelada por el usuario")
                        input("\nPresione ENTER para continuar...")
                        limpiar_pantalla()
                        break
                    elif id_cliente_input.isdigit():
                        cliente_seleccionado = controller.obtener_cliente(int(id_cliente_input))
                        if cliente_seleccionado:
                            print(f"Cliente encontrado: {cliente_seleccionado.nombre}")
                            break  # Sale del bucle de selección de cliente
                        else:
                            print(f"El cliente con ID {id_cliente_input} no existe.")
                            opcion_cliente = input("¿Desea ir a la opción de cliente para agregarlo? (s/n): ").lower()
                            if opcion_cliente == 's':
                                print("Redirigiendo a la opción de cliente...")
                                limpiar_pantalla()
                                break  # Sale para redirigir (volverá al menú principal y el usuario elegirá '1')
                            else:
                                input("\nPresione ENTER para continuar...")
                                limpiar_pantalla()
                                break  # Vuelve a pedir ID
                    else:
                        print("Por favor, ingrese un ID de cliente válido o '0' para buscar.")
                        input("\nPresione ENTER para continuar...")
                        limpiar_pantalla()
                        continue  # Vuelve a pedir ID

                if not cliente_seleccionado:
                    continue  # Vuelve al menú de cotizaciones

                # Parte 2: Datos de Cotización
                print("\n=== Datos del Cliente para la Cotización ===")
                print(f"Nombre: {cliente_seleccionado.nombre}")
                print(f"Correo: {cliente_seleccionado.correo or 'No especificado'}")
                print(f"Teléfono: {cliente_seleccionado.telefono or 'No especificado'}")
                print(f"Tipo de Cliente: {cliente_seleccionado.tipo_cliente}")
                print(f"RFC: {cliente_seleccionado.rfc or 'No especificado'}")

                fecha_creacion = datetime.today()
                fecha_creacion_str = fecha_creacion.strftime('%Y-%m-%d')
                print(f"Fecha de Creación: {fecha_creacion_str}")

                fecha_activacion_str = input("Ingrese la fecha de activación (YYYY-MM-DD): ").strip()
                observaciones = input("Ingrese las observaciones de la cotización: ").strip()
                usuario_creador = input("Ingrese el usuario creador: ").strip()

                cotizacion_data = {
                    "id_cliente": cliente_seleccionado.id_cliente,
                    "fecha_creacion": fecha_creacion,
                    "fecha_activacion": datetime.strptime(fecha_activacion_str, '%Y-%m-%d') if fecha_activacion_str else None,
                    "fecha_finalizacion": None,
                    "fecha_cancelacion": None,
                    "observaciones": observaciones,
                    "usuario_creador": usuario_creador,
                    "nombre_cliente": cliente_seleccionado.nombre,
                    "correo_cliente": cliente_seleccionado.correo or "",
                    "telefono_cliente": cliente_seleccionado.telefono,
                    "tipo_cliente": cliente_seleccionado.tipo_cliente,
                    "rfc_cliente": cliente_seleccionado.rfc or "",
                    "activo": True
                }

                # Parte 3: Servicios
                servicios_seleccionados = []
                while True:
                    print("\n=== Información del Servicio ===")
                    nombre_servicio = input("Ingrese el nombre del servicio (o '0' para terminar): ").strip()

                    if nombre_servicio == '0':
                        if not servicios_seleccionados:
                            confirmar = input("No ha agregado servicios. ¿Desea cancelar? (s/n): ").lower()
                            if confirmar == 's':
                                print("\nOperación cancelada por el usuario")
                                input("\nPresione ENTER para continuar...")
                                limpiar_pantalla()
                                break  # Sale del bucle de servicios y vuelve al menú principal de cotizaciones
                            else:
                                continue  # Vuelve a pedir servicio
                        else:
                            break  # Sale del bucle de recolección de servicios

                    descripcion_servicio = input("Ingrese la descripción del servicio (opcional): ").strip() or None
                    tipo_servicio = input("Ingrese el tipo de servicio (opcional): ").strip() or None

                    try:
                        costo_servicio = float(input("Ingrese el costo del servicio: ").strip())
                        cantidad_servicio_input = input("Ingrese la cantidad del servicio (opcional): ").strip()
                        cantidad_servicio = float(cantidad_servicio_input) if cantidad_servicio_input else None

                        servicios_seleccionados.append({
                            "nombre_servicio": nombre_servicio,
                            "descripcion_servicio": descripcion_servicio,
                            "tipo_servicio": tipo_servicio,
                            "costo_servicio": costo_servicio,
                            "cantidad_servicio": cantidad_servicio,
                            "fecha_creacion_servicio": datetime.today(),
                            "usuario_creador_servicio": usuario_creador,
                            "activo": True,
                            "fecha_actualizacion_servicio": None
                        })
                        print(f"✅ Servicio '{nombre_servicio}' agregado a la lista.")

                    except ValueError:
                        print("❌ Error: Ingrese valores numéricos válidos")
                        continue  # Vuelve a pedir datos del servicio

                # Si salimos del bucle sin servicios, volvemos al menú principal de cotizaciones
                if not servicios_seleccionados:
                    continue

                # --- Opción para Agregar Materiales ---
                materiales_seleccionados = []
                while True:
                    agregar_material = input("\n¿Desea agregar materiales a esta cotización? (si/no): ")
                    if agregar_material.lower() == 'si':
                        print("\n--- Materiales Disponibles ---")
                        material_controller = MaterialController(connection_string)
                        cotizacion_material_controller = CotizacionMaterialController(connection_string)
                        materiales_disponibles = material_controller.obtener_todos_materiales()
                        if materiales_disponibles:
                            for material in materiales_disponibles:
                                print(f"ID: {material.id_material}, Nombre: {material.nombre}, Descripción: {material.descripcion}")
                            try:
                                id_material_seleccionado = int(input("Ingrese el ID del material que desea agregar (o 0 para volver): "))
                                if id_material_seleccionado == 0:
                                    break

                                id_proveedor_material_seleccionado = input("Ingrese el ID del Proveedor-Material (opcional, deje vacío si no aplica): ")
                                id_proveedor_material = int(id_proveedor_material_seleccionado) if id_proveedor_material_seleccionado else None

                                cantidad_material = Decimal(input("Ingrese la cantidad del material: "))

                                material_info = next((m for m in materiales_disponibles if m.id_material == id_material_seleccionado), None)
   
                                if material_info:
                                    materiales_seleccionados.append({
                                        "id_material": id_material_seleccionado,
                                        "nombre_material": material_info.nombre,
                                        "cantidad": cantidad_material,
                                        "id_proveedor_material": id_proveedor_material
                                    })
                                    # print(f"✅ Material '{material_info.nombre}' agregado a la lista.")
                                else:
                                    print("❌ El ID del material ingresado no es válido.")

                            except ValueError:
                                print("❌ ID de material o cantidad inválido.")
                        else:
                            print("No hay materiales disponibles en este momento.")

                    elif agregar_material.lower() == 'no':
                        break
                    else:
                        print("Por favor, ingrese 'si' o 'no'.")

                # ==============================================
                # NUEVA SECCIÓN DE RESUMEN MEJORADA (REEMPLAZO)
                # ==============================================
                print("\n" + "="*60)
                print("📋 RESUMEN PROFESIONAL DE COTIZACIÓN".center(60))
                print("="*60)

                # Datos del Cliente
                print("\n👤 DATOS DEL CLIENTE")
                print(f"  • Nombre: {cliente_seleccionado.nombre}")
                print(f"  • Tipo: {cliente_seleccionado.tipo_cliente}")
                print(f"  • RFC: {cliente_seleccionado.rfc or 'No especificado'}")
                print(f"  • Teléfono: {cliente_seleccionado.telefono or 'No especificado'}")
                print(f"  • Correo: {cliente_seleccionado.correo or 'No especificado'}")

                # Datos de la Cotización
                print("\n📅 DATOS DE LA COTIZACIÓN")
                print(f"  • Fecha creación: {fecha_creacion_str}")
                print(f"  • Fecha activación: {fecha_activacion_str}")
                print(f"  • Observaciones: {observaciones}")
                print(f"  • Creador: {usuario_creador}")

                # Servicios (Mano de Obra)
                print("\n🔧 SERVICIOS (MANO DE OBRA)")
                total_servicios = 0
                if servicios_seleccionados:
                    print("-"*60)
                    print("| {:<3} | {:<20} | {:<10} | {:>10} | {:>8} |".format(
                        "#", "Nombre", "Tipo", "Costo Unit.", "Subtotal"))
                    print("-"*60)
                    
                    for i, servicio in enumerate(servicios_seleccionados, 1):
                        cantidad = servicio["cantidad_servicio"] or 1
                        subtotal = servicio["costo_servicio"] * cantidad
                        total_servicios += subtotal
                        print("| {:<3} | {:<20} | {:<10} | {:>10.2f} | {:>8.2f} |".format(
                            i,
                            servicio["nombre_servicio"][:20],
                            (servicio["tipo_servicio"] or "-")[:10],
                            servicio["costo_servicio"],
                            subtotal
                        ))
                    
                    print("-"*60)
                    print(f"💰 TOTAL SERVICIOS: ${total_servicios:.2f}".rjust(59))
                else:
                    print("  No se agregaron servicios")


                # print("\n📦 MATERIALES")
                # total_materiales = 0
                # if materiales_seleccionados:
                #     print("-"*65)
                #     print("| {:<3} | {:<20} | {:>8} | {:>12} | {:>10} |".format(
                #         "#", "Nombre Material", "Cantidad", "Costo Unit.", "Subtotal"))
                #     print("-"*65)

                #     for i, material in enumerate(materiales_seleccionados, 1):
                #         cantidad = material["cantidad"]
                        
                #         # Simulación de costo unitario (si no tienes costo aún, usa un costo fijo o 0.0 provisional)
                #         costo_unitario = 50.00  # ❗ Aquí deberías obtener el costo real del material
                #         subtotal = float(cantidad) * costo_unitario
                #         total_materiales += subtotal

                #         print("| {:<3} | {:<20} | {:>8} | {:>12.2f} | {:>10.2f} |".format(
                #             i,
                #             material["nombre_material"][:20],
                #             str(cantidad),
                #             costo_unitario,
                #             subtotal
                #         ))
                #     print("-"*65)
                #     print(f"💰 TOTAL MATERIALES: ${total_materiales:.2f}".rjust(64))
                # else:
                #     print("  No se agregaron materiales")

                print("\n📦 MATERIALES")
                total_materiales = 0
                proveedor_material_repository = ProveedorMaterialRepository(connection_string)
                if materiales_seleccionados:
                    print("-" * 65)
                    print("| {:<3} | {:<20} | {:>8} | {:>12} | {:>10} |".format(
                        "#", "Nombre Material", "Cantidad", "Precio", "Subtotal"))
                    print("-" * 65)

                    for i, material in enumerate(materiales_seleccionados, 1):
                        cantidad = material["cantidad"]

                        # 🔥 Obtiene el precio real desde Proveedor_Material
                        # vinculo = ProveedorMaterialRepository.obtener_vinculo(material["id_proveedor_material"])
                        vinculo = proveedor_material_repository.obtener_vinculo(material["id_proveedor_material"])

                        if vinculo:
                            precio = float(vinculo.precio)
                        else:
                            precio = 0.0  # O podrías poner un mensaje de error si quieres

                        subtotal = float(cantidad) * precio
                        total_materiales += subtotal

                        print("| {:<3} | {:<20} | {:>8} | {:>12.2f} | {:>10.2f} |".format(
                            i,
                            material["nombre_material"][:20],
                            str(cantidad),
                            precio,
                            subtotal
                        ))

                    print("-" * 65)
                    print(f"💰 TOTAL MATERIALES: ${total_materiales:.2f}".rjust(64))
                else:
                    print("  No se agregaron materiales")


                iva_servicios = total_servicios * 0.16
                total_servicios_con_iva = total_servicios + iva_servicios

                # Resumen Final
                print("\n" + "="*60)
                print("🧮 RESUMEN FINAL".center(60))
                print("-"*60)
                print(f"  Total Servicios (sin IVA): ${total_servicios:.2f}".rjust(59))
                print(f"  IVA 16% Servicios: ${iva_servicios:.2f}".rjust(59))
                print(f"  Total Servicios (con IVA): ${total_servicios_con_iva:.2f}".rjust(59))
                print(f"  Total Materiales: ${total_materiales:.2f}".rjust(59))
                print("-"*60)
                gran_total = total_servicios_con_iva + total_materiales
                print(f"  GRAN TOTAL: ${gran_total:.2f}".rjust(59))
                print("="*60)


                # # Confirmación final mejorada
                # while True:
                #     """Muestra un menú de confirmación estilizado."""
                #     print("\n╔══════════════════════════════════════╗")
                #     print("║        Opciones de Cotización         ║")
                #     print("╠══════════════════════════════════════╣")
                #     print("║ [1] Guardar Cotización             ║")
                #     print("║ [2] Editar Cotización              ║")
                #     print("║ [3] Cancelar Operación               ║")
                #     print("╚══════════════════════════════════════╝")
                #     confirmar = input("\nSeleccione una opción (1-3): ").strip()
                #     if confirmar in ['1', '2', '3']:
                #         break
                #     print("❌ Opción inválida. Por favor ingrese 1, 2 o 3")

                # if confirmar == '1':
                #     # Guardar cotización
                #     nueva_cotizacion = controller_cotizacion.crear_cotizacion(cotizacion_data)
                #     print(f"\n✅ Cotización creada con ID: {nueva_cotizacion.id_cotizacion}")
                    
                #     # Guardar servicios
                #     repository_cotizacion_servicio = CotizacionServicioRepository(connection_string)
                #     for servicio_data in servicios_seleccionados:
                #         nueva_cotizacion_servicio = CotizacionServicio(
                #             id_cotizacion=nueva_cotizacion.id_cotizacion,
                #             id_servicio=0,
                #             nombre_servicio=servicio_data["nombre_servicio"],
                #             descripcion_servicio=servicio_data["descripcion_servicio"],
                #             tipo_servicio=servicio_data["tipo_servicio"],
                #             costo_servicio=servicio_data["costo_servicio"],
                #             cantidad_servicio=servicio_data["cantidad_servicio"],
                #             fecha_creacion_servicio=servicio_data["fecha_creacion_servicio"],
                #             activo=servicio_data["activo"],
                #             usuario_creador_servicio=servicio_data["usuario_creador_servicio"],
                #             fecha_actualizacion_servicio=servicio_data["fecha_actualizacion_servicio"]
                #         )
                #         repository_cotizacion_servicio.create_cotizacion_servicio(nueva_cotizacion_servicio)
                #         print(f"✅ Servicio '{servicio_data['nombre_servicio']}' agregado a la cotización.")
                    
                #     # Guardar materiales
                #     cotizacion_material_controller = CotizacionMaterialController(connection_string)
                #     for material in materiales_seleccionados:
                #         cotizacion_material_controller.agregar_material_a_cotizacion(
                #             id_cotizacion=nueva_cotizacion.id_cotizacion,
                #             id_proveedor_material=material['id_proveedor_material'],
                #             cantidad=material['cantidad']
                #         )
                #         print(f"✅ Material '{material['nombre_material']}' agregado a la cotización.")
                    
                #     print("✅ Todos los elementos se guardaron correctamente")
                    
                # elif confirmar == '2':
                #     print("\n✏️ Redirigiendo a edición...")
                #     continue  # Vuelve al inicio del bucle
                    
                # elif confirmar == '3':
                #     print("\n❌ Operación cancelada por el usuario")
                #     input("\nPresione Enter para continuar...")
                #     limpiar_pantalla()
                #     continue  # Vuelve al menú principal de cotizaciones

                # input("\nPresione Enter para continuar...")
                # limpiar_pantalla()
                # break  # Vuelve al menú principal de cotizaciones
                # Confirmación final mejorada
                while True:
                    """Muestra un menú de confirmación estilizado."""
                    print("\n╔══════════════════════════════════════╗")
                    print("║        Opciones de Cotización         ║")
                    print("╠══════════════════════════════════════╣")
                    print("║ [1] Guardar Cotización                ║")
                    print("║ [2] Editar Cotización                 ║")
                    print("║ [3] Cancelar Operación                ║")
                    print("╚══════════════════════════════════════╝")
                    confirmar = input("\nSeleccione una opción (1-3): ").strip()
                    if confirmar in ['1', '2', '3']:
                        break
                    print("❌ Opción inválida. Por favor ingrese 1, 2 o 3")

                if confirmar == '1':
                    # Guardar cotización
                    nueva_cotizacion = controller_cotizacion.crear_cotizacion(cotizacion_data)
                    print(f"\n✅ Cotización creada con ID: {nueva_cotizacion.id_cotizacion}")
                    
                    # Guardar servicios
                    repository_cotizacion_servicio = CotizacionServicioRepository(connection_string)
                    for servicio_data in servicios_seleccionados:
                        nueva_cotizacion_servicio = CotizacionServicio(
                            id_cotizacion=nueva_cotizacion.id_cotizacion,
                            id_servicio=0,
                            nombre_servicio=servicio_data["nombre_servicio"],
                            descripcion_servicio=servicio_data["descripcion_servicio"],
                            tipo_servicio=servicio_data["tipo_servicio"],
                            costo_servicio=servicio_data["costo_servicio"],
                            cantidad_servicio=servicio_data["cantidad_servicio"],
                            fecha_creacion_servicio=servicio_data["fecha_creacion_servicio"],
                            activo=servicio_data["activo"],
                            usuario_creador_servicio=servicio_data["usuario_creador_servicio"],
                            fecha_actualizacion_servicio=servicio_data["fecha_actualizacion_servicio"]
                        )
                        repository_cotizacion_servicio.create_cotizacion_servicio(nueva_cotizacion_servicio)
                        print(f"✅ Servicio '{servicio_data['nombre_servicio']}' agregado a la cotización.")
                    
                    # Guardar materiales
                    cotizacion_material_controller = CotizacionMaterialController(connection_string)
                    for material in materiales_seleccionados:
                        cotizacion_material_controller.agregar_material_a_cotizacion(
                            id_cotizacion=nueva_cotizacion.id_cotizacion,
                            id_proveedor_material=material['id_proveedor_material'],
                            cantidad=material['cantidad']
                        )
                        print(f"✅ Material '{material['nombre_material']}' agregado a la cotización.")
                    
                    print("✅ Todos los elementos se guardaron correctamente")
                    
                    # Preguntar si desea generar PDF
                    generar_pdf = input("\n¿Desea generar un PDF de esta cotización? (s/n): ").lower()
                    if generar_pdf == 's':
                        try:
                            # Obtener los materiales con precios desde la base de datos
                            cotizacion_material_repo = CotizacionMaterialRepository(connection_string)
                            materiales_bd = cotizacion_material_repo.obtener_materiales_por_cotizacion(nueva_cotizacion.id_cotizacion)
                            
                            # Obtener los servicios desde la base de datos
                            cotizacion_servicio_repo = CotizacionServicioRepository(connection_string)
                            servicios_bd = cotizacion_servicio_repo.get_servicios_por_cotizacion(nueva_cotizacion.id_cotizacion)
                            
                            # Generar el PDF
                            ruta_pdf = generar_pdf_cotizacion(
                                cotizacion=nueva_cotizacion,
                                cliente=cliente_seleccionado,
                                servicios=servicios_bd,
                                materiales=materiales_bd
                            )
                            
                            print(f"\n✅ PDF generado correctamente: {ruta_pdf}")
                            
                            # Opcionalmente, abrir el PDF automáticamente
                            abrir_pdf = input("¿Desea abrir el PDF ahora? (s/n): ").lower()
                            if abrir_pdf == 's':
                                import os
                                import platform
                                
                                if platform.system() == 'Windows':
                                    os.startfile(ruta_pdf)
                                elif platform.system() == 'Darwin':  # macOS
                                    os.system(f'open "{ruta_pdf}"')
                                else:  # Linux
                                    os.system(f'xdg-open "{ruta_pdf}"')
                                    
                        except Exception as e:
                            print(f"❌ Error al generar el PDF: {str(e)}")
                    
                elif confirmar == '2':
                    print("\n✏️ Redirigiendo a edición...")
                    continue  # Vuelve al inicio del bucle
                    
                elif confirmar == '3':
                    print("\n❌ Operación cancelada por el usuario")
                    input("\nPresione Enter para continuar...")
                    limpiar_pantalla()
                    continue  # Vuelve al menú principal de cotizaciones

                input("\nPresione Enter para continuar...")
                limpiar_pantalla()
                break  # Vuelve al menú principal de cotizaciones
            elif entrada_cotizacion.opcionSub == "2":
                print("Has seleccionado editar una cotizacion.")
                print("\n=== COTIZACIONES REGISTRADAS ===")
                
                controller_cotizacion = CotizacionController(connection_string)
                cotizaciones = controller_cotizacion.obtener_todas_cotizaciones()
                
                if not cotizaciones:
                    print("No hay cotizaciones registradas.")
                    input("\nPresione Enter para continuar...")
                    limpiar_pantalla()
                    continue
                
                # Mostrar lista de cotizaciones
                print("\n" + "-"*80)
                print("| {:<5} | {:<20} | {:<12} | {:<15} | {:<15} |".format(
                    "ID", "Cliente", "Fecha", "Usuario", "Estado"))
                print("-"*80)
                
                for cotizacion in cotizaciones:
                    estado = "Activa"
                    if cotizacion.fecha_cancelacion:
                        estado = "Cancelada"
                    elif cotizacion.fecha_finalizacion:
                        estado = "Finalizada"
                    
                    print("| {:<5} | {:<20} | {:<12} | {:<15} | {:<15} |".format(
                        cotizacion.id_cotizacion,
                        cotizacion.nombre_cliente[:20],
                        cotizacion.fecha_creacion.strftime('%Y-%m-%d'),
                        cotizacion.usuario_creador[:15],
                        estado
                    ))
                
                print("-"*80)
                
                # Opción para ver detalles de una cotización
                while True:
                    id_seleccionado = input("\nIngrese el ID de la cotización para ver detalles (o '0' para volver): ")
                    
                    if id_seleccionado == "0":
                        break
                        
                    try:
                        id_cotizacion = int(id_seleccionado)
                        
                        # Obtener la cotización
                        cotizacion = controller_cotizacion.obtener_cotizacion(id_cotizacion)
                        if not cotizacion:
                            print("❌ Cotización no encontrada.")
                            continue
                        
                        # Obtener servicios
                        cotizacion_servicio_repo = CotizacionServicioRepository(connection_string)
                        servicios = cotizacion_servicio_repo.get_servicios_por_cotizacion(id_cotizacion)
                        
                        # Obtener materiales
                        cotizacion_material_repo = CotizacionMaterialRepository(connection_string)
                        materiales = cotizacion_material_repo.obtener_materiales_por_cotizacion(id_cotizacion)
                        
                        # Mostrar detalles de la cotización con formato similar al de creación
                        limpiar_pantalla()
                        print("\n" + "="*60)
                        print("📋 RESUMEN PROFESIONAL DE COTIZACIÓN".center(60))
                        print("="*60)
                        
                        # Datos del Cliente
                        print("\n👤 DATOS DEL CLIENTE")
                        print(f"  • Nombre: {cotizacion.nombre_cliente}")
                        print(f"  • Tipo: {cotizacion.tipo_cliente}")
                        print(f"  • RFC: {cotizacion.rfc_cliente or 'No especificado'}")
                        print(f"  • Teléfono: {cotizacion.telefono_cliente or 'No especificado'}")
                        print(f"  • Correo: {cotizacion.correo_cliente or 'No especificado'}")
                        
                        # Datos de la Cotización
                        print("\n📅 DATOS DE LA COTIZACIÓN")
                        print(f"  • Fecha creación: {cotizacion.fecha_creacion.strftime('%Y-%m-%d')}")
                        fecha_activacion = cotizacion.fecha_activacion.strftime('%Y-%m-%d') if cotizacion.fecha_activacion else "No especificada"
                        print(f"  • Fecha activación: {fecha_activacion}")
                        print(f"  • Observaciones: {cotizacion.observaciones}")
                        print(f"  • Creador: {cotizacion.usuario_creador}")
                        
                        # Servicios (Mano de Obra)
                        print("\n🔧 SERVICIOS (MANO DE OBRA)")
                        total_servicios = 0
                        if servicios:
                            print("-"*60)
                            print("| {:<3} | {:<20} | {:<10} | {:>10} | {:>8} |".format(
                                "#", "Nombre", "Tipo", "Costo Unit.", "Subtotal"))
                            print("-"*60)
                            
                            for i, servicio in enumerate(servicios, 1):
                                cantidad = servicio.cantidad_servicio or 1
                                subtotal = servicio.costo_servicio * cantidad
                                total_servicios += subtotal
                                
                                print("| {:<3} | {:<20} | {:<10} | {:>10.2f} | {:>8.2f} |".format(
                                    i,
                                    servicio.nombre_servicio[:20],
                                    (servicio.tipo_servicio or "-")[:10],
                                    servicio.costo_servicio,
                                    subtotal
                                ))
                            
                            print("-"*60)
                            print(f"💰 TOTAL SERVICIOS: ${total_servicios:.2f}".rjust(59))
                        else:
                            print("  No hay servicios registrados para esta cotización")
                        
                        # # Materiales
                        # print("\n📦 MATERIALES")
                        # total_materiales = 0
                        # if materiales:
                        #     print("-" * 65)
                        #     print("| {:<3} | {:<20} | {:<8} | {:>12} | {:>10} |".format(
                        #         "#", "Nombre Material", "Cantidad", "Precio", "Subtotal"))
                        #     print("-" * 65)
                            
                        #     for i, material in enumerate(materiales, 1):
                        #         cantidad = float(material["cantidad"]) if material["cantidad"] else 0
                        #         precio = float(material["precio_unitario"]) if material["precio_unitario"] else 0
                                
                        #         subtotal = cantidad * precio
                        #         total_materiales += subtotal
                                
                        #         print("| {:<3} | {:<20} | {:<8} | {:>12.2f} | {:>10.2f} |".format(
                        #             i,
                        #             material["nombre_material"][:20],
                        #             cantidad,
                        #             precio,
                        #             subtotal
                        #         ))
                            
                        #     print("-" * 65)
                        #     print(f"💰 TOTAL MATERIALES: ${total_materiales:.2f}".rjust(64))
                        # else:
                        #     print("  No hay materiales registrados para esta cotización")
                        # # Materiales
                        # print("\n📦 MATERIALES")
                        # total_materiales = 0
                        # if materiales and len(materiales) > 0:
                        #     print("-" * 65)
                        #     print("| {:<3} | {:<20} | {:<8} | {:>12} | {:>10} |".format(
                        #         "#", "Nombre Material", "Cantidad", "Precio", "Subtotal"))
                        #     print("-" * 65)
                            
                        #     for i, material in enumerate(materiales, 1):
                        #         try:
                        #             # Imprimir el material para depuración
                        #             print(f"Procesando material: {material}")
                                    
                        #             # Extraer valores con manejo de errores
                        #             cantidad = 0
                        #             if "cantidad" in material and material["cantidad"] is not None:
                        #                 cantidad = float(material["cantidad"])
                                    
                        #             precio = 0
                        #             if "precio_unitario" in material and material["precio_unitario"] is not None:
                        #                 precio = float(material["precio_unitario"])
                                    
                        #             nombre_material = "Desconocido"
                        #             if "nombre_material" in material and material["nombre_material"] is not None:
                        #                 nombre_material = material["nombre_material"]
                                    
                        #             subtotal = cantidad * precio
                        #             total_materiales += subtotal
                                    
                        #             print("| {:<3} | {:<20} | {:<8} | {:>12.2f} | {:>10.2f} |".format(
                        #                 i,
                        #                 nombre_material[:20],
                        #                 cantidad,
                        #                 precio,
                        #                 subtotal
                        #             ))
                        #         except Exception as e:
                        #             print(f"Error al procesar material {i}: {str(e)}")
                            
                        #     print("-" * 65)
                        #     print(f"💰 TOTAL MATERIALES: ${total_materiales:.2f}".rjust(64))
                        # else:
                        #     print("  No hay materiales registrados para esta cotización")
                        #     print(f"  Valor de materiales: {materiales}")
                        # Materiales
                        print("\n📦 MATERIALES")
                        total_materiales = 0
                        if materiales and len(materiales) > 0:
                            print("-" * 75)
                            print("| {:<3} | {:<25} | {:<12} | {:>12} | {:>12} |".format(
                                "#", "Nombre Material", "Cantidad", "Precio", "Subtotal"))
                            print("-" * 75)
                            
                            for i, material in enumerate(materiales, 1):
                                try:
                                    # Extraer valores con manejo de errores
                                    cantidad = 0
                                    if "cantidad" in material and material["cantidad"] is not None:
                                        cantidad = float(material["cantidad"])
                                    
                                    precio = 0
                                    if "precio_unitario" in material and material["precio_unitario"] is not None:
                                        precio = float(material["precio_unitario"])
                                    
                                    nombre_material = "Desconocido"
                                    if "nombre_material" in material and material["nombre_material"] is not None:
                                        nombre_material = material["nombre_material"]
                                    
                                    unidad_medida = ""
                                    if "unidad_medida" in material and material["unidad_medida"] is not None:
                                        unidad_medida = material["unidad_medida"]
                                    
                                    nombre_proveedor = ""
                                    if "nombre_proveedor" in material and material["nombre_proveedor"] is not None:
                                        nombre_proveedor = f" ({material['nombre_proveedor']})"
                                    
                                    subtotal = cantidad * precio
                                    total_materiales += subtotal
                                    
                                    print("| {:<3} | {:<25} | {:<12} | {:>12.2f} | {:>12.2f} |".format(
                                        i,
                                        nombre_material[:25],
                                        f"{cantidad} {unidad_medida}",
                                        precio,
                                        subtotal
                                    ))
                                except Exception as e:
                                    print(f"Error al procesar material {i}: {str(e)}")
                            
                            print("-" * 75)
                            print(f"💰 TOTAL MATERIALES: ${total_materiales:.2f}".rjust(74))
                        else:
                            print("  No hay materiales registrados para esta cotización")
                        
                        # Cálculos finales
                        iva_servicios = total_servicios * 0.16
                        total_servicios_con_iva = total_servicios + iva_servicios
                        
                        # Resumen Final
                        print("\n" + "="*60)
                        print("🧮 RESUMEN FINAL".center(60))
                        print("-"*60)
                        print(f"  Total Servicios (sin IVA): ${total_servicios:.2f}".rjust(59))
                        print(f"  IVA 16% Servicios: ${iva_servicios:.2f}".rjust(59))
                        print(f"  Total Servicios (con IVA): ${total_servicios_con_iva:.2f}".rjust(59))
                        print(f"  Total Materiales: ${total_materiales:.2f}".rjust(59))
                        print("-"*60)
                        gran_total = total_servicios_con_iva + total_materiales
                        print(f"  GRAN TOTAL: ${gran_total:.2f}".rjust(59))
                        print("="*60)
                        
                        # Opciones adicionales
                        print("\n[1] Volver a la lista de cotizaciones")
                        print("[2] Generar PDF (No implementado)")
                        print("[3] Enviar por correo (No implementado)")
                        
                        opcion = input("\nSeleccione una opción: ")
                        if opcion == "1":
                            limpiar_pantalla()
                            break
                        else:
                            print("Funcionalidad no implementada.")
                            input("\nPresione Enter para continuar...")
                            limpiar_pantalla()
                            break
                            
                    except ValueError:
                        print("❌ Por favor ingrese un ID válido.")
                    except Exception as e:
                        print(f"❌ Error: {str(e)}")
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        break
                
                limpiar_pantalla()




            elif entrada_cotizacion.opcionSub == "3":
                print("Has seleccionado eliminar una cotizacion.")
                print("\n=== DAR DE BAJA COTIZACIÓN ===")
                
                controller_cotizacion = CotizacionController(connection_string)
                cotizaciones = controller_cotizacion.obtener_todas_cotizaciones(activas_only=True)
                
                if not cotizaciones:
                    print("No hay cotizaciones activas registradas.")
                    input("\nPresione Enter para continuar...")
                    limpiar_pantalla()
                    continue
                
                # Mostrar lista de cotizaciones activas
                print("\n" + "-"*80)
                print("| {:<5} | {:<20} | {:<12} | {:<15} | {:<15} |".format(
                    "ID", "Cliente", "Fecha", "Usuario", "Estado"))
                print("-"*80)
                
                for cotizacion in cotizaciones:
                    print("| {:<5} | {:<20} | {:<12} | {:<15} | {:<15} |".format(
                        cotizacion.id_cotizacion,
                        cotizacion.nombre_cliente[:20],
                        cotizacion.fecha_creacion.strftime('%Y-%m-%d'),
                        cotizacion.usuario_creador[:15],
                        "Activa"
                    ))
                
                print("-"*80)
                
                # Solicitar ID de la cotización a dar de baja
                while True:
                    id_seleccionado = input("\nIngrese el ID de la cotización a dar de baja (o '0' para volver): ")
                    
                    if id_seleccionado == "0":
                        break
                        
                    try:
                        id_cotizacion = int(id_seleccionado)
                        
                        # Verificar que la cotización existe y está activa
                        cotizacion = controller_cotizacion.obtener_cotizacion(id_cotizacion)
                        if not cotizacion:
                            print("❌ Cotización no encontrada.")
                            continue
                            
                        if not cotizacion.activo:
                            print("❌ La cotización ya está inactiva.")
                            continue
                        
                        # Confirmar la baja
                        print(f"\nCotización seleccionada: #{cotizacion.id_cotizacion} - {cotizacion.nombre_cliente}")
                        confirmacion = input("¿Está seguro que desea dar de baja esta cotización? (s/n): ").lower()
                        
                        if confirmacion == 's':
                            # Solicitar motivo de cancelación
                            motivo = input("Ingrese el motivo de la cancelación (opcional): ")
                            
                            # Si se proporcionó un motivo, actualizar las observaciones
                            if motivo:
                                observaciones_actuales = cotizacion.observaciones or ""
                                cotizacion.observaciones = f"{observaciones_actuales}\nMotivo de cancelación: {motivo}"
                                controller_cotizacion.repository.update_cotizacion(id_cotizacion, cotizacion)
                            
                            # Marcar como inactiva
                            if controller_cotizacion.marcar_cotizacion_como_inactiva(id_cotizacion):
                                print("✅ Cotización dada de baja correctamente.")
                                input("\nPresione Enter para continuar...")
                                break
                        else:
                            print("Operación cancelada.")
                            
                    except ValueError:
                        print("❌ Por favor ingrese un ID válido.")
                    except Exception as e:
                        print(f"❌ Error: {str(e)}")
                        input("\nPresione Enter para continuar...")
                        break
                
                limpiar_pantalla()
            elif entrada_cotizacion.opcionSub == "4":
                print("Has seleccionado Buscar Cotizacion.")
                break
            elif entrada_cotizacion.opcionSub == "5":
                print("Has seleccionado Listar Cotizaciones.")
                break
            elif entrada_cotizacion.opcionSub == "6":
                print("Has seleccionado Volver al menú principal.")
                break


#-----------------------------------------------------------------------------------------------------------------------------------------
    elif entrada.opcion == "3":
        while True:

            menu_proveedores()
            opcion_proveedor = pedir_opcion_submenu()
            limpiar_pantalla()

            if opcion_proveedor.opcionSub == "1":
                while True:
                    print("\n=== Agregar Proveedor ===")
                    print("Todos los campos son obligatorios\n")
                    print("Ingrese '0' en el nombre para cancelar y volver al menú anterior\n")
                    controller = ProveedorController(connection_string)
                    
                    datos_proveedor = {}
                    errores = []
                    
                    def validar_campo(valor, campo, tipo="texto", longitud=None):
                        valor = valor.strip()
                        
                        # Validación general para todos los campos
                        if not valor:
                            errores.append(f"- El campo {campo} es obligatorio")
                            return False
                            
                        # Validación para evitar solo números en campos de texto
                        if tipo == "texto":
                            if valor.isdigit():
                                errores.append(f"- El campo {campo} no puede contener solo números")
                                return False
                                
                        # Validación para evitar solo espacios
                        if valor.isspace():
                            errores.append(f"- El campo {campo} no puede contener solo espacios")
                            return False
                            
                        # Validaciones específicas por tipo
                        if tipo == "telefono":
                            if not valor.isdigit():
                                errores.append(f"- El teléfono solo debe contener números")
                                return False
                            if len(valor) != 10:
                                errores.append(f"- El teléfono debe tener exactamente 10 dígitos")
                                return False
                                
                        elif tipo == "email":
                            if "@" not in valor or "." not in valor.split("@")[-1]:
                                errores.append(f"- Formato de email inválido (debe contener @ y dominio válido)")
                                return False
                                
                        elif tipo == "rfc":
                            if len(valor) != 13:
                                errores.append(f"- El RFC debe tener exactamente 13 caracteres")
                                return False
                                
                        elif tipo == "direccion":
                            if valor.replace(" ", "").isdigit():
                                errores.append(f"- La dirección no puede contener solo números")
                                return False
                                
                        return True
                    
                    # Recoger datos con validaciones
                    datos_proveedor["nombre"] = input("Nombre del proveedor: ").upper()
                    if datos_proveedor["nombre"].strip() == "0":
                        print("\nOperación cancelada por el usuario")
                        input("\nPresione ENTER para continuar...")
                        limpiar_pantalla()
                        break
                        
                    datos_proveedor["contacto"] = input("Persona de contacto: ").upper()
                    datos_proveedor["telefono"] = input("Teléfono (10 dígitos): ")
                    datos_proveedor["correo"] = input("Correo electrónico: ")
                    datos_proveedor["rfc"] = input("RFC (13 caracteres): ").upper()
                    datos_proveedor["direccion"] = input("Dirección: ")
                    
                    # Validar campos con reglas específicas
                    validar_campo(datos_proveedor["nombre"], "nombre del proveedor", "texto")
                    validar_campo(datos_proveedor["contacto"], "persona de contacto", "texto")
                    validar_campo(datos_proveedor["telefono"], "teléfono", "telefono")
                    validar_campo(datos_proveedor["correo"], "correo electrónico", "email")
                    validar_campo(datos_proveedor["rfc"], "RFC", "rfc")
                    validar_campo(datos_proveedor["direccion"], "dirección", "direccion")
                    
                    # try:
                    if errores:
                        print("\n❌ Errores encontrados:")
                        print("\n".join(errores))
                        input("\nPresione Enter para corregir los datos...")
                        limpiar_pantalla()
                        continue

                    # Mostrar resumen
                    print("\n" + "="*40)
                    print("📋 RESUMEN DEL PROVEEDOR A REGISTRAR")
                    print("="*40)
                    print(f"🔹 Nombre/Razón Social: {datos_proveedor['nombre']}")
                    print(f"🔹 Persona de Contacto: {datos_proveedor['contacto']}")
                    print(f"🔹 Teléfono: {datos_proveedor['telefono']}")
                    print(f"🔹 Email: {datos_proveedor['correo']}")
                    print(f"🔹 RFC: {datos_proveedor['rfc']}")
                    print(f"🔹 Dirección: {datos_proveedor['direccion']}")
                    print("="*40)
                    
                    # Validación de confirmación
                    while True:
                        confirmar = input("\n¿Confirmar creación de proveedor? (s/n): ").lower().strip()
                        if confirmar not in ['s', 'n']:
                            print("❌ Por favor ingrese 's' para confirmar o 'n' para cancelar")
                            continue
                        break
                        
                    if confirmar != 's':
                        print("❌ Operación cancelada")
                        limpiar_pantalla()
                        break
                    
                    # Crear proveedor
                    proveedor_creado = controller.crear_proveedor({
                        'nombre': datos_proveedor["nombre"],
                        'contacto': datos_proveedor["contacto"],
                        'telefono': datos_proveedor["telefono"],
                        'correo': datos_proveedor["correo"].lower(),
                        'rfc': datos_proveedor["rfc"],
                        'direccion': datos_proveedor["direccion"]
                    })
                    
                    if proveedor_creado:
                        print(f"\n✅ Proveedor creado exitosamente con ID: {proveedor_creado.id_proveedor}")
                        input("\nPresione Enter para continuar...")
                        limpiar_pantalla()
                        break
                    else:
                        print("\n❌ Error al crear el proveedor")
                            
                    # except Exception as e:
                    #     print(f"\n❌ Error inesperado: {str(e)}")
                    #     input("\nPresione Enter para continuar...")

        
                    

            elif opcion_proveedor.opcionSub == "2":
                print("\n=== Editar Proveedor ===")
                controller = ProveedorController(connection_string)  # Instancia local del controlador
                
                try:
                    # Obtener lista de proveedores activos
                    proveedores = controller.obtener_todos_proveedores(activos_only=True)
                    
                    if not proveedores:
                        print("\n❌ No hay proveedores activos registrados")
                    else:
                        print("\nProveedores disponibles (ACTIVOS):")
                        for p in proveedores:
                            print(f"ID: {p.id_proveedor} - {p.nombre}")
                        
                        # Validación del ID
                        try:
                            id_editar = int(input("\nIngrese el ID del proveedor a editar (0 para cancelar): "))
                            if id_editar == 0:
                                print("Operación cancelada")
                                input("\nPresione ENTER para continuar...")
                                limpiar_pantalla()

                            else:
                                proveedor = controller.obtener_proveedor(id_editar)
                                
                                if not proveedor:
                                    print("\n❌ No existe un proveedor con ese ID o está inactivo")
                                else:
                                    print("\nDatos actuales del proveedor:")
                                    print(f"1. Nombre: {proveedor.nombre}")
                                    print(f"2. Contacto: {proveedor.contacto}")
                                    print(f"3. Teléfono: {proveedor.telefono}")
                                    print(f"4. Correo: {proveedor.correo}")
                                    print(f"5. RFC: {proveedor.rfc}")
                                    print(f"6. Dirección: {proveedor.direccion}")
                                    
                                    # Diccionario para almacenar cambios
                                    updates = {}
                                    errores = []
                                    
                                    # Función de validación
                                    def validar_campo(valor, campo, tipo="texto", longitud=None):
                                        valor = valor.strip()
                                        if valor:  # Solo validar si hay valor (campos opcionales)
                                            if tipo == "telefono":
                                                if not valor.isdigit():
                                                    errores.append(f"El teléfono debe contener solo números")
                                                    return False
                                                if len(valor) != 10:
                                                    errores.append(f"El teléfono debe tener 10 dígitos")
                                                    return False
                                            elif tipo == "email":
                                                if "@" not in valor or "." not in valor:
                                                    errores.append(f"Formato de email inválido")
                                                    return False
                                            elif tipo == "rfc" and len(valor) != 13:
                                                errores.append(f"El RFC debe tener 13 caracteres")
                                                return False
                                        return True
                                    
                                    # Recoger nuevos valores
                                    nuevos_datos = {
                                        "nombre": input("\nNuevo nombre (ENTER para mantener actual): ").strip().upper(),
                                        "contacto": input("Nuevo contacto (ENTER para mantener actual): ").strip().upper(),
                                        "telefono": input("Nuevo teléfono (10 dígitos, ENTER para mantener actual): ").strip(),
                                        "correo": input("Nuevo correo (ENTER para mantener actual): ").strip().upper(),
                                        "rfc": input("Nuevo RFC (13 caracteres, ENTER para mantener actual): ").strip().upper(),
                                        "direccion": input("Nueva dirección (ENTER para mantener actual): ").strip().upper()
                                    }
                                    
                                    # Validar campos modificados
                                    if nuevos_datos["telefono"]:
                                        validar_campo(nuevos_datos["telefono"], "teléfono", "telefono")
                                    if nuevos_datos["correo"]:
                                        validar_campo(nuevos_datos["correo"], "correo", "email")
                                    if nuevos_datos["rfc"]:
                                        validar_campo(nuevos_datos["rfc"], "RFC", "rfc")
                                    
                                    if errores:
                                        print("\n❌ Errores encontrados:")
                                        for error in errores:
                                            print(f"- {error}")
                                    else:
                                        # Preparar datos para actualizar (solo campos modificados)
                                        updates = {k: v for k, v in nuevos_datos.items() if v}
                                        
                                        if updates:
                                            confirmar = input("\n¿Confirmar cambios? (s/n): ").lower()
                                            if confirmar == 's':
                                                resultado = controller.actualizar_proveedor(id_editar, updates)
                                                if resultado:
                                                    print("\n✅ Proveedor actualizado exitosamente")
                                                else:
                                                    print("\n❌ Error al actualizar el proveedor")
                                            else:
                                                print("Cambios cancelados")
                                        else:
                                            print("\n⚠️ No se realizaron cambios")
                        
                        except ValueError:
                            print("\n❌ Error: Debe ingresar un ID numérico válido")
                
                except Exception as e:
                    print(f"\n❌ Error inesperado: {str(e)}")
                
                # input("\nPresione ENTER para continuar...")
                limpiar_pantalla()



            elif opcion_proveedor.opcionSub == "3":
                while True:
                    print("\n=== Eliminar Proveedor (Marcar como Inactivo) ===")
                    controller = ProveedorController(connection_string)  # Instancia local del controlador
                    
                    try:
                        # Obtener solo proveedores activos
                        proveedores = controller.obtener_todos_proveedores(activos_only=True)
                        
                        if not proveedores:
                            print("\nℹ️ No hay proveedores activos registrados")
                        else:
                            print("\nProveedores ACTIVOS disponibles:")
                            for p in proveedores:
                                print(f"ID: {p.id_proveedor} - {p.nombre}")
                            
                            # Validación del ID
                            try:
                                id_eliminar = input("\nIngrese el ID del proveedor a eliminar (0 para cancelar): ").strip()
                                
                                if id_eliminar == "0":
                                    print("Operación cancelada")
                                    input("\nPresione ENTER para continuar...")
                                    limpiar_pantalla()
                                    break
                                else:
                                    id_eliminar = int(id_eliminar)  # Conversión a entero
                                    proveedor = controller.obtener_proveedor(id_eliminar)
                                    
                                    if not proveedor or not proveedor.activo:
                                        print("\n❌ No existe un proveedor activo con ese ID")
                                    else:
                                        # Confirmación con detalles
                                        print("\n⚠️ ATENCIÓN: Esta acción marcará al proveedor como INACTIVO")
                                        print(f"ID: {proveedor.id_proveedor}")
                                        print(f"Nombre: {proveedor.nombre}")
                                        print(f"RFC: {proveedor.rfc}")
                                        
                                        confirmar = input("\n¿ESTÁ SEGURO que desea continuar? (s/n): ").lower()
                                        if confirmar == 's':
                                            if controller.eliminar_proveedor(id_eliminar):
                                                print("\n✅ Proveedor marcado como inactivo correctamente")
                                                # Mostrar datos del proveedor eliminado
                                                proveedor_eliminado = controller.obtener_proveedor(id_eliminar)
                                                print(f"\nDetalles del proveedor inactivado:")
                                                print(f"Estado actual: {'ACTIVO' if proveedor_eliminado.activo else 'INACTIVO'}")
                                            else:
                                                print("\n❌ Error al marcar el proveedor como inactivo")
                                        else:
                                            print("Operación cancelada por el usuario")
                            
                            except ValueError:
                                print("\n❌ Error: Debe ingresar un número válido")
                            except Exception as e:
                                print(f"\n❌ Error al procesar el ID: {str(e)}")
                    
                    except Exception as e:
                        print(f"\n❌ Error inesperado: {str(e)}")
                    
                    input("\nPresione ENTER para continuar...")
                    limpiar_pantalla()
                


            elif opcion_proveedor.opcionSub == "4":
                while True:
                    print("\n=== Buscar Proveedor ===")
                    print("Ingrese '0' para cancelar y volver al menú anterior\n")
                    controller = ProveedorController(connection_string)
                    
                    try:
                        criterio = input("Ingrese ID, nombre o RFC del proveedor: ").strip()
                        
                        # Opción para cancelar
                        if criterio == "0":
                            print("\nOperación cancelada por el usuario")
                            limpiar_pantalla()
                            break
                            
                        if not criterio:
                            print("\n❌ Debe ingresar un criterio de búsqueda")
                            input("\nPresione ENTER para continuar...")
                            limpiar_pantalla()
                            continue
                            
                        proveedores = []
                        
                        # Búsqueda por ID si es numérico
                        if criterio.isdigit():
                            proveedor = controller.obtener_proveedor(int(criterio))
                            if proveedor:
                                proveedores = [proveedor]
                        else:
                            # Búsqueda por nombre o RFC
                            todos_proveedores = controller.obtener_todos_proveedores(activos_only=False)
                            criterio_lower = criterio.lower()
                            proveedores = [
                                p for p in todos_proveedores
                                if (criterio_lower in p.nombre.lower() or
                                    (p.rfc and criterio_lower in p.rfc.lower()))
                            ]
                        
                        if not proveedores:
                            print("\n🔍 No se encontraron proveedores con ese criterio")
                        else:
                            print(f"\n🔎 Resultados encontrados ({len(proveedores)}):")
                            for p in proveedores:
                                estado = "ACTIVO" if p.activo else "INACTIVO"
                                print(f"\nID: {p.id_proveedor} ({estado})")
                                print(f"Nombre: {p.nombre}")
                                print(f"Contacto: {p.contacto}")
                                print(f"Teléfono: {p.telefono}")
                                print(f"Correo: {p.correo}")
                                print(f"RFC: {p.rfc}")
                                print(f"Dirección: {p.direccion}")
                                print("-" * 30)
                        
                        input("\nPresione ENTER para continuar...")
                        limpiar_pantalla()
                        break
                        
                    except ValueError:
                        print("\n❌ El ID debe ser un número válido")
                        input("\nPresione ENTER para continuar...")
                        limpiar_pantalla()
                    except Exception as e:
                        print(f"\n❌ Error inesperado: {str(e)}")
                        input("\nPresione ENTER para continuar...")
                        limpiar_pantalla()



            elif opcion_proveedor.opcionSub == "5":
                while True:
                    print("\n=== Listado Completo de Proveedores ===")
                    controller = ProveedorController(connection_string)  # Instancia local del controlador

                    try:
                        # Validar entrada del usuario
                        opcion = input("¿Mostrar proveedores inactivos? (s/n) o 0 para cancelar: ").lower()

                        if opcion not in ['s', 'n', '0']:
                            print("⚠️ Opción no válida. Ingrese 's', 'n' o '0'.")
                            input("\nPresione ENTER para continuar...")
                            limpiar_pantalla()
                            continue

                        if opcion == '0':
                            print("\n🚫 Operación cancelada por el usuario.")
                            input("\nPresione ENTER para continuar...")
                            limpiar_pantalla()
                            break  # Salir del ciclo while

                        mostrar_inactivos = opcion == 's'

                        # Obtener proveedores según filtro
                        proveedores = controller.obtener_todos_proveedores(activos_only=not mostrar_inactivos)

                        if not proveedores:
                            estado = "activos" if not mostrar_inactivos else "registrados"
                            print(f"\nℹ️ No hay proveedores {estado} en el sistema")
                        else:
                            estado = "ACTIVOS" if not mostrar_inactivos else "TODOS (activos e inactivos)"
                            print(f"\n📋 Listado de proveedores ({estado}) - Total: {len(proveedores)}")
                            print("=" * 60)

                            for p in proveedores:
                                estado = "ACTIVO" if p.activo else "INACTIVO"
                                print(f"\nID: {p.id_proveedor} ({estado})")
                                print(f"Nombre: {p.nombre}")
                                print(f"Contacto: {p.contacto or 'No especificado'}")
                                print(f"Teléfono: {p.telefono or 'No especificado'}")
                                print(f"Correo: {p.correo or 'No especificado'}")
                                print(f"RFC: {p.rfc or 'No especificado'}")
                                print(f"Dirección: {p.direccion or 'No especificada'}")
                                print("-" * 60)

                    except Exception as e:
                        print(f"\n❌ Error al obtener proveedores: {str(e)}")

                    input("\nPresione ENTER para continuar...")
                    limpiar_pantalla()
                    break

            elif opcion_proveedor.opcionSub == "6":  
                limpiar_pantalla()
                break






#
# 
# 
# 
# #-------------------------------------------------------------------------------------------------------------------------------------


    elif entrada.opcion == "4":  # Asumiendo que 4 es el número para el menú de materiales
        while True:
            menu_materiales()  # Necesitarás crear esta función similar a menu_proveedores()
            opcion_material = pedir_opcion_submenu()
            limpiar_pantalla()
            if opcion_material.opcionSub == "1":  # Agregar material
                while True:
                    print("\n=== AGREGAR MATERIAL ===")
                    print("Los campos marcados con (*) son obligatorios")
                    print("Ingrese '0' en el nombre para cancelar\n")

                    controller = MaterialController(connection_string)
                    datos_material = {}
                    errores = []

                    def validar_campo(valor, campo, tipo="texto", obligatorio=True):
                        valor = valor.strip() if valor else ""
                        if obligatorio:
                            if not valor:
                                errores.append(f"- El campo {campo} es obligatorio")
                                return None
                            if valor.isspace():
                                errores.append(f"- El campo {campo} no puede contener solo espacios en blanco")
                                return None
                        if tipo == "decimal":
                            try:
                                valor = float(valor.replace(',', '.'))
                                if valor <= 0:
                                    errores.append(f"- El {campo} debe ser mayor que cero")
                                    return None
                                return valor
                            except:
                                errores.append(f"- El {campo} debe ser un número válido")
                                return None
                        return valor

                    # Recoger y validar datos
                    datos_material["nombre"] = input("Nombre del material (*): ").strip().upper()
                    if datos_material["nombre"] == "0":
                        print("\nOperación cancelada por el usuario")
                        break

                    datos_material["descripcion"] = input("Descripción [Opcional]: ").strip().upper()
                    datos_material["unidad_medida"] = validar_campo(
                        input("Unidad de medida (*) (ej. kg, l, m, pz): ").upper(),
                        "unidad de medida"
                    )
                    datos_material["marca"] = validar_campo(
                        input("Marca (*): ").upper(),
                        "marca"
                    )
                    datos_material["categoria"] = validar_campo(
                        input("Categoría (*): ").upper(),
                        "categoría"
                    )

                    if errores:
                        print("\n❌ Errores encontrados:")
                        print("\n".join(errores))
                        input("\nPresione Enter para corregir...")
                        limpiar_pantalla()
                        continue

                    # Mostrar resumen
                    print("\n" + "="*40)
                    print("📋 RESUMEN DEL MATERIAL")
                    print("="*40)
                    print(f"🔹 Nombre: {datos_material['nombre']}")
                    print(f"🔹 Descripción: {datos_material['descripcion'] or 'Ninguna'}")
                    print(f"🔹 Unidad: {datos_material['unidad_medida']}")
                    print(f"🔹 Marca: {datos_material['marca']}")
                    print(f"🔹 Categoría: {datos_material['categoria']}")
                    print("="*40)

                    if input("\n¿Confirmar creación? (s/n): ").lower() != 's':
                        print("❌ Operación cancelada")
                        break

                    # Crear material
                    # try:
                    material_creado = controller.crear_material({
                        'nombre': datos_material['nombre'],
                        'descripcion': datos_material['descripcion'],
                        'unidad_medida': datos_material['unidad_medida'],
                        'marca': datos_material['marca'],
                        'categoria': datos_material['categoria'],
                        'fecha_registro': datetime.now()
                    })

                    if not material_creado:
                        print("\n❌ Error al crear el material")
                        continue

                    print(f"\n✅ Material creado exitosamente (ID: {material_creado.id_material})")

                    # Sección de vinculación con proveedor
                    # if input("\n¿Vincular con proveedor ahora? (s/n): ").lower() != 's':
                    #     break

                    controller_proveedor = ProveedorController(connection_string)
                    controller_proveedor_material = ProveedorMaterialController(connection_string)

                    proveedores = controller_proveedor.obtener_todos_proveedores()
                    if not proveedores:
                        print("\nℹ️ No hay proveedores registrados")
                        input("\nPresione Enter para continuar...")
                        break

                    while True:
                        limpiar_pantalla()
                        print("\n=== VINCULAR MATERIAL ===")
                        print(f"Material: {material_creado.nombre} (ID: {material_creado.id_material})")
                        print("\nProveedores disponibles:")
                        for p in proveedores:
                            print(f"ID: {p.id_proveedor} - {p.nombre}")
                        print("\nIngrese '0' para cancelar")

                        try:
                            id_proveedor = int(input("\nID del proveedor a vincular: "))
                            if id_proveedor == 0:
                                break

                            proveedor = controller_proveedor.obtener_proveedor(id_proveedor)
                            if not proveedor:
                                print("\n❌ Proveedor no encontrado")
                                input("\nPresione Enter para continuar...")
                                continue

                            precio = validar_campo(
                                input("Precio ofrecido (*): $").strip(),
                                "precio",
                                "decimal"
                            )
                            if precio is None:
                                input("\nPresione Enter para continuar...")
                                continue

                            # # Confirmar vinculación
                            # print(f"\nℹ️ Se vinculará a: {proveedor.nombre} por ${precio:.2f}")
                            # if input("¿Confirmar? (s/n): ").lower() != 's':
                            #     continue

                            if controller_proveedor_material.vincular_material(
                                id_proveedor,
                                material_creado.id_material,
                                precio
                            ):
                                print(f"\n✅ Vinculado exitosamente a {material_creado.nombre} con {proveedor.nombre} con precio de ${precio:.2f} ")
                                input("\nPresione Enter para continuar...")
                                limpiar_pantalla()
                                break
                            else:
                                print("\n❌ Error al vincular")
                                input("\nPresione Enter para continuar...")

                        except ValueError:
                            print("\n❌ Ingrese un ID numérico válido")
                            input("\nPresione Enter para continuar...")
                    break

                    # except Exception as e:
                    #     print(f"\n❌ Error inesperado: {str(e)}")
                    #     input("\nPresione Enter para continuar...")
           


            elif opcion_material.opcionSub == "2":
                while True:
                    print("\n=== Editar Material ===")
                    controller = MaterialController(connection_string)
                    
                    try:
                        materiales = controller.obtener_todos_materiales(activos_only=True)
                        
                        if not materiales:
                            print("\n❌ No hay materiales activos registrados")
                        else:
                            print("\nMateriales disponibles (ACTIVOS):")
                            for m in materiales:
                                print(f"ID: {m.id_material} - {m.nombre} ({m.unidad_medida})")
                            
                            try:
                                # Validación estricta para el 0 de cancelación
                                id_input = input("\nIngrese el ID del material a editar (0 para cancelar): ").strip()
                                if id_input == "0":  # Solo acepta "0" exacto
                                    print("Operación cancelada")
                                    limpiar_pantalla()
                                    break
                                
                                id_editar = int(id_input)
                                material = controller.obtener_material(id_editar)
                                
                                if not material:
                                    print("\n❌ No existe un material con ese ID o está inactivo")
                                else:
                                    print("\nDatos actuales del material:")
                                    print(f"1. Nombre: {material.nombre}")
                                    print(f"2. Descripción: {material.descripcion or 'Ninguna'}")
                                    print(f"3. Unidad de medida: {material.unidad_medida}")
                                    print(f"4. Marca: {material.marca or 'No especificada'}")
                                    print(f"5. Categoría: {material.categoria or 'No especificada'}")
                                    
                                    errores = []
                                    
                                    def validar_edicion(valor, campo, tipo="texto", max_caracteres=None):
                                        valor = valor.strip()
                                        
                                        # Validación general para todos los campos
                                        if not valor:
                                            return True  # Campo vacío (no se actualiza)
                                            
                                        if valor.isspace():
                                            errores.append(f"- El campo {campo} no puede contener solo espacios")
                                            return False
                                            
                                        if tipo == "texto":
                                            if valor.isdigit():
                                                errores.append(f"- El campo {campo} no puede ser solo números")
                                                return False
                                                
                                        elif tipo == "unidad":
                                            if len(valor) > 10:
                                                errores.append(f"- La unidad no puede exceder 10 caracteres")
                                                return False
                                            if valor.isdigit():
                                                errores.append(f"- La unidad no puede ser solo números")
                                                return False
                                        
                                        if max_caracteres and len(valor) > max_caracteres:
                                            errores.append(f"- El {campo} no puede exceder {max_caracteres} caracteres")
                                            return False
                                            
                                        return True
                                    
                                    # Obtener nuevos datos con strip() automático
                                    nuevos_datos = {
                                        "nombre": input("\nNuevo nombre (solo letras, ENTER para mantener): ").strip().upper(),
                                        "descripcion": input("Nueva descripción (ENTER para mantener): ").strip().upper(),
                                        "unidad_medida": input("Nueva unidad (ej. kg, pz, ENTER para mantener): ").strip().lower(),
                                        "marca": input("Nueva marca (ENTER para mantener): ").strip().upper(),
                                        "categoria": input("Nueva categoría (ENTER para mantener): ").strip().upper()
                                    }
                                    
                                    # Validar cada campo que tenga contenido
                                    if nuevos_datos["nombre"]:
                                        validar_edicion(nuevos_datos["nombre"], "nombre", "texto", 100)
                                    if nuevos_datos["descripcion"]:
                                        validar_edicion(nuevos_datos["descripcion"], "descripción", "texto", 500)
                                    if nuevos_datos["unidad_medida"]:
                                        validar_edicion(nuevos_datos["unidad_medida"], "unidad de medida", "unidad")
                                    if nuevos_datos["marca"]:
                                        validar_edicion(nuevos_datos["marca"], "marca", "texto", 50)
                                    if nuevos_datos["categoria"]:
                                        validar_edicion(nuevos_datos["categoria"], "categoría", "texto", 50)
                                    
                                    if errores:
                                        print("\n❌ Errores encontrados:")
                                        print("\n".join(errores))
                                        input("\nPresione Enter para corregir...")
                                        limpiar_pantalla()
                                    else:
                                        # Preparar actualización solo para campos modificados
                                        updates = {}
                                        for campo, valor in nuevos_datos.items():
                                            if valor:  # Solo actualizar campos con contenido
                                                updates[campo] = valor
                                        
                                        if updates:
                                            print("\n=== Resumen de cambios ===")
                                            for campo, valor in updates.items():
                                                old_val = getattr(material, campo)
                                                print(f"{campo}: {old_val} → {valor}")
                                            
                                            confirmar = input("\n¿Confirmar cambios? (s/n): ").lower().strip()
                                            if confirmar == 's':
                                                resultado = controller.actualizar_material(id_editar, updates)
                                                if resultado:
                                                    print("\n✅ Material actualizado exitosamente")
                                                else:
                                                    print("\n❌ Error al actualizar el material")
                                            else:
                                                print("Operación cancelada")
                                        else:
                                            print("\n⚠️ No se realizaron cambios")
                            
                            except ValueError:
                                print("\n❌ Error: Debe ingresar un ID numérico válido")
                            except Exception as e:
                                print(f"\n❌ Error al procesar: {str(e)}")
                    
                    except Exception as e:
                        print(f"\n❌ Error inesperado: {str(e)}")

                    input("\nPresione ENTER para continuar...")
                    limpiar_pantalla()
                    break



            elif opcion_material.opcionSub == "3":
                while True:
                    print("\n=== Eliminar Material (Marcar como Inactivo) ===")
                    controller = MaterialController(connection_string)
                    
                    try:
                        # Obtener y mantener la lista de materiales activos
                        materiales_activos = controller.obtener_todos_materiales(activos_only=True)
                        
                        if not materiales_activos:
                            print("\nℹ️ No hay materiales activos registrados")
                            input("\nPresione ENTER para continuar...")
                            limpiar_pantalla()
                            break
                            
                        print("\nMateriales ACTIVOS disponibles:")
                        for m in materiales_activos:
                            print(f"ID: {m.id_material} - {m.nombre} ({m.categoria or 'Sin categoría'})")
                        
                        try:
                            id_input = input("\nIngrese el ID del material a eliminar (0 para cancelar): ").strip()
                            
                            if id_input == "0":
                                print("Operación cancelada")
                                limpiar_pantalla()
                                break
                            
                            id_eliminar = int(id_input)
                            
                            # Buscar en la lista ya cargada
                            material = next((m for m in materiales_activos if m.id_material == id_eliminar), None)
                            
                            if not material:
                                print("\n❌ El ID no corresponde a ningún material mostrado")
                            else:
                                print("\n⚠️ ATENCIÓN: Esta acción marcará el material como INACTIVO")
                                print(f"ID: {material.id_material}")
                                print(f"Nombre: {material.nombre}")
                                print(f"Unidad: {material.unidad_medida}")
                                print(f"Categoría: {material.categoria or 'No especificada'}")
                                print(f"Marca: {material.marca or 'No especificada'}")
                                
                                confirmar = input("\n¿ESTÁ SEGURO que desea continuar? (s/n): ").lower()
                                if confirmar == 's':
                                    if controller.eliminar_material(id_eliminar):
                                        print("\n✅ Material marcado como inactivo correctamente")
                                    else:
                                        print("\n❌ Error al realizar la operación")
                        
                        except ValueError:
                            print("\n❌ Debe ingresar un número válido")
                        
                    except Exception as e:
                        print(f"\n❌ Error inesperado: {str(e)}")
                    
                    input("\nPresione ENTER para continuar...")
                    limpiar_pantalla()
                    break

            elif opcion_material.opcionSub == "4":
                while True:
                    print("\n=== Buscar Material ===")
                    print("Ingrese '0' para cancelar y volver al menú anterior\n")
                    controller = MaterialController(connection_string)

                    try:
                        criterio = input("Ingrese ID, nombre o categoría del material: ").strip()

                        # Opción para cancelar
                        if criterio == "0":
                            print("\nOperación cancelada por el usuario")
                            limpiar_pantalla()
                            break

                        if not criterio:
                            print("\n❌ Debe ingresar un criterio de búsqueda")
                            input("\nPresione ENTER para continuar...")
                            limpiar_pantalla()
                            continue

                        materiales = []

                        # Búsqueda por ID si es numérico
                        if criterio.isdigit():
                            material = controller.obtener_material(int(criterio))
                            if material:
                                materiales = [material]
                        else:
                            # Búsqueda por nombre o categoría
                            todos_materiales = controller.obtener_todos_materiales(activos_only=False)
                            criterio_lower = criterio.lower()
                            materiales = [
                                m for m in todos_materiales
                                if (criterio_lower in m.nombre.lower() or
                                    (m.categoria and criterio_lower in m.categoria.lower()))
                            ]

                        if not materiales:
                            print("\n🔍 No se encontraron materiales con ese criterio")
                        else:
                            print(f"\n🔎 Resultados encontrados ({len(materiales)}):")
                            for m in materiales:
                                estado = "ACTIVO" if m.activo else "INACTIVO"
                                print(f"\nID: {m.id_material} ({estado})")
                                print(f"Nombre: {m.nombre}")
                                print(f"Unidad de Medida: {m.unidad_medida}")
                                print(f"Categoría: {m.categoria or 'No especificada'}")
                                print(f"Marca: {m.marca or 'No especificada'}")
                                print(f"Fecha Registro: {m.fecha_registro.strftime('%d/%m/%Y')}")
                                print("-" * 30)

                        input("\nPresione ENTER para continuar...")
                        limpiar_pantalla()
                        break

                    except ValueError:
                        print("\n❌ El ID debe ser un número válido")
                        input("\nPresione ENTER para continuar...")
                        limpiar_pantalla()
                    except Exception as e:
                        print(f"\n❌ Error inesperado: {str(e)}")
                        input("\nPresione ENTER para continuar...")
                        limpiar_pantalla()

            elif opcion_material.opcionSub == "5":
                while True:
                    print("\n=== Listado Completo de Materiales ===")
                    controller = MaterialController(connection_string)  # Instancia local del controlador

                    try:
                        # Validar entrada del usuario
                        opcion = input("¿Mostrar materiales inactivos? (s/n) o 0 para cancelar: ").lower()

                        if opcion not in ['s', 'n', '0']:
                            print("⚠️ Opción no válida. Ingrese 's', 'n' o '0'.")
                            input("\nPresione ENTER para continuar...")
                            limpiar_pantalla()
                            continue

                        if opcion == '0':
                            print("\n🚫 Operación cancelada por el usuario.")
                            input("\nPresione ENTER para continuar...")
                            limpiar_pantalla()
                            break  # Salir del ciclo while


                        mostrar_inactivos = opcion == 's'

                        # Obtener materiales según filtro
                        materiales = controller.obtener_todos_materiales(activos_only=not mostrar_inactivos)

                        if not materiales:
                            estado = "activos" if not mostrar_inactivos else "registrados"
                            print(f"\nℹ️ No hay materiales {estado} en el sistema")
                        else:
                            estado = "ACTIVOS" if not mostrar_inactivos else "TODOS (activos e inactivos)"
                            print(f"\n📋 Listado de materiales ({estado}) - Total: {len(materiales)}")
                            print("=" * 60)

                            for m in materiales:
                                estado = "ACTIVO" if m.activo else "INACTIVO"
                                print(f"\nID: {m.id_material} ({estado})")
                                print(f"Nombre: {m.nombre}")
                                print(f"Unidad de Medida: {m.unidad_medida or 'No especificada'}")
                                print(f"Categoría: {m.categoria or 'No especificada'}")
                                print(f"Marca: {m.marca or 'No especificada'}")
                                print(f"Fecha Registro: {m.fecha_registro.strftime('%d/%m/%Y') if m.fecha_registro else 'No registrada'}")
                                print("-" * 60)

                    except Exception as e:
                        print(f"\n❌ Error al obtener materiales: {str(e)}")

                    input("\nPresione ENTER para continuar...")
                    limpiar_pantalla()
                    break

            

            elif opcion_material.opcionSub == "6":  
                limpiar_pantalla()
                break





    # Si el usuario elige "5", sale de la app
    elif entrada.opcion == "5":
        print("Vuelve pronto")
        break

    # Si no se ingresa una opción válida (aunque con pydantic esto no debería pasar)
    # print("---")



