#Funciones del Main
from pydantic import BaseModel, ValidationError
from typing import Literal
import os


# Función que imprime el logo en ASCII del sistema
def Logo_siga ():
    print('''  
  ____  _   ____     _ 
 / ___|| | / ___|   / \  
 \___ \| || |  _   / _ \ 
  ___) | || |_| | / ___ \ 
 |____/|_| \____|/_/   \_\
''')
    
# Clase que valida que solo se pueda ingresar una de las opciones válidas del menú (1, 2 o 3)
class MenuInput(BaseModel):
    opcion: Literal["1", "2", "3", "4","5"]  # Solo acepta estas tres cadenas como entrada


# Clase que valida que solo se pueda ingresar una de las opciones válidas del menú (1, 2 o 3)
class SubMenuInput(BaseModel):
    opcionSub: Literal["1", "2", "3", "4", "5", "6"]  # Solo acepta estas tres cadenas como entrada

# Función que limpia la pantalla en sistemas operativos Windows
def limpiar_pantalla():
    os.system("cls")

# Función que imprime el menú principal con tres opciones
def menu_principal():
    print("\n==== Menú Principal ====")
    print("Sobre qué quieres trabajar?")
    print("1. Cliente")
    print("2. Cotizaciones")
    print("3. Proveedores")
    print("4. Materiales")
    print("5. Salir")

# Función que imprime el menú de opciones relacionadas con los clientes
def menu_clientes():
    '''
    Muestra el menú de opciones relacionadas con los clientes.
    '''
    print("\n==== Menú Clientes ====")
    print("1. Agregar Cliente")
    print("2. Editar Cliente")
    print("3. Eliminar Cliente")
    print("4. Buscar Cliente") 
    print("5. Listar Clientes")
    print("6. Volver al menú principal")

# Función que imprime el menú de opciones relacionadas con las cotizaciones
def menu_cotizaciones():
    '''
    Muestra el menú de opciones relacionadas con las cotizaciones.
    '''
    print("\n==== Menú Cotizaciones ====")
    print("1. Crear Cotización")
    print("2. Editar Cotizaciones")
    print("3. Eliminar Cotización")
    print("4. Buscar Cotizacion") 
    print("5. Listar Cotizaciones")  # Nueva opción
    print("6. Volver al menú principal")

# Función que imprime el menú de opciones relacionadas con los proveedores
def menu_proveedores():
    '''
    Muestra el menú de opciones relacionadas con los proveedores.
    '''
    print("\n==== Menú Proveedores ====")
    print("1. Agregar Proveedor")
    print("2. Editar Proveedor")
    print("3. Eliminar Proveedor")
    print("4. Buscar Proveedor") 
    print("5. Listar Todos los Proveedores")
    print("6. Volver al menú principal")

def menu_materiales():
    '''
    Muestra el menú de opciones relacionadas con los materiales.
    '''
    print("\n==== Menú Materiales ====")
    print("1. Agregar Material")
    print("2. Editar Material")
    print("3. Eliminar Material")
    print("4. Buscar Material")
    print("5. Listar Materiales")
    print("6. Volver al menú principal")

# Función para pedir y validar una opción del menú principal
def pedir_opcion_menu():
    while True:
        opcion = input("Ingresa una opción deseada (1-4): ")
        try:
            return MenuInput(opcion=opcion)  # Valida que la opción esté entre "1", "2" o "3"
        except ValidationError:
            print("❌ Entrada inválida. Solo se permite del 1 al 6.")  # Muestra mensaje si la opción es inválida
            print("---")
        limpiar_pantalla()
        Logo_siga()
        menu_principal()




# Función para pedir y validar una opción del menú principal
def pedir_opcion_submenu():
    while True:
        opcion = input("Ingresa una opción deseada (1-6): ")
        try:
            return SubMenuInput(opcionSub=opcion)  
        except ValidationError:
            print("❌ Entrada inválida. Solo se permite del 1 al 6.")  # Muestra mensaje si la opción es inválida
            print("---")