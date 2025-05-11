# # cliente_gui.py
# from Controllers.cliente_controller import ClienteController
# import sys
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QHBoxLayout,
#     QPushButton, QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem
# )

# class ClienteGUI(QWidget):
#     def __init__(self, connection_string):
#         super().__init__()
#         self.controller = ClienteController(connection_string)
#         self.init_ui()

#     def init_ui(self):
#         self.setWindowTitle("Gestión de Clientes")

#         layout = QVBoxLayout()

#         # --------- Formularios ---------
#         form_layout = QHBoxLayout()

#         self.nombre_input = QLineEdit()
#         self.nombre_input.setPlaceholderText("Nombre")

#         self.correo_input = QLineEdit()
#         self.correo_input.setPlaceholderText("Correo")

#         self.telefono_input = QLineEdit()
#         self.telefono_input.setPlaceholderText("Teléfono")

#         self.tipo_cliente_input = QLineEdit()
#         self.tipo_cliente_input.setPlaceholderText("Tipo de Cliente")

#         self.direccion_input = QLineEdit()
#         self.direccion_input.setPlaceholderText("Dirección")

#         self.rfc_input = QLineEdit()
#         self.rfc_input.setPlaceholderText("RFC")

#         form_layout.addWidget(self.nombre_input)
#         form_layout.addWidget(self.correo_input)
#         form_layout.addWidget(self.telefono_input)
#         form_layout.addWidget(self.tipo_cliente_input)
#         form_layout.addWidget(self.direccion_input)
#         form_layout.addWidget(self.rfc_input)

#         layout.addLayout(form_layout)

#         # --------- Botones ---------
#         button_layout = QHBoxLayout()

#         self.add_button = QPushButton("Agregar Cliente")
#         self.update_button = QPushButton("Actualizar Cliente")
#         self.delete_button = QPushButton("Eliminar Cliente")
#         self.search_button = QPushButton("Buscar por Nombre")
#         self.refresh_button = QPushButton("Refrescar Lista")

#         button_layout.addWidget(self.add_button)
#         button_layout.addWidget(self.update_button)
#         button_layout.addWidget(self.delete_button)
#         button_layout.addWidget(self.search_button)
#         button_layout.addWidget(self.refresh_button)

#         layout.addLayout(button_layout)

#         # --------- Tabla de Clientes ---------
#         self.cliente_table = QTableWidget()
#         self.cliente_table.setColumnCount(8)
#         self.cliente_table.setHorizontalHeaderLabels([
#             "ID", "Nombre", "Correo", "Teléfono", "Tipo Cliente",
#             "Dirección", "RFC", "Activo"
#         ])

#         layout.addWidget(self.cliente_table)

#         self.setLayout(layout)

#         # --------- Conexiones ---------
#         self.add_button.clicked.connect(self.agregar_cliente)
#         self.update_button.clicked.connect(self.actualizar_cliente)
#         self.delete_button.clicked.connect(self.eliminar_cliente)
#         self.search_button.clicked.connect(self.buscar_cliente)
#         self.refresh_button.clicked.connect(self.cargar_clientes)

#         self.cliente_table.cellClicked.connect(self.seleccionar_cliente)

#         self.selected_id = None
#         self.cargar_clientes()

#     def agregar_cliente(self):
#         data = {
#             "nombre": self.nombre_input.text(),
#             "correo": self.correo_input.text(),
#             "telefono": self.telefono_input.text(),
#             "tipo_cliente": self.tipo_cliente_input.text(),
#             "direccion": self.direccion_input.text(),
#             "rfc": self.rfc_input.text(),
#         }
#         try:
#             self.controller.crear_cliente(data)
#             QMessageBox.information(self, "Éxito", "Cliente agregado correctamente.")
#             self.limpiar_formulario()
#             self.cargar_clientes()
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Error al agregar cliente: {str(e)}")

#     def actualizar_cliente(self):
#         if not self.selected_id:
#             QMessageBox.warning(self, "Advertencia", "Selecciona un cliente primero.")
#             return

#         data = {
#             "nombre": self.nombre_input.text(),
#             "correo": self.correo_input.text(),
#             "telefono": self.telefono_input.text(),
#             "tipo_cliente": self.tipo_cliente_input.text(),
#             "direccion": self.direccion_input.text(),
#             "rfc": self.rfc_input.text(),
#         }
#         try:
#             self.controller.actualizar_cliente(self.selected_id, data)
#             QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente.")
#             self.limpiar_formulario()
#             self.cargar_clientes()
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Error al actualizar cliente: {str(e)}")

#     def eliminar_cliente(self):
#         if not self.selected_id:
#             QMessageBox.warning(self, "Advertencia", "Selecciona un cliente primero.")
#             return
#         try:
#             self.controller.eliminar_cliente(self.selected_id)
#             QMessageBox.information(self, "Éxito", "Cliente eliminado (lógicamente).")
#             self.limpiar_formulario()
#             self.cargar_clientes()
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Error al eliminar cliente: {str(e)}")

#     def buscar_cliente(self):
#         nombre = self.nombre_input.text()
#         clientes = self.controller.buscar_por_nombre(nombre)
#         self.mostrar_clientes(clientes)

#     def cargar_clientes(self):
#         clientes = self.controller.obtener_todos_clientes()
#         self.mostrar_clientes(clientes)

#     def mostrar_clientes(self, clientes):
#         self.cliente_table.setRowCount(0)
#         for cliente in clientes:
#             row_position = self.cliente_table.rowCount()
#             self.cliente_table.insertRow(row_position)
#             self.cliente_table.setItem(row_position, 0, QTableWidgetItem(str(cliente.id_cliente)))
#             self.cliente_table.setItem(row_position, 1, QTableWidgetItem(cliente.nombre))
#             self.cliente_table.setItem(row_position, 2, QTableWidgetItem(cliente.correo or ""))
#             self.cliente_table.setItem(row_position, 3, QTableWidgetItem(cliente.telefono or ""))
#             self.cliente_table.setItem(row_position, 4, QTableWidgetItem(cliente.tipo_cliente or ""))
#             self.cliente_table.setItem(row_position, 5, QTableWidgetItem(cliente.direccion or ""))
#             self.cliente_table.setItem(row_position, 6, QTableWidgetItem(cliente.rfc or ""))
#             self.cliente_table.setItem(row_position, 7, QTableWidgetItem("Sí" if cliente.activo else "No"))

#     def seleccionar_cliente(self, row, column):
#         self.selected_id = int(self.cliente_table.item(row, 0).text())
#         self.nombre_input.setText(self.cliente_table.item(row, 1).text())
#         self.correo_input.setText(self.cliente_table.item(row, 2).text())
#         self.telefono_input.setText(self.cliente_table.item(row, 3).text())
#         self.tipo_cliente_input.setText(self.cliente_table.item(row, 4).text())
#         self.direccion_input.setText(self.cliente_table.item(row, 5).text())
#         self.rfc_input.setText(self.cliente_table.item(row, 6).text())

#     def limpiar_formulario(self):
#         self.nombre_input.clear()
#         self.correo_input.clear()
#         self.telefono_input.clear()
#         self.tipo_cliente_input.clear()
#         self.direccion_input.clear()
#         self.rfc_input.clear()
#         self.selected_id = None

# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)

# #     # Reemplaza esta cadena por tu conexión real a la base de datos
# #     connection_string = "DRIVER={SQL Server};SERVER=tu_servidor;DATABASE=tu_bd;UID=usuario;PWD=contraseña"

# #     ventana = ClienteGUI(connection_string)
# #     ventana.show()
# #     sys.exit(app.exec_())
# if __name__ == "__main__":
#     from Database.Conexion import obtener_conexion

#     connection = obtener_conexion()
#     if connection is None:
#         print("❌ No se pudo conectar a la base de datos.")
#         exit()

#     import sys
#     from PyQt5.QtWidgets import QApplication

#     app = QApplication(sys.argv)
#     ventana = ClienteGUI(connection)
#     ventana.show()
#     sys.exit(app.exec_())


# cliente_gui.py
from Controllers.cliente_controller import ClienteController
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class ClienteGUI(QWidget):
    def __init__(self, connection_string):
        super().__init__()
        self.controller = ClienteController(connection_string)
        self.init_ui()

    def validar_campo(self, valor, campo, tipo="texto", obligatorio=True):
        """Función para validar campos del formulario"""
        valor = valor.strip() if valor else ""
        errores = []

        if obligatorio and not valor:
            errores.append(f"- El campo {campo} es obligatorio")
            return False, errores

        if valor.isspace():
            errores.append(f"- El campo {campo} no puede contener solo espacios")
            return False, errores

        if tipo == "nombre":
            if valor.isdigit():
                errores.append(f"- El campo {campo} no puede ser solo números")
                return False, errores

        elif tipo == "telefono":
            if not valor.isdigit():
                errores.append(f"- El teléfono solo debe contener números")
                return False, errores
            if len(valor) != 10:
                errores.append(f"- El teléfono debe tener exactamente 10 dígitos")
                return False, errores

        elif tipo == "email" and valor:
            if "@" not in valor or "." not in valor:
                errores.append(f"- Formato de email inválido (debe contener @ y dominio)")
                return False, errores

        elif tipo == "rfc" and valor:
            if len(valor) != 13:
                errores.append(f"- El RFC debe tener exactamente 13 caracteres")
                return False, errores

        elif tipo == "tipo_cliente" and valor:
            # Normalizar el valor para la comparación
            valor_normalizado = valor.lower().replace("í", "i").replace("á", "a")
            if valor_normalizado not in ["persona fisica", "persona moral"]:
                errores.append(f"- Tipo de cliente inválido (debe ser 'Persona Fisica' o 'Persona Moral')")
                return False, errores

        return True, errores

    def normalizar_tipo_cliente(self, valor):
        """Normaliza el tipo de cliente a formato estándar"""
        if not valor:
            return valor
            
        valor = valor.lower().replace("í", "i").replace("á", "a")
        if valor == "persona fisica":
            return "Persona Fisica"
        elif valor == "persona moral":
            return "Persona Moral"
        return valor

    def init_ui(self):
        self.setWindowTitle("Gestión de Clientes")
        self.setGeometry(100, 100, 1200, 600)

        # Establecer fondo rojo
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#FF4C4C"))  # Rojo suave
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setSpacing(15)  # Espaciado entre elementos

        # --------- Formularios ---------
        form_layout = QHBoxLayout()
        form_layout.setSpacing(10)

        # Estilo común para los campos de entrada
        input_style = """
            QLineEdit {
                background-color: white;
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #ccc;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
            }
        """

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre/Razón Social")
        self.nombre_input.setStyleSheet(input_style)

        self.correo_input = QLineEdit()
        self.correo_input.setPlaceholderText("Correo electrónico")
        self.correo_input.setStyleSheet(input_style)

        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("10 dígitos")
        self.telefono_input.setStyleSheet(input_style)

        self.tipo_cliente_input = QLineEdit()
        self.tipo_cliente_input.setPlaceholderText("Persona Fisica/Moral")
        self.tipo_cliente_input.setStyleSheet(input_style)

        self.direccion_input = QLineEdit()
        self.direccion_input.setPlaceholderText("Dirección")
        self.direccion_input.setStyleSheet(input_style)

        self.rfc_input = QLineEdit()
        self.rfc_input.setPlaceholderText("13 caracteres")
        self.rfc_input.setStyleSheet(input_style)

        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(self.correo_input)
        form_layout.addWidget(self.telefono_input)
        form_layout.addWidget(self.tipo_cliente_input)
        form_layout.addWidget(self.direccion_input)
        form_layout.addWidget(self.rfc_input)

        layout.addLayout(form_layout)

        # --------- Botones ---------
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Estilo común para los botones
        button_style = """
            QPushButton {
                background-color: #d3d3d3;
                color: black;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #bbbbbb;
            }
        """

        self.add_button = QPushButton("Agregar Cliente")
        self.update_button = QPushButton("Actualizar Cliente")
        self.delete_button = QPushButton("Eliminar Cliente")
        self.search_button = QPushButton("Buscar por Nombre")
        self.refresh_button = QPushButton("Refrescar Lista")

        # Aplicar estilo a los botones
        for button in [self.add_button, self.update_button, self.delete_button, 
                      self.search_button, self.refresh_button]:
            button.setStyleSheet(button_style)
            button_layout.addWidget(button)

        layout.addLayout(button_layout)

        # --------- Tabla de Clientes ---------
        self.cliente_table = QTableWidget()
        self.cliente_table.setColumnCount(8)
        self.cliente_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Correo", "Teléfono", "Tipo Cliente",
            "Dirección", "RFC", "Activo"
        ])

        # Estilo para la tabla
        self.cliente_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                alternate-background-color: #f9f9f9;
                border: 1px solid #ddd;
                border-radius: 5px;
                gridline-color: #ddd;
            }
            QHeaderView::section {
                background-color: #d3d3d3;
                padding: 5px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)

        layout.addWidget(self.cliente_table)

        self.setLayout(layout)

        # --------- Conexiones ---------
        self.add_button.clicked.connect(self.agregar_cliente)
        self.update_button.clicked.connect(self.actualizar_cliente)
        self.delete_button.clicked.connect(self.eliminar_cliente)
        self.search_button.clicked.connect(self.buscar_cliente)
        self.refresh_button.clicked.connect(self.cargar_clientes)

        self.cliente_table.cellClicked.connect(self.seleccionar_cliente)

        self.selected_id = None
        self.cargar_clientes()

    def validar_formulario(self):
        """Valida todos los campos del formulario"""
        errores = []
        
        # Validar nombre
        valido, err = self.validar_campo(self.nombre_input.text(), "Nombre/Razón Social", tipo="nombre", obligatorio=True)
        if not valido:
            errores.extend(err)

        # Validar correo
        valido, err = self.validar_campo(self.correo_input.text(), "Correo", tipo="email", obligatorio=False)
        if not valido:
            errores.extend(err)

        # Validar teléfono
        valido, err = self.validar_campo(self.telefono_input.text(), "Teléfono", tipo="telefono", obligatorio=True)
        if not valido:
            errores.extend(err)

        # Validar tipo de cliente
        valido, err = self.validar_campo(self.tipo_cliente_input.text(), "Tipo de Cliente", tipo="tipo_cliente", obligatorio=True)
        if not valido:
            errores.extend(err)

        # Validar RFC
        valido, err = self.validar_campo(self.rfc_input.text(), "RFC", tipo="rfc", obligatorio=True)
        if not valido:
            errores.extend(err)

        return len(errores) == 0, errores

    def agregar_cliente(self):
        # Validar formulario
        valido, errores = self.validar_formulario()
        if not valido:
            QMessageBox.critical(self, "Error de Validación", "\n".join(errores))
            return

        data = {
            "nombre": self.nombre_input.text().strip().upper(),
            "correo": self.correo_input.text().strip().lower(),
            "telefono": self.telefono_input.text().strip(),
            "tipo_cliente": self.normalizar_tipo_cliente(self.tipo_cliente_input.text().strip()),
            "direccion": self.direccion_input.text().strip().upper(),
            "rfc": self.rfc_input.text().strip().upper(),
        }

        try:
            self.controller.crear_cliente(data)
            QMessageBox.information(self, "Éxito", "Cliente agregado correctamente.")
            self.limpiar_formulario()
            self.cargar_clientes()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar cliente: {str(e)}")

    def actualizar_cliente(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Advertencia", "Selecciona un cliente primero.")
            return

        # Validar formulario
        valido, errores = self.validar_formulario()
        if not valido:
            QMessageBox.critical(self, "Error de Validación", "\n".join(errores))
            return

        data = {
            "nombre": self.nombre_input.text().strip().upper(),
            "correo": self.correo_input.text().strip().lower(),
            "telefono": self.telefono_input.text().strip(),
            "tipo_cliente": self.normalizar_tipo_cliente(self.tipo_cliente_input.text().strip()),
            "direccion": self.direccion_input.text().strip().upper(),
            "rfc": self.rfc_input.text().strip().upper(),
        }

        try:
            self.controller.actualizar_cliente(self.selected_id, data)
            QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente.")
            self.limpiar_formulario()
            self.cargar_clientes()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar cliente: {str(e)}")

    def eliminar_cliente(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Advertencia", "Selecciona un cliente primero.")
            return

        reply = QMessageBox.question(self, 'Confirmar Eliminación',
                                   '¿Estás seguro que deseas marcar este cliente como inactivo?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                self.controller.eliminar_cliente(self.selected_id)
                QMessageBox.information(self, "Éxito", "Cliente eliminado (lógicamente).")
                self.limpiar_formulario()
                self.cargar_clientes()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar cliente: {str(e)}")

    def buscar_cliente(self):
        nombre = self.nombre_input.text().strip().upper()
        if not nombre:
            QMessageBox.warning(self, "Advertencia", "Ingrese un nombre para buscar.")
            return

        clientes = self.controller.buscar_por_nombre(nombre)
        self.mostrar_clientes(clientes)

    def cargar_clientes(self):
        clientes = self.controller.obtener_todos_clientes()
        self.mostrar_clientes(clientes)

    def mostrar_clientes(self, clientes):
        self.cliente_table.setRowCount(0)
        for cliente in clientes:
            row_position = self.cliente_table.rowCount()
            self.cliente_table.insertRow(row_position)
            self.cliente_table.setItem(row_position, 0, QTableWidgetItem(str(cliente.id_cliente)))
            self.cliente_table.setItem(row_position, 1, QTableWidgetItem(cliente.nombre))
            self.cliente_table.setItem(row_position, 2, QTableWidgetItem(cliente.correo or ""))
            self.cliente_table.setItem(row_position, 3, QTableWidgetItem(cliente.telefono or ""))
            self.cliente_table.setItem(row_position, 4, QTableWidgetItem(cliente.tipo_cliente or ""))
            self.cliente_table.setItem(row_position, 5, QTableWidgetItem(cliente.direccion or ""))
            self.cliente_table.setItem(row_position, 6, QTableWidgetItem(cliente.rfc or ""))
            self.cliente_table.setItem(row_position, 7, QTableWidgetItem("Sí" if cliente.activo else "No"))

    def seleccionar_cliente(self, row, column):
        self.selected_id = int(self.cliente_table.item(row, 0).text())
        self.nombre_input.setText(self.cliente_table.item(row, 1).text())
        self.correo_input.setText(self.cliente_table.item(row, 2).text())
        self.telefono_input.setText(self.cliente_table.item(row, 3).text())
        self.tipo_cliente_input.setText(self.cliente_table.item(row, 4).text())
        self.direccion_input.setText(self.cliente_table.item(row, 5).text())
        self.rfc_input.setText(self.cliente_table.item(row, 6).text())

    def limpiar_formulario(self):
        self.nombre_input.clear()
        self.correo_input.clear()
        self.telefono_input.clear()
        self.tipo_cliente_input.clear()
        self.direccion_input.clear()
        self.rfc_input.clear()
        self.selected_id = None

if __name__ == "__main__":
    from Database.Conexion import obtener_conexion

    connection = obtener_conexion()
    if connection is None:
        print("❌ No se pudo conectar a la base de datos.")
        exit()

    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ventana = ClienteGUI(connection)
    ventana.show()
    sys.exit(app.exec_())