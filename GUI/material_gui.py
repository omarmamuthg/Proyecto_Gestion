# # material_gui.py
# from Controllers.material_controller import MaterialController
# from datetime import datetime
# import sys
# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QHBoxLayout,
#     QPushButton, QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem
# )

# class MaterialGUI(QWidget):
#     def __init__(self, connection):
#         super().__init__()
#         self.controller = MaterialController(connection)  # Pasamos la conexión abierta aquí
#         self.init_ui()

#     def init_ui(self):
#         self.setWindowTitle("Gestión de Materiales")

#         layout = QVBoxLayout()

#         # --------- Formularios ---------
#         form_layout = QHBoxLayout()

#         self.nombre_input = QLineEdit()
#         self.nombre_input.setPlaceholderText("Nombre del Material")

#         self.descripcion_input = QLineEdit()
#         self.descripcion_input.setPlaceholderText("Descripción (opcional)")

#         self.unidad_medida_input = QLineEdit()
#         self.unidad_medida_input.setPlaceholderText("Unidad de Medida (ej: kg, l, m, pz)")

#         self.marca_input = QLineEdit()
#         self.marca_input.setPlaceholderText("Marca")

#         self.categoria_input = QLineEdit()
#         self.categoria_input.setPlaceholderText("Categoría")

#         form_layout.addWidget(self.nombre_input)
#         form_layout.addWidget(self.descripcion_input)
#         form_layout.addWidget(self.unidad_medida_input)
#         form_layout.addWidget(self.marca_input)
#         form_layout.addWidget(self.categoria_input)

#         layout.addLayout(form_layout)

#         # --------- Botones ---------
#         button_layout = QHBoxLayout()

#         self.add_button = QPushButton("Agregar Material")
#         self.update_button = QPushButton("Actualizar Material")
#         self.delete_button = QPushButton("Eliminar Material")
#         self.search_button = QPushButton("Buscar por Nombre")
#         self.refresh_button = QPushButton("Refrescar Lista")

#         button_layout.addWidget(self.add_button)
#         button_layout.addWidget(self.update_button)
#         button_layout.addWidget(self.delete_button)
#         button_layout.addWidget(self.search_button)
#         button_layout.addWidget(self.refresh_button)

#         layout.addLayout(button_layout)

#         # --------- Tabla de Materiales ---------
#         self.material_table = QTableWidget()
#         self.material_table.setColumnCount(7)
#         self.material_table.setHorizontalHeaderLabels([
#             "ID", "Nombre", "Descripción", "Unidad Medida",
#             "Marca", "Categoría", "Activo"
#         ])

#         layout.addWidget(self.material_table)

#         self.setLayout(layout)

#         # --------- Conexiones ---------
#         self.add_button.clicked.connect(self.agregar_material)
#         self.update_button.clicked.connect(self.actualizar_material)
#         self.delete_button.clicked.connect(self.eliminar_material)
#         self.search_button.clicked.connect(self.buscar_material)
#         self.refresh_button.clicked.connect(self.cargar_materiales)

#         self.material_table.cellClicked.connect(self.seleccionar_material)

#         self.selected_id = None
#         self.cargar_materiales()

#     # def agregar_material(self):
#     #     data = {
#     #         "nombre": self.nombre_input.text(),
#     #         "descripcion": self.descripcion_input.text(),
#     #         "unidad_medida": self.unidad_medida_input.text(),
#     #         "marca": self.marca_input.text(),
#     #         "categoria": self.categoria_input.text(),
#     #     }
#     #     try:
#     #         self.controller.crear_material(data)
#     #         QMessageBox.information(self, "Éxito", "Material agregado correctamente.")
#     #         self.limpiar_formulario()
#     #         self.cargar_materiales()
#     #     except Exception as e:
#     #         QMessageBox.critical(self, "Error", f"Error al agregar material: {str(e)}")


#     def agregar_material(self):
#         data = {
#             "nombre": self.nombre_input.text(),
#             "descripcion": self.descripcion_input.text(),
#             "unidad_medida": self.unidad_medida_input.text(),
#             "marca": self.marca_input.text(),
#             "categoria": self.categoria_input.text(),
#             "fecha_registro": datetime.now()  # Se añade la fecha de registro actual
#         }
#         try:
#             self.controller.crear_material(data)
#             QMessageBox.information(self, "Éxito", "Material agregado correctamente.")
#             self.limpiar_formulario()
#             self.cargar_materiales()
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Error al agregar material: {str(e)}")


#     def actualizar_material(self):
#         if not self.selected_id:
#             QMessageBox.warning(self, "Advertencia", "Selecciona un material primero.")
#             return

#         data = {
#             "nombre": self.nombre_input.text(),
#             "descripcion": self.descripcion_input.text(),
#             "unidad_medida": self.unidad_medida_input.text(),
#             "marca": self.marca_input.text(),
#             "categoria": self.categoria_input.text(),
#         }
#         try:
#             self.controller.actualizar_material(self.selected_id, data)
#             QMessageBox.information(self, "Éxito", "Material actualizado correctamente.")
#             self.limpiar_formulario()
#             self.cargar_materiales()
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Error al actualizar material: {str(e)}")

#     def eliminar_material(self):
#         if not self.selected_id:
#             QMessageBox.warning(self, "Advertencia", "Selecciona un material primero.")
#             return
#         try:
#             self.controller.eliminar_material(self.selected_id)
#             QMessageBox.information(self, "Éxito", "Material eliminado (lógicamente).")
#             self.limpiar_formulario()
#             self.cargar_materiales()
#         except Exception as e:
#             QMessageBox.critical(self, "Error", f"Error al eliminar material: {str(e)}")

#     def buscar_material(self):
#         nombre = self.nombre_input.text()
#         materiales = self.controller.buscar_por_nombre(nombre)
#         self.mostrar_materiales(materiales)

#     def cargar_materiales(self):
#         materiales = self.controller.obtener_todos_materiales()
#         self.mostrar_materiales(materiales)

#     def mostrar_materiales(self, materiales):
#         self.material_table.setRowCount(0)
#         for material in materiales:
#             row_position = self.material_table.rowCount()
#             self.material_table.insertRow(row_position)
#             self.material_table.setItem(row_position, 0, QTableWidgetItem(str(material.id_material)))
#             self.material_table.setItem(row_position, 1, QTableWidgetItem(material.nombre))
#             self.material_table.setItem(row_position, 2, QTableWidgetItem(material.descripcion or ""))
#             self.material_table.setItem(row_position, 3, QTableWidgetItem(material.unidad_medida or ""))
#             self.material_table.setItem(row_position, 4, QTableWidgetItem(material.marca or ""))
#             self.material_table.setItem(row_position, 5, QTableWidgetItem(material.categoria or ""))
#             self.material_table.setItem(row_position, 6, QTableWidgetItem("Sí" if material.activo else "No"))

#     def seleccionar_material(self, row, column):
#         self.selected_id = int(self.material_table.item(row, 0).text())
#         self.nombre_input.setText(self.material_table.item(row, 1).text())
#         self.descripcion_input.setText(self.material_table.item(row, 2).text())
#         self.unidad_medida_input.setText(self.material_table.item(row, 3).text())
#         self.marca_input.setText(self.material_table.item(row, 4).text())
#         self.categoria_input.setText(self.material_table.item(row, 5).text())

#     def limpiar_formulario(self):
#         self.nombre_input.clear()
#         self.descripcion_input.clear()
#         self.unidad_medida_input.clear()
#         self.marca_input.clear()
#         self.categoria_input.clear()
#         self.selected_id = None

# if __name__ == "__main__":
#     from Database.Conexion import obtener_conexion

#     connection = obtener_conexion()  # Se obtiene la conexión
#     if connection is None:
#         print("❌ No se pudo conectar a la base de datos.")
#         exit()

#     app = QApplication(sys.argv)
#     ventana = MaterialGUI(connection)  # Se pasa la conexión abierta
#     ventana.show()
#     sys.exit(app.exec_())

# material_gui.py
from Controllers.material_controller import MaterialController
from Controllers.proveedor_controller import ProveedorController
from Controllers.proveedor_material_controller import ProveedorMaterialController
from datetime import datetime
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
)

class MaterialGUI(QWidget):
    def __init__(self, connection_string):
        super().__init__()
        self.controller = MaterialController(connection_string)  # Pasamos la cadena de conexión aquí
        self.proveedor_controller = ProveedorController(connection_string)
        self.proveedor_material_controller = ProveedorMaterialController(connection_string)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gestión de Materiales")

        layout = QVBoxLayout()

        # --------- Formularios ---------
        form_layout = QHBoxLayout()

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del Material")

        self.descripcion_input = QLineEdit()
        self.descripcion_input.setPlaceholderText("Descripción (opcional)")

        self.unidad_medida_input = QLineEdit()
        self.unidad_medida_input.setPlaceholderText("Unidad de Medida (ej: kg, l, m, pz)")

        self.marca_input = QLineEdit()
        self.marca_input.setPlaceholderText("Marca")

        self.categoria_input = QLineEdit()
        self.categoria_input.setPlaceholderText("Categoría")

        form_layout.addWidget(self.nombre_input)
        form_layout.addWidget(self.descripcion_input)
        form_layout.addWidget(self.unidad_medida_input)
        form_layout.addWidget(self.marca_input)
        form_layout.addWidget(self.categoria_input)

        layout.addLayout(form_layout)

        # --------- Botones ---------
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Agregar Material")
        self.update_button = QPushButton("Actualizar Material")
        self.delete_button = QPushButton("Eliminar Material")
        self.search_button = QPushButton("Buscar por Nombre")
        self.refresh_button = QPushButton("Refrescar Lista")
        self.link_supplier_button = QPushButton("Vincular con Proveedor")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.link_supplier_button)

        layout.addLayout(button_layout)

        # --------- Tabla de Materiales ---------
        self.material_table = QTableWidget()
        self.material_table.setColumnCount(7)
        self.material_table.setHorizontalHeaderLabels([
            "ID", "Nombre", "Descripción", "Unidad Medida",
            "Marca", "Categoría", "Activo"
        ])

        layout.addWidget(self.material_table)

        self.setLayout(layout)

        # --------- Conexiones ---------
        self.add_button.clicked.connect(self.agregar_material)
        self.update_button.clicked.connect(self.actualizar_material)
        self.delete_button.clicked.connect(self.eliminar_material)
        self.search_button.clicked.connect(self.buscar_material)
        self.refresh_button.clicked.connect(self.cargar_materiales)
        self.link_supplier_button.clicked.connect(self.vincular_con_proveedor)

        self.material_table.cellClicked.connect(self.seleccionar_material)

        self.selected_id = None
        self.cargar_materiales()

    def agregar_material(self):
        data = {
            "nombre": self.nombre_input.text(),
            "descripcion": self.descripcion_input.text(),
            "unidad_medida": self.unidad_medida_input.text(),
            "marca": self.marca_input.text(),
            "categoria": self.categoria_input.text(),
            "fecha_registro": datetime.now()  # Se añade la fecha de registro actual
        }
        try:
            material_creado = self.controller.crear_material(data)
            QMessageBox.information(self, "Éxito", "Material agregado correctamente.")
            self.limpiar_formulario()
            self.cargar_materiales()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar material: {str(e)}")

    def actualizar_material(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Advertencia", "Selecciona un material primero.")
            return

        data = {
            "nombre": self.nombre_input.text(),
            "descripcion": self.descripcion_input.text(),
            "unidad_medida": self.unidad_medida_input.text(),
            "marca": self.marca_input.text(),
            "categoria": self.categoria_input.text(),
        }
        try:
            self.controller.actualizar_material(self.selected_id, data)
            QMessageBox.information(self, "Éxito", "Material actualizado correctamente.")
            self.limpiar_formulario()
            self.cargar_materiales()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar material: {str(e)}")

    def eliminar_material(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Advertencia", "Selecciona un material primero.")
            return
        try:
            self.controller.eliminar_material(self.selected_id)
            QMessageBox.information(self, "Éxito", "Material eliminado (lógicamente).")
            self.limpiar_formulario()
            self.cargar_materiales()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar material: {str(e)}")

    def buscar_material(self):
        nombre = self.nombre_input.text()
        materiales = self.controller.buscar_por_nombre(nombre)
        self.mostrar_materiales(materiales)

    def cargar_materiales(self):
        materiales = self.controller.obtener_todos_materiales()
        self.mostrar_materiales(materiales)

    def mostrar_materiales(self, materiales):
        self.material_table.setRowCount(0)
        for material in materiales:
            row_position = self.material_table.rowCount()
            self.material_table.insertRow(row_position)
            self.material_table.setItem(row_position, 0, QTableWidgetItem(str(material.id_material)))
            self.material_table.setItem(row_position, 1, QTableWidgetItem(material.nombre))
            self.material_table.setItem(row_position, 2, QTableWidgetItem(material.descripcion or ""))
            self.material_table.setItem(row_position, 3, QTableWidgetItem(material.unidad_medida or ""))
            self.material_table.setItem(row_position, 4, QTableWidgetItem(material.marca or ""))
            self.material_table.setItem(row_position, 5, QTableWidgetItem(material.categoria or ""))
            self.material_table.setItem(row_position, 6, QTableWidgetItem("Sí" if material.activo else "No"))

    def seleccionar_material(self, row, column):
        self.selected_id = int(self.material_table.item(row, 0).text())
        self.nombre_input.setText(self.material_table.item(row, 1).text())
        self.descripcion_input.setText(self.material_table.item(row, 2).text())
        self.unidad_medida_input.setText(self.material_table.item(row, 3).text())
        self.marca_input.setText(self.material_table.item(row, 4).text())
        self.categoria_input.setText(self.material_table.item(row, 5).text())

    def limpiar_formulario(self):
        self.nombre_input.clear()
        self.descripcion_input.clear()
        self.unidad_medida_input.clear()
        self.marca_input.clear()
        self.categoria_input.clear()
        self.selected_id = None

    def vincular_con_proveedor(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Advertencia", "Selecciona un material primero.")
            return

        proveedores = self.proveedor_controller.obtener_todos_proveedores()
        if not proveedores:
            QMessageBox.warning(self, "Advertencia", "No hay proveedores disponibles.")
            return

        # Crear un cuadro de selección de proveedores
        proveedor_names = [p.nombre for p in proveedores]
        proveedor_combobox = QComboBox(self)
        proveedor_combobox.addItems(proveedor_names)

        precio_input = QLineEdit(self)
        precio_input.setPlaceholderText("Precio ofrecido por el proveedor")

        # Mostrar ventana emergente para confirmar vinculación
        confirm_dialog = QWidget()
        dialog_layout = QVBoxLayout()

        dialog_layout.addWidget(QLabel("Selecciona un proveedor:"))
        dialog_layout.addWidget(proveedor_combobox)
        dialog_layout.addWidget(precio_input)

        confirm_dialog.setLayout(dialog_layout)

        def confirm_vinculacion():
            proveedor_seleccionado = proveedores[proveedor_combobox.currentIndex()]
            precio = precio_input.text()

            if not precio:
                QMessageBox.warning(self, "Advertencia", "El precio es obligatorio.")
                return

            try:
                precio = float(precio)
                if precio <= 0:
                    QMessageBox.warning(self, "Advertencia", "El precio debe ser mayor que cero.")
                    return

                resultado = self.proveedor_material_controller.vincular_material(
                    proveedor_seleccionado.id_proveedor,
                    self.selected_id,
                    precio
                )
                if resultado:
                    QMessageBox.information(self, "Éxito", "Material vinculado con proveedor.")
                    confirm_dialog.close()
                else:
                    QMessageBox.critical(self, "Error", "No se pudo vincular el material con el proveedor. Revisa la consola para más detalles.")
            except ValueError:
                QMessageBox.warning(self, "Advertencia", "El precio debe ser un número válido.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al vincular: {str(e)}")

        # Agregar un botón para confirmar la vinculación
        confirm_button = QPushButton("Vincular Material")
        confirm_button.clicked.connect(confirm_vinculacion)
        dialog_layout.addWidget(confirm_button)

        confirm_dialog.show()

if __name__ == "__main__":
    from Database.Conexion import obtener_conexion

    connection_string = obtener_conexion()  # Se obtiene la cadena de conexión
    if connection_string is None:
        print("❌ No se pudo conectar a la base de datos.")
        exit()

    app = QApplication(sys.argv)
    ventana = MaterialGUI(connection_string)  # Se pasa la cadena de conexión
    ventana.show()
    sys.exit(app.exec_())
