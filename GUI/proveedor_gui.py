# proveedor_gui.py
from Controllers.proveedor_controller import ProveedorController
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem
)

class ProveedorGUI(QWidget):
    def __init__(self, connection_string):
        super().__init__()
        self.controller = ProveedorController(connection_string)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gestión de Proveedores")

        layout = QVBoxLayout()

        # --------- Formularios ---------
        form_layout = QHBoxLayout()

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre Proveedor")

        self.contacto_input = QLineEdit()
        self.contacto_input.setPlaceholderText("Nombre Contacto")

        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Teléfono")

        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText("Correo")

        self.direccion_input = QLineEdit()
        self.direccion_input.setPlaceholderText("Dirección")

        self.rfc_input = QLineEdit()
        self.rfc_input.setPlaceholderText("RFC")


        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(self.contacto_input)
        form_layout.addWidget(self.telefono_input)
        form_layout.addWidget(self.correo_input)
        form_layout.addWidget(self.rfc_input) 
        form_layout.addWidget(self.direccion_input)

        layout.addLayout(form_layout)

        # --------- Botones ---------
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Agregar Proveedor")
        self.update_button = QPushButton("Actualizar Proveedor")
        self.delete_button = QPushButton("Eliminar Proveedor")
        self.search_button = QPushButton("Buscar por Nombre")
        self.refresh_button = QPushButton("Refrescar Lista")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.refresh_button)

        layout.addLayout(button_layout)

        # # --------- Tabla de Proveedores ---------
        # self.proveedor_table = QTableWidget()
        # self.proveedor_table.setColumnCount(7)
        # self.proveedor_table.setHorizontalHeaderLabels([
        #     "ID", "Nombre", "Nombre Contacto", "Teléfono", "Correo", "Dirección", "Activo"
        # ])
        # --------- Tabla de Proveedores ---------
        self.proveedor_table = QTableWidget()
        self.proveedor_table.setColumnCount(9)
        self.proveedor_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Contacto", "Teléfono", "Correo", "RFC", "Dirección", "Fecha Registro", "Activo"
        ])


        layout.addWidget(self.proveedor_table)

        self.setLayout(layout)

        # --------- Conexiones ---------
        self.add_button.clicked.connect(self.agregar_proveedor)
        self.update_button.clicked.connect(self.actualizar_proveedor)
        self.delete_button.clicked.connect(self.eliminar_proveedor)
        self.search_button.clicked.connect(self.buscar_proveedor)
        self.refresh_button.clicked.connect(self.cargar_proveedores)

        self.proveedor_table.cellClicked.connect(self.seleccionar_proveedor)

        self.selected_id = None
        self.cargar_proveedores()

    def agregar_proveedor(self):
        data = {
            "nombre": self.nombre_input.text(),
            "contacto": self.contacto_input.text(),  # 🔥 Aquí cambiar
            "telefono": self.telefono_input.text(),
            "correo": self.correo_input.text(),
            "rfc": self.rfc_input.text(),
            "direccion": self.direccion_input.text(),
        }
        try:
            self.controller.crear_proveedor(data)
            QMessageBox.information(self, "Éxito", "Proveedor agregado correctamente.")
            self.limpiar_formulario()
            self.cargar_proveedores()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar proveedor: {str(e)}")

    def actualizar_proveedor(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Advertencia", "Selecciona un proveedor primero.")
            return

        data = {
            "nombre": self.nombre_input.text(),
            "contacto": self.contacto_input.text(),
            "telefono": self.telefono_input.text(),
            "correo": self.correo_input.text(),
            "rfc": self.rfc_input.text(),  # 👈 Agregado
            "direccion": self.direccion_input.text(),
        }

        try:
            self.controller.actualizar_proveedor(self.selected_id, data)
            QMessageBox.information(self, "Éxito", "Proveedor actualizado correctamente.")
            self.limpiar_formulario()
            self.cargar_proveedores()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar proveedor: {str(e)}")

    def eliminar_proveedor(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Advertencia", "Selecciona un proveedor primero.")
            return
        try:
            self.controller.eliminar_proveedor(self.selected_id)
            QMessageBox.information(self, "Éxito", "Proveedor eliminado (lógicamente).")
            self.limpiar_formulario()
            self.cargar_proveedores()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar proveedor: {str(e)}")

    def buscar_proveedor(self):
        nombre = self.nombre_input.text()
        proveedores = self.controller.buscar_por_nombre(nombre)
        self.mostrar_proveedores(proveedores)

    def cargar_proveedores(self):
        proveedores = self.controller.obtener_todos_proveedores()
        self.mostrar_proveedores(proveedores)

    # def mostrar_proveedores(self, proveedores):
    #     self.proveedor_table.setRowCount(0)
    #     for proveedor in proveedores:
    #         row_position = self.proveedor_table.rowCount()
    #         self.proveedor_table.insertRow(row_position)
    #         self.proveedor_table.setItem(row_position, 0, QTableWidgetItem(str(proveedor.id_proveedor)))
    #         self.proveedor_table.setItem(row_position, 1, QTableWidgetItem(proveedor.nombre))
    #         self.proveedor_table.setItem(row_position, 2, QTableWidgetItem(proveedor.nombre_contacto or ""))
    #         self.proveedor_table.setItem(row_position, 3, QTableWidgetItem(proveedor.telefono or ""))
    #         self.proveedor_table.setItem(row_position, 4, QTableWidgetItem(proveedor.correo or ""))
    #         self.proveedor_table.setItem(row_position, 5, QTableWidgetItem(proveedor.direccion or ""))
    #         self.proveedor_table.setItem(row_position, 6, QTableWidgetItem("Sí" if proveedor.activo else "No"))
#### def mostrar_proveedores(self, proveedores):
    #     self.proveedor_table.setRowCount(0)
    #     for proveedor in proveedores:
    #         row_position = self.proveedor_table.rowCount()
    #         self.proveedor_table.insertRow(row_position)
    #         self.proveedor_table.setItem(row_position, 0, QTableWidgetItem(str(proveedor.id_proveedor)))
    #         self.proveedor_table.setItem(row_position, 1, QTableWidgetItem(proveedor.nombre))
    #         self.proveedor_table.setItem(row_position, 2, QTableWidgetItem(proveedor.contacto or ""))  # 🔥 aquí corregido
    #         self.proveedor_table.setItem(row_position, 3, QTableWidgetItem(proveedor.telefono or ""))
    #         self.proveedor_table.setItem(row_position, 4, QTableWidgetItem(proveedor.correo or ""))
    #         self.proveedor_table.setItem(row_position, 5, QTableWidgetItem(proveedor.rfc or ""))
    #         self.proveedor_table.setItem(row_position, 6, QTableWidgetItem(proveedor.direccion or ""))
    #         self.proveedor_table.setItem(row_position, 7, QTableWidgetItem(
    #             proveedor.fecha_registro.strftime('%Y-%m-%d %H:%M') if proveedor.fecha_registro else ""
    #         ))
    #         self.proveedor_table.setItem(row_position, 8, QTableWidgetItem("Sí" if proveedor.activo else "No"))
    def mostrar_proveedores(self, proveedores):
        self.proveedor_table.setRowCount(0)
        for proveedor in proveedores:
            row_position = self.proveedor_table.rowCount()
            self.proveedor_table.insertRow(row_position)
            self.proveedor_table.setItem(row_position, 0, QTableWidgetItem(str(proveedor.id_proveedor)))
            self.proveedor_table.setItem(row_position, 1, QTableWidgetItem(proveedor.nombre))
            self.proveedor_table.setItem(row_position, 2, QTableWidgetItem(proveedor.contacto or ""))
            self.proveedor_table.setItem(row_position, 3, QTableWidgetItem(proveedor.telefono or ""))
            self.proveedor_table.setItem(row_position, 4, QTableWidgetItem(proveedor.correo or ""))
            self.proveedor_table.setItem(row_position, 5, QTableWidgetItem(proveedor.rfc or ""))
            self.proveedor_table.setItem(row_position, 6, QTableWidgetItem(proveedor.direccion or ""))
            self.proveedor_table.setItem(row_position, 7, QTableWidgetItem(
                proveedor.fecha_registro.strftime('%Y-%m-%d %H:%M') if proveedor.fecha_registro else ""
            ))
            self.proveedor_table.setItem(row_position, 8, QTableWidgetItem("Sí" if proveedor.activo else "No"))


    def seleccionar_proveedor(self, row, column):
        self.selected_id = int(self.proveedor_table.item(row, 0).text())
        self.nombre_input.setText(self.proveedor_table.item(row, 1).text())
        self.contacto_input.setText(self.proveedor_table.item(row, 2).text())
        self.telefono_input.setText(self.proveedor_table.item(row, 3).text())
        self.correo_input.setText(self.proveedor_table.item(row, 4).text())
        self.rfc_input.setText(self.proveedor_table.item(row, 5).text())  # 👈 Agregado
        self.direccion_input.setText(self.proveedor_table.item(row, 6).text())


    def limpiar_formulario(self):
        self.nombre_input.clear()
        self.contacto_input.clear()
        self.telefono_input.clear()
        self.correo_input.clear()
        self.rfc_input.clear()  # 👈 Agregado
        self.direccion_input.clear()
        self.selected_id = None


if __name__ == "__main__":
    from Database.Conexion import obtener_conexion

    connection = obtener_conexion()
    if connection is None:
        print("❌ No se pudo conectar a la base de datos.")
        exit()

    app = QApplication(sys.argv)
    ventana = ProveedorGUI(connection)
    ventana.show()
    sys.exit(app.exec_())
