# # menu_principal.py
# import sys
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
# )
# from Database.Conexion import obtener_conexion
# from GUI.cliente_gui import ClienteGUI
# from GUI.proveedor_gui import ProveedorGUI


# class MenuPrincipal(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.connection = obtener_conexion()

#         if self.connection is None:
#             QMessageBox.critical(self, "Error", "❌ No se pudo conectar a la base de datos.")
#             sys.exit()

#         self.init_ui()

#     def init_ui(self):
#         self.setWindowTitle("Menú Principal")
#         self.setGeometry(100, 100, 400, 300)

#         layout = QVBoxLayout()

#         self.btn_cliente = QPushButton("Cliente")
#         self.btn_cotizaciones = QPushButton("Cotizaciones")
#         self.btn_proveedores = QPushButton("Proveedores")
#         self.btn_materiales = QPushButton("Materiales")
#         self.btn_salir = QPushButton("Salir")

#         layout.addWidget(self.btn_cliente)
#         layout.addWidget(self.btn_cotizaciones)
#         layout.addWidget(self.btn_proveedores)
#         layout.addWidget(self.btn_materiales)
#         layout.addWidget(self.btn_salir)

#         self.setLayout(layout)

#         # Conectar botones a funciones
#         self.btn_cliente.clicked.connect(self.abrir_cliente)
#         self.btn_cotizaciones.clicked.connect(self.cotizaciones_no_disponible)
#         # self.btn_proveedores.clicked.connect(self.proveedores_no_disponible)
#         self.btn_proveedores.clicked.connect(self.abrir_proveedor)
#         self.btn_materiales.clicked.connect(self.materiales_no_disponible)
#         self.btn_salir.clicked.connect(self.close)

#     def abrir_cliente(self):
#         self.cliente_window = ClienteGUI(self.connection)
#         self.cliente_window.show()

#     def cotizaciones_no_disponible(self):
#         QMessageBox.information(self, "Info", "🔧 Cotizaciones no disponible todavía.")

#     # def proveedores_no_disponible(self):
#     #     QMessageBox.information(self, "Info", "🔧 Proveedores no disponible todavía.")
#     def abrir_proveedor(self):
#         self.proveedor_window = ProveedorGUI(self.connection)
#         self.proveedor_window.show()


#     def materiales_no_disponible(self):
#         QMessageBox.information(self, "Info", "🔧 Materiales no disponible todavía.")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ventana = MenuPrincipal()
#     ventana.show()
#     sys.exit(app.exec_())



import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox
)
from Database.Conexion import obtener_conexion
from GUI.cliente_gui import ClienteGUI
from GUI.proveedor_gui import ProveedorGUI
from GUI.material_gui import MaterialGUI
from GUI.cotizacion_gui import CotizacionGUI  # 🔥 Agregamos la importación de CotizacionGUI

class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.connection = obtener_conexion()

        if self.connection is None:
            QMessageBox.critical(self, "Error", "❌ No se pudo conectar a la base de datos.")
            sys.exit()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.btn_cliente = QPushButton("Cliente")
        self.btn_cotizaciones = QPushButton("Cotizaciones")
        self.btn_proveedores = QPushButton("Proveedores")
        self.btn_materiales = QPushButton("Materiales")
        self.btn_salir = QPushButton("Salir")

        layout.addWidget(self.btn_cliente)
        layout.addWidget(self.btn_cotizaciones)
        layout.addWidget(self.btn_proveedores)
        layout.addWidget(self.btn_materiales)
        layout.addWidget(self.btn_salir)

        self.setLayout(layout)

        # Conectar botones a funciones
        self.btn_cliente.clicked.connect(self.abrir_cliente)
        self.btn_cotizaciones.clicked.connect(self.abrir_cotizacion)  # 🔥 Cambiamos a abrir_cotizacion
        self.btn_proveedores.clicked.connect(self.abrir_proveedor)
        self.btn_materiales.clicked.connect(self.abrir_material)
        self.btn_salir.clicked.connect(self.close)

    def abrir_cliente(self):
        self.cliente_window = ClienteGUI(self.connection)
        self.cliente_window.show()

    def abrir_cotizacion(self):  # 🔥 Nuevo método para abrir CotizacionGUI
        self.cotizacion_window = CotizacionGUI(self.connection)
        self.cotizacion_window.show()

    def abrir_proveedor(self):
        self.proveedor_window = ProveedorGUI(self.connection)
        self.proveedor_window.show()

    def abrir_material(self):
        from Database.Conexion import obtener_conexion
        connection_string = obtener_conexion()
        if connection_string is None:
            QMessageBox.critical(self, "Error", "❌ No se pudo conectar a la base de datos.")
            return
        self.material_window = MaterialGUI(connection_string)
        self.material_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MenuPrincipal()
    ventana.show()
    sys.exit(app.exec_())
