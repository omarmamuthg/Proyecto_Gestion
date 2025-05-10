import sys
import os
from datetime import datetime
from decimal import Decimal
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Añadir esto al principio del archivo para suprimir las advertencias
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="PyQt5.*")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sip.*")

# El resto del código sigue igual...
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, 
                            QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
                            QTextEdit, QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox,
                            QDialog, QDialogButtonBox, QScrollArea, QFrame, QSplitter,
                            QStatusBar, QToolBar, QAction, QStyle, QFileDialog, QInputDialog, QDateEdit, QCheckBox)
from PyQt5.QtCore import Qt, QSize, QSettings, pyqtSignal, QDate
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QPalette, QKeySequence
import pyodbc
# Cadena de conexión (la misma que ya tienes)
connection_string = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=OMARLAPTOP;'
    'DATABASE=DB_SIGA;'
    'UID=DB_SIGA;'
    'PWD=db_siga'
)
# Importar los controladores
try:
    from Controllers.cliente_controller import ClienteController
    from Controllers.cotizacion_controller import CotizacionController
    from Controllers.material_controller import MaterialController
    from Controllers.cotizacion_material_contoller import CotizacionMaterialController
    from Repositorys.cotizacion_servicio_repository import CotizacionServicioRepository
    from Repositorys.cotizacion_material_repository import CotizacionMaterialRepository
    from Repositorys.proveedor_material_repository import ProveedorMaterialRepository
    from Models.cotizacion import Cotizacion
    from Models.cotizacion_servicio import CotizacionServicio
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    sys.exit(1)

# Importar para generar PDF (opcional)
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# Configuración de la aplicación
APP_NAME = "Sistema de Cotizaciones"
APP_VERSION = "1.0.0"
CONFIG_FILE = "config.ini"

# Colores y estilos
PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#3498db"
ACCENT_COLOR = "#e74c3c"
SUCCESS_COLOR = "#2ecc71"
WARNING_COLOR = "#f39c12"
BACKGROUND_COLOR = "#ecf0f1"
TEXT_COLOR = "#2c3e50"

# Estilos CSS
STYLE_SHEET = f"""
QMainWindow, QDialog {{
    background-color: {BACKGROUND_COLOR};
}}

QTabWidget::pane {{
    border: 1px solid #cccccc;
    background-color: white;
    border-radius: 4px;
}}

QTabBar::tab {{
    background-color: #f0f0f0;
    border: 1px solid #cccccc;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 8px 12px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: white;
    border-bottom: 1px solid white;
}}

QPushButton {{
    background-color: {SECONDARY_COLOR};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    min-width: 100px;
}}

QPushButton:hover {{
    background-color: #2980b9;
}}

QPushButton:pressed {{
    background-color: #1c6ea4;
}}

QPushButton#deleteButton {{
    background-color: {ACCENT_COLOR};
}}

QPushButton#deleteButton:hover {{
    background-color: #c0392b;
}}

QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 6px;
    background-color: white;
}}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 1px solid {SECONDARY_COLOR};
}}

QGroupBox {{
    border: 1px solid #cccccc;
    border-radius: 4px;
    margin-top: 12px;
    font-weight: bold;
    background-color: white;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
    background-color: white;
}}

QTableWidget {{
    border: 1px solid #cccccc;
    border-radius: 4px;
    background-color: white;
    alternate-background-color: #f9f9f9;
}}

QTableWidget::item:selected {{
    background-color: {SECONDARY_COLOR};
    color: white;
}}

QHeaderView::section {{
    background-color: #f0f0f0;
    border: 1px solid #cccccc;
    padding: 4px;
    font-weight: bold;
}}

QStatusBar {{
    background-color: {PRIMARY_COLOR};
    color: white;
}}

QToolBar {{
    background-color: {PRIMARY_COLOR};
    border: none;
    spacing: 3px;
}}

QToolButton {{
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 5px;
}}

QToolButton:hover {{
    background-color: rgba(255, 255, 255, 0.2);
}}

QToolButton:pressed {{
    background-color: rgba(255, 255, 255, 0.1);
}}

QLabel#titleLabel {{
    font-size: 16px;
    font-weight: bold;
    color: {PRIMARY_COLOR};
}}

QLabel#sectionLabel {{
    font-size: 14px;
    font-weight: bold;
    color: {PRIMARY_COLOR};
    border-bottom: 1px solid {PRIMARY_COLOR};
    padding-bottom: 5px;
}}
"""

class ConnectionDialog(QDialog):
    """Diálogo para configurar la conexión a la base de datos"""
    
    def __init__(self, parent=None, connection_string=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Conexión")
        self.setMinimumWidth(500)
        self.connection_string = connection_string
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Formulario de conexión
        form_layout = QFormLayout()
        
        self.server_input = QLineEdit()
        self.database_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Si hay una cadena de conexión existente, intentar extraer los valores
        if self.connection_string:
            try:
                parts = self.connection_string.split(';')
                for part in parts:
                    if '=' in part:
                        key, value = part.split('=', 1)
                        if key.upper() == 'SERVER':
                            self.server_input.setText(value)
                        elif key.upper() == 'DATABASE':
                            self.database_input.setText(value)
                        elif key.upper() == 'UID':
                            self.username_input.setText(value)
                        elif key.upper() == 'PWD':
                            self.password_input.setText(value)
            except:
                pass
        
        form_layout.addRow("Servidor:", self.server_input)
        form_layout.addRow("Base de datos:", self.database_input)
        form_layout.addRow("Usuario:", self.username_input)
        form_layout.addRow("Contraseña:", self.password_input)
        
        layout.addLayout(form_layout)
        
        # Opción de autenticación de Windows
        self.windows_auth_checkbox = QCheckBox("Usar autenticación de Windows")
        self.windows_auth_checkbox.toggled.connect(self.toggle_windows_auth)
        layout.addWidget(self.windows_auth_checkbox)
        
        # Botón de prueba de conexión
        test_button = QPushButton("Probar Conexión")
        test_button.clicked.connect(self.test_connection)
        layout.addWidget(test_button)
        
        # Botones de aceptar/cancelar
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)
        
    def toggle_windows_auth(self, checked):
        self.username_input.setEnabled(not checked)
        self.password_input.setEnabled(not checked)
        
    def test_connection(self):
        connection_string = self.get_connection_string()
        
        try:
            conn = pyodbc.connect(connection_string)
            conn.close()
            QMessageBox.information(self, "Conexión exitosa", "La conexión a la base de datos se ha establecido correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar a la base de datos:\n{str(e)}")
            
    def get_connection_string(self):
        if self.windows_auth_checkbox.isChecked():
            return f"DRIVER={{SQL Server}};SERVER={self.server_input.text()};DATABASE={self.database_input.text()};Trusted_Connection=yes;"
        else:
            return f"DRIVER={{SQL Server}};SERVER={self.server_input.text()};DATABASE={self.database_input.text()};UID={self.username_input.text()};PWD={self.password_input.text()}"
            
    def accept(self):
        self.connection_string = self.get_connection_string()
        super().accept()

class ClienteSelector(QDialog):
    """Diálogo para seleccionar un cliente"""
    
    def __init__(self, connection_string, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Cliente")
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        
        self.connection_string = connection_string
        self.cliente_controller = ClienteController(connection_string)
        self.selected_client = None
        
        self.setup_ui()
        self.load_clients()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Selección de Cliente")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Búsqueda
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Buscar:"))
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre, RFC o teléfono...")
        self.search_input.textChanged.connect(self.filter_clients)
        
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.filter_clients)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        
        layout.addLayout(search_layout)
        
        # Tabla de clientes
        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(6)
        self.clients_table.setHorizontalHeaderLabels(["ID", "Nombre", "RFC", "Teléfono", "Correo", "Tipo"])
        self.clients_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.clients_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.clients_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.clients_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.clients_table.setAlternatingRowColors(True)
        self.clients_table.doubleClicked.connect(self.accept_selection)
        
        layout.addWidget(self.clients_table)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        new_client_btn = QPushButton("Nuevo Cliente")
        new_client_btn.clicked.connect(self.new_client)
        
        select_btn = QPushButton("Seleccionar")
        select_btn.clicked.connect(self.accept_selection)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(new_client_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(select_btn)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
    def load_clients(self):
        try:
            clients = self.cliente_controller.obtener_todos_clientes()
            self.display_clients(clients)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar clientes: {str(e)}")
        
    def display_clients(self, clients):
        self.clients_table.setRowCount(0)
        
        for i, client in enumerate(clients):
            self.clients_table.insertRow(i)
            self.clients_table.setItem(i, 0, QTableWidgetItem(str(client.id_cliente)))
            self.clients_table.setItem(i, 1, QTableWidgetItem(client.nombre))
            self.clients_table.setItem(i, 2, QTableWidgetItem(client.rfc or ""))
            self.clients_table.setItem(i, 3, QTableWidgetItem(client.telefono or ""))
            self.clients_table.setItem(i, 4, QTableWidgetItem(client.correo or ""))
            self.clients_table.setItem(i, 5, QTableWidgetItem(client.tipo_cliente or ""))
            
    def filter_clients(self):
        search_text = self.search_input.text().lower()
        if search_text:
            clients = self.cliente_controller.buscar_por_nombre(search_text)
            # También buscar por RFC si parece ser un RFC
            if len(search_text) >= 10:  # RFC mínimo tiene 10 caracteres
                rfc_client = self.cliente_controller.buscar_por_rfc(search_text)
                if rfc_client and rfc_client not in clients:
                    clients.append(rfc_client)
        else:
            clients = self.cliente_controller.obtener_todos_clientes()
            
        self.display_clients(clients)
        
    def new_client(self):
        # Esta función abriría un diálogo para crear un nuevo cliente
        # Por ahora, solo mostramos un mensaje
        QMessageBox.information(self, "Información", "La funcionalidad para agregar nuevos clientes no está implementada en esta versión.")
        
    def accept_selection(self):
        selected_rows = self.clients_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selección requerida", "Por favor seleccione un cliente")
            return
            
        row = selected_rows[0].row()
        client_id = int(self.clients_table.item(row, 0).text())
        
        # Obtener el cliente completo de la base de datos
        self.selected_client = self.cliente_controller.obtener_cliente(client_id)
        
        # Verificar que se obtuvo el cliente correctamente
        if not self.selected_client:
            QMessageBox.critical(self, "Error", "No se pudo obtener la información del cliente")
            return
            
        # Verificar que el cliente tenga teléfono
        if not self.selected_client.telefono:
            QMessageBox.warning(self, "Error", "El cliente seleccionado no tiene un número de teléfono registrado")
            return
            
        self.accept()

class MaterialSelector(QDialog):
    """Diálogo para seleccionar un material"""
    
    def __init__(self, connection_string, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar Material")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        self.connection_string = connection_string
        self.material_controller = MaterialController(connection_string)
        self._conn_pm = pyodbc.connect(connection_string)
        self.proveedor_material_repo = ProveedorMaterialRepository(self._conn_pm)
        self.selected_material = None
        self.selected_proveedor_material_id = None
        self.selected_cantidad = 1.0
        
        self.setup_ui()
        self.load_materials()
        
    def __del__(self):
        if hasattr(self, '_conn_pm') and self._conn_pm:
            self._conn_pm.close()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Selección de Material")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Búsqueda
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Buscar:"))
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar material por nombre o categoría...")
        self.search_input.textChanged.connect(self.filter_materials)
        
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.filter_materials)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        
        layout.addLayout(search_layout)
        
        # Splitter para dividir materiales y proveedores
        splitter = QSplitter(Qt.Vertical)
        
        # Panel de materiales
        materials_widget = QWidget()
        materials_layout = QVBoxLayout(materials_widget)
        
        materials_label = QLabel("Materiales Disponibles")
        materials_label.setStyleSheet("font-weight: bold; border-bottom: 1px solid #cccccc; padding-bottom: 5px;")
        materials_layout.addWidget(materials_label)
        
        self.materials_table = QTableWidget()
        self.materials_table.setColumnCount(5)
        self.materials_table.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Unidad", "Categoría"])
        self.materials_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.materials_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.materials_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.materials_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.materials_table.setAlternatingRowColors(True)
        self.materials_table.selectionModel().selectionChanged.connect(self.on_material_selected)
        
        materials_layout.addWidget(self.materials_table)
        splitter.addWidget(materials_widget)
        
        # Panel de proveedores
        providers_widget = QWidget()
        providers_layout = QVBoxLayout(providers_widget)
        
        providers_label = QLabel("Proveedores Disponibles")
        providers_label.setStyleSheet("font-weight: bold; border-bottom: 1px solid #cccccc; padding-bottom: 5px;")
        providers_layout.addWidget(providers_label)
        
        self.providers_table = QTableWidget()
        self.providers_table.setColumnCount(4)
        self.providers_table.setHorizontalHeaderLabels(["ID", "Proveedor", "Precio", "Seleccionar"])
        self.providers_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.providers_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.providers_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.providers_table.setAlternatingRowColors(True)
        
        providers_layout.addWidget(self.providers_table)
        splitter.addWidget(providers_widget)
        
        layout.addWidget(splitter)
        
        # Cantidad
        quantity_group = QGroupBox("Detalles del Material")
        quantity_layout = QFormLayout()
        
        self.quantity_spin = QDoubleSpinBox()
        self.quantity_spin.setMinimum(0.01)
        self.quantity_spin.setMaximum(9999.99)
        self.quantity_spin.setValue(1.0)
        self.quantity_spin.setDecimals(2)
        self.quantity_spin.setSingleStep(0.5)
        self.quantity_spin.valueChanged.connect(self.update_cantidad)
        
        self.subtotal_label = QLabel("$0.00")
        
        quantity_layout.addRow("Cantidad:", self.quantity_spin)
        quantity_layout.addRow("Subtotal:", self.subtotal_label)
        
        quantity_group.setLayout(quantity_layout)
        layout.addWidget(quantity_group)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("Agregar Material")
        add_btn.clicked.connect(self.accept_selection)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
    def load_materials(self):
        try:
            materials = self.material_controller.obtener_todos_materiales()
            self.display_materials(materials)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar materiales: {str(e)}")
        
    def display_materials(self, materials):
        self.materials_table.setRowCount(0)
        
        for i, material in enumerate(materials):
            self.materials_table.insertRow(i)
            self.materials_table.setItem(i, 0, QTableWidgetItem(str(material.id_material)))
            self.materials_table.setItem(i, 1, QTableWidgetItem(material.nombre))
            self.materials_table.setItem(i, 2, QTableWidgetItem(material.descripcion or ""))
            self.materials_table.setItem(i, 3, QTableWidgetItem(material.unidad_medida))
            self.materials_table.setItem(i, 4, QTableWidgetItem(material.categoria or ""))
            
    def filter_materials(self):
        search_text = self.search_input.text().lower()
        if search_text:
            materials = self.material_controller.buscar_por_nombre(search_text)
        else:
            materials = self.material_controller.obtener_todos_materiales()
            
        self.display_materials(materials)
        
    def on_material_selected(self):
        selected_rows = self.materials_table.selectionModel().selectedRows()
        if not selected_rows:
            return
            
        row = selected_rows[0].row()
        material_id = int(self.materials_table.item(row, 0).text())
        self.selected_material = self.material_controller.obtener_material(material_id)
        
        # Cargar proveedores para este material
        self.load_providers(material_id)
        
    def load_providers(self, material_id):
        """Carga los proveedores disponibles para un material"""
        try:
            # Obtener proveedores del material
            providers = self.proveedor_material_repo.obtener_proveedores_de_material(material_id)
            
            # Limpiar la tabla
            self.providers_table.setRowCount(0)
            
            if not providers:
                QMessageBox.information(self, "Información", "No hay proveedores disponibles para este material")
                return
            
            # Llenar la tabla con los proveedores
            for i, provider in enumerate(providers):
                try:
                    self.providers_table.insertRow(i)
                    
                    # ID del proveedor-material
                    id_proveedor_material = provider.get('id_proveedor_material')
                    if id_proveedor_material is None:
                        print(f"Advertencia: Proveedor sin ID en la posición {i}")
                        continue
                        
                    id_item = QTableWidgetItem(str(id_proveedor_material))
                    self.providers_table.setItem(i, 0, id_item)
                    
                    # Nombre del proveedor
                    nombre = provider.get('nombre', 'Sin nombre')
                    name_item = QTableWidgetItem(nombre)
                    self.providers_table.setItem(i, 1, name_item)
                    
                    # Precio
                    try:
                        precio = float(provider.get('precio', 0))
                        price_item = QTableWidgetItem(f"${precio:.2f}")
                        price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        self.providers_table.setItem(i, 2, price_item)
                    except (ValueError, TypeError):
                        print(f"Advertencia: Precio inválido para el proveedor {nombre}")
                        price_item = QTableWidgetItem("$0.00")
                        price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        self.providers_table.setItem(i, 2, price_item)
                    
                    # Botón de selección
                    select_btn = QPushButton("Seleccionar")
                    select_btn.setProperty("row", i)
                    select_btn.clicked.connect(self.select_provider)
                    self.providers_table.setCellWidget(i, 3, select_btn)
                    
                except Exception as e:
                    print(f"Error al procesar proveedor {i}: {str(e)}")
                    continue
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar proveedores: {str(e)}")
    
    def select_provider(self):
        """Selecciona un proveedor y actualiza el subtotal"""
        sender = self.sender()
        if not sender:
            return
            
        row = sender.property("row")
        if row is None:
            return
            
        try:
            # Obtener el ID del proveedor-material
            id_proveedor_material = int(self.providers_table.item(row, 0).text())
            
            # Obtener el precio del proveedor
            price_text = self.providers_table.item(row, 2).text().replace('$', '').replace(',', '')
            price = float(price_text)
            
            # Actualizar el proveedor seleccionado
            self.selected_proveedor_material_id = id_proveedor_material
            
            # Actualizar el subtotal
            cantidad = self.quantity_spin.value()
            subtotal = price * cantidad
            self.subtotal_label.setText(f"${subtotal:.2f}")
            
            # Seleccionar la fila en la tabla
            self.providers_table.selectRow(row)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al seleccionar proveedor: {str(e)}")
    
    def update_cantidad(self, value):
        self.selected_cantidad = value
        
        # Actualizar subtotal si hay un proveedor seleccionado
        selected_rows = self.providers_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            price_text = self.providers_table.item(row, 2).text().replace('$', '')
            price = float(price_text)
            
            subtotal = price * value
            self.subtotal_label.setText(f"${subtotal:.2f}")
        
    def accept_selection(self):
        if not self.selected_material:
            QMessageBox.warning(self, "Selección requerida", "Por favor seleccione un material")
            return
            
        selected_provider_rows = self.providers_table.selectionModel().selectedRows()
        if not selected_provider_rows:
            QMessageBox.warning(self, "Selección requerida", "Por favor seleccione un proveedor")
            return
            
        provider_row = selected_provider_rows[0].row()
        self.selected_proveedor_material_id = int(self.providers_table.item(provider_row, 0).text())
        
        self.accept()

class ServiceDialog(QDialog):
    """Diálogo para agregar o editar un servicio"""
    
    def __init__(self, parent=None, service_data=None):
        super().__init__(parent)
        self.setWindowTitle("Servicio")
        self.setMinimumWidth(500)
        
        self.service_data = service_data
        self.setup_ui()
        
        # Si se proporciona data, llenar los campos
        if service_data:
            self.nombre_input.setText(service_data["nombre_servicio"])
            self.descripcion_input.setPlainText(service_data["descripcion_servicio"] or "")
            self.tipo_input.setText(service_data["tipo_servicio"] or "")
            self.costo_input.setValue(service_data["costo_servicio"])
            self.cantidad_input.setValue(service_data["cantidad_servicio"])
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Información del Servicio")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # Formulario
        form_layout = QFormLayout()
        
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del servicio")
        
        self.descripcion_input = QTextEdit()
        self.descripcion_input.setPlaceholderText("Descripción detallada del servicio")
        self.descripcion_input.setMaximumHeight(100)
        
        self.tipo_input = QLineEdit()
        self.tipo_input.setPlaceholderText("Tipo de servicio (opcional)")
        
        self.costo_input = QDoubleSpinBox()
        self.costo_input.setMinimum(0.01)
        self.costo_input.setMaximum(9999999.99)
        self.costo_input.setValue(0.00)
        self.costo_input.setPrefix("$ ")
        self.costo_input.valueChanged.connect(self.update_subtotal)
        
        self.cantidad_input = QDoubleSpinBox()
        self.cantidad_input.setMinimum(0.01)
        self.cantidad_input.setMaximum(9999.99)
        self.cantidad_input.setValue(1.00)
        self.cantidad_input.valueChanged.connect(self.update_subtotal)
        
        self.subtotal_label = QLabel("$ 0.00")
        
        form_layout.addRow("Nombre:", self.nombre_input)
        form_layout.addRow("Descripción:", self.descripcion_input)
        form_layout.addRow("Tipo:", self.tipo_input)
        form_layout.addRow("Costo unitario:", self.costo_input)
        form_layout.addRow("Cantidad:", self.cantidad_input)
        form_layout.addRow("Subtotal:", self.subtotal_label)
        
        layout.addLayout(form_layout)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("Guardar")
        save_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        # Actualizar subtotal inicial
        self.update_subtotal()
        
    def update_subtotal(self):
        costo = self.costo_input.value()
        cantidad = self.cantidad_input.value()
        subtotal = costo * cantidad
        self.subtotal_label.setText(f"$ {subtotal:.2f}")
        
    def get_service_data(self):
        return {
            "nombre_servicio": self.nombre_input.text().strip(),
            "descripcion_servicio": self.descripcion_input.toPlainText().strip() or None,
            "tipo_servicio": self.tipo_input.text().strip() or None,
            "costo_servicio": float(self.costo_input.value()),
            "cantidad_servicio": float(self.cantidad_input.value()),
            "fecha_creacion_servicio": datetime.today() if not self.service_data else self.service_data["fecha_creacion_servicio"],
            "usuario_creador_servicio": "Usuario" if not self.service_data else self.service_data["usuario_creador_servicio"],
            "activo": True,
            "fecha_actualizacion_servicio": datetime.today() if self.service_data else None
        }
        
    def accept(self):
        if not self.nombre_input.text().strip():
            QMessageBox.warning(self, "Datos incompletos", "El nombre del servicio es obligatorio")
            return
            
        super().accept()

class CotizacionGUI(QWidget):
    def __init__(self, connection_string):
        super().__init__()
        self.connection_string = connection_string

        # Pasa la cadena de conexión a los controladores y repositorios
        self.controller = CotizacionController(connection_string)
        self.cliente_controller = ClienteController(connection_string)
        self.material_controller = MaterialController(connection_string)
        self.cotizacion_material_controller = CotizacionMaterialController(connection_string)
        self.cotizacion_servicio_repo = CotizacionServicioRepository(connection_string)
        self.cotizacion_material_repo = CotizacionMaterialRepository(connection_string)

        # Variables de estado
        self.current_client = None
        self.servicios_list = []
        self.materiales_list = []
        self.selected_cotizacion_id = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gestión de Cotizaciones")
        self.setMinimumSize(1000, 700)

        # Layout principal
        main_layout = QVBoxLayout(self)

        # Crear pestañas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: white;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
        """)
        
        # Pestaña de nueva cotización
        self.nueva_cotizacion_tab = QWidget()
        self.setup_nueva_cotizacion_tab()
        self.tabs.addTab(self.nueva_cotizacion_tab, "Nueva Cotización")
        
        # Pestaña de cotizaciones existentes
        self.cotizaciones_tab = QWidget()
        self.setup_cotizaciones_tab()
        self.tabs.addTab(self.cotizaciones_tab, "Cotizaciones Existentes")
        
        main_layout.addWidget(self.tabs)

    def setup_nueva_cotizacion_tab(self):
        layout = QVBoxLayout(self.nueva_cotizacion_tab)
        
        # Scroll area para todo el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)
        
        # Título
        title_layout = QHBoxLayout()
        title_label = QLabel("Nueva Cotización")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Fecha actual
        date_label = QLabel(f"Fecha: {datetime.today().strftime('%d/%m/%Y')}")
        title_layout.addWidget(date_label)
        
        scroll_layout.addLayout(title_layout)
        
        # Sección de cliente
        client_group = QGroupBox("Información del Cliente")
        client_layout = QVBoxLayout()
        
        # Datos del cliente
        client_form = QFormLayout()
        
        self.client_id_input = QLineEdit()
        self.client_id_input.setReadOnly(True)
        
        self.client_name_input = QLineEdit()
        self.client_name_input.setReadOnly(True)
        
        self.client_rfc_input = QLineEdit()
        self.client_rfc_input.setReadOnly(True)
        
        self.client_phone_input = QLineEdit()
        self.client_phone_input.setReadOnly(True)
        
        self.client_email_input = QLineEdit()
        self.client_email_input.setReadOnly(True)
        
        client_form.addRow("ID:", self.client_id_input)
        client_form.addRow("Nombre:", self.client_name_input)
        client_form.addRow("RFC:", self.client_rfc_input)
        client_form.addRow("Teléfono:", self.client_phone_input)
        client_form.addRow("Correo:", self.client_email_input)
        
        client_layout.addLayout(client_form)
        
        # Botón de selección de cliente
        select_client_btn = QPushButton("Seleccionar Cliente")
        select_client_btn.clicked.connect(self.select_client)
        client_layout.addWidget(select_client_btn)
        
        client_group.setLayout(client_layout)
        scroll_layout.addWidget(client_group)
        
        # Sección de datos de cotización
        cotizacion_group = QGroupBox("Datos de la Cotización")
        cotizacion_layout = QFormLayout()
        
        self.fecha_creacion_input = QLineEdit()
        self.fecha_creacion_input.setText(datetime.today().strftime('%Y-%m-%d'))
        self.fecha_creacion_input.setReadOnly(True)
        
        self.fecha_activacion_input = QLineEdit()
        self.fecha_activacion_input.setText(datetime.today().strftime('%Y-%m-%d'))
        
        self.observaciones_input = QTextEdit()
        self.observaciones_input.setMaximumHeight(80)
        self.observaciones_input.setPlaceholderText("Observaciones o notas adicionales...")
        
        self.usuario_creador_input = QLineEdit()
        self.usuario_creador_input.setText(os.getenv('USERNAME', 'Usuario'))
        
        cotizacion_layout.addRow("Fecha Creación:", self.fecha_creacion_input)
        cotizacion_layout.addRow("Fecha Activación:", self.fecha_activacion_input)
        cotizacion_layout.addRow("Observaciones:", self.observaciones_input)
        cotizacion_layout.addRow("Usuario Creador:", self.usuario_creador_input)
        
        cotizacion_group.setLayout(cotizacion_layout)
        scroll_layout.addWidget(cotizacion_group)
        
        # Sección de servicios
        servicios_group = QGroupBox("Servicios (Mano de Obra)")
        servicios_layout = QVBoxLayout()
        
        # Tabla de servicios
        self.servicios_table = QTableWidget()
        self.servicios_table.setColumnCount(7)
        self.servicios_table.setHorizontalHeaderLabels(["#", "Nombre", "Descripción", "Tipo", "Costo", "Cantidad", "Subtotal"])
        self.servicios_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.servicios_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.servicios_table.setAlternatingRowColors(True)
        self.servicios_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        servicios_layout.addWidget(self.servicios_table)
        
        # Botones para servicios
        servicios_buttons_layout = QHBoxLayout()
        
        add_service_btn = QPushButton("Agregar Servicio")
        add_service_btn.clicked.connect(self.add_service)
        
        edit_service_btn = QPushButton("Editar Servicio")
        edit_service_btn.clicked.connect(self.edit_service)
        
        remove_service_btn = QPushButton("Eliminar Servicio")
        remove_service_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        remove_service_btn.clicked.connect(self.remove_service)
        
        servicios_buttons_layout.addWidget(add_service_btn)
        servicios_buttons_layout.addWidget(edit_service_btn)
        servicios_buttons_layout.addWidget(remove_service_btn)
        servicios_buttons_layout.addStretch()
        
        servicios_layout.addLayout(servicios_buttons_layout)
        
        servicios_group.setLayout(servicios_layout)
        scroll_layout.addWidget(servicios_group)
        
        # Sección de materiales
        materiales_group = QGroupBox("Materiales")
        materiales_layout = QVBoxLayout()
        
        # Tabla de materiales
        self.materiales_table = QTableWidget()
        self.materiales_table.setColumnCount(7)
        self.materiales_table.setHorizontalHeaderLabels(["#", "Nombre", "Proveedor", "Unidad", "Cantidad", "Precio", "Subtotal"])
        self.materiales_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.materiales_table.setAlternatingRowColors(True)
        self.materiales_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        materiales_layout.addWidget(self.materiales_table)
        
        # Botones para materiales
        materiales_buttons_layout = QHBoxLayout()
        
        add_material_btn = QPushButton("Agregar Material")
        add_material_btn.clicked.connect(self.add_material)
        
        edit_material_btn = QPushButton("Editar Cantidad")
        edit_material_btn.clicked.connect(self.edit_material)
        
        remove_material_btn = QPushButton("Eliminar Material")
        remove_material_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        remove_material_btn.clicked.connect(self.remove_material)
        
        materiales_buttons_layout.addWidget(add_material_btn)
        materiales_buttons_layout.addWidget(edit_material_btn)
        materiales_buttons_layout.addWidget(remove_material_btn)
        materiales_buttons_layout.addStretch()
        
        materiales_layout.addLayout(materiales_buttons_layout)
        
        materiales_group.setLayout(materiales_layout)
        scroll_layout.addWidget(materiales_group)
        
        # Sección de resumen
        resumen_group = QGroupBox("Resumen Financiero")
        resumen_layout = QFormLayout()
        
        self.total_servicios_label = QLabel("$0.00")
        self.iva_servicios_label = QLabel("$0.00")
        self.total_servicios_iva_label = QLabel("$0.00")
        self.total_materiales_label = QLabel("$0.00")
        self.gran_total_label = QLabel("$0.00")
        
        font = QFont()
        font.setBold(True)
        self.gran_total_label.setFont(font)
        
        resumen_layout.addRow("Total Servicios (sin IVA):", self.total_servicios_label)
        resumen_layout.addRow("IVA 16% Servicios:", self.iva_servicios_label)
        resumen_layout.addRow("Total Servicios (con IVA):", self.total_servicios_iva_label)
        resumen_layout.addRow("Total Materiales:", self.total_materiales_label)
        resumen_layout.addRow("GRAN TOTAL:", self.gran_total_label)
        
        resumen_group.setLayout(resumen_layout)
        scroll_layout.addWidget(resumen_group)
        
        # Botones de acción
        actions_layout = QHBoxLayout()
        
        save_btn = QPushButton("Guardar Cotización")
        save_btn.clicked.connect(self.save_cotizacion)
        
        preview_btn = QPushButton("Vista Previa")
        preview_btn.clicked.connect(self.preview_cotizacion)
        
        clear_btn = QPushButton("Limpiar Formulario")
        clear_btn.clicked.connect(self.clear_form)
        
        actions_layout.addStretch()
        actions_layout.addWidget(preview_btn)
        actions_layout.addWidget(save_btn)
        actions_layout.addWidget(clear_btn)
        
        scroll_layout.addLayout(actions_layout)
        
        # Finalizar scroll area
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
    
    def setup_cotizaciones_tab(self):
        layout = QVBoxLayout(self.cotizaciones_tab)
        
        # Título
        title_layout = QHBoxLayout()
        title_label = QLabel("Cotizaciones Existentes")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Botón de actualizar
        refresh_btn = QPushButton("Actualizar")
        refresh_btn.clicked.connect(self.load_cotizaciones)
        title_layout.addWidget(refresh_btn)
        
        layout.addLayout(title_layout)
        
        # Filtros
        filter_group = QGroupBox("Filtros de Búsqueda")
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Buscar:"))
        self.search_cotizacion_input = QLineEdit()
        self.search_cotizacion_input.setPlaceholderText("Buscar por cliente o ID...")
        self.search_cotizacion_input.textChanged.connect(self.filter_cotizaciones)
        filter_layout.addWidget(self.search_cotizacion_input)
        
        filter_layout.addWidget(QLabel("Estado:"))
        self.estado_filter = QComboBox()
        self.estado_filter.addItems(["Todas", "Activas", "Canceladas", "Finalizadas"])
        self.estado_filter.currentIndexChanged.connect(self.filter_cotizaciones)
        filter_layout.addWidget(self.estado_filter)
        
        filter_layout.addWidget(QLabel("Fecha:"))
        self.fecha_desde = QLineEdit()
        self.fecha_desde.setPlaceholderText("Desde (YYYY-MM-DD)")
        filter_layout.addWidget(self.fecha_desde)
        
        self.fecha_hasta = QLineEdit()
        self.fecha_hasta.setPlaceholderText("Hasta (YYYY-MM-DD)")
        filter_layout.addWidget(self.fecha_hasta)
        
        apply_filter_btn = QPushButton("Aplicar")
        apply_filter_btn.clicked.connect(self.filter_cotizaciones)
        filter_layout.addWidget(apply_filter_btn)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        # Tabla de cotizaciones
        self.cotizaciones_table = QTableWidget()
        self.cotizaciones_table.setColumnCount(7)
        self.cotizaciones_table.setHorizontalHeaderLabels(["ID", "Cliente", "Fecha", "Usuario", "Estado", "Total", "Acciones"])
        self.cotizaciones_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cotizaciones_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.cotizaciones_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cotizaciones_table.setAlternatingRowColors(True)
        self.cotizaciones_table.doubleClicked.connect(self.view_cotizacion_details)
        
        layout.addWidget(self.cotizaciones_table)
        
        # Botones de acción
        actions_layout = QHBoxLayout()
        
        view_btn = QPushButton("Ver Detalles")
        view_btn.clicked.connect(self.view_cotizacion_details)
        
        print_btn = QPushButton("Imprimir")
        print_btn.clicked.connect(self.print_cotizacion)
        
        export_btn = QPushButton("Exportar")
        export_btn.clicked.connect(self.export_cotizacion)
        
        cancel_btn = QPushButton("Cancelar Cotización")
        cancel_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        cancel_btn.clicked.connect(self.cancel_cotizacion)
        
        actions_layout.addStretch()
        actions_layout.addWidget(view_btn)
        actions_layout.addWidget(print_btn)
        actions_layout.addWidget(export_btn)
        actions_layout.addWidget(cancel_btn)
        
        layout.addLayout(actions_layout)
        
        # Cargar cotizaciones al iniciar
        self.load_cotizaciones()
    
    def select_client(self):
        """Abre el diálogo para seleccionar un cliente"""
        try:
            dialog = ClienteSelector(self.connection_string, self)
            if dialog.exec_():
                self.current_client = dialog.selected_client
                if self.current_client:
                    self.update_client_info()
                else:
                    QMessageBox.warning(self, "Error", "No se pudo obtener la información del cliente seleccionado")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al seleccionar cliente: {str(e)}")
            
    def update_client_info(self):
        """Actualiza la información del cliente en el formulario"""
        if self.current_client:
            self.client_id_input.setText(str(self.current_client.id_cliente))
            self.client_name_input.setText(self.current_client.nombre)
            self.client_rfc_input.setText(self.current_client.rfc or "")
            self.client_phone_input.setText(self.current_client.telefono or "")
            self.client_email_input.setText(self.current_client.correo or "")
    
    def add_service(self):
        """Abre el diálogo para agregar un servicio"""
        if not self.current_client:
            QMessageBox.warning(self, "Cliente requerido", "Debe seleccionar un cliente antes de agregar servicios")
            return
            
        dialog = ServiceDialog(self)
        if dialog.exec_():
            service_data = dialog.get_service_data()
            if service_data:
                self.servicios_list.append(service_data)
                self.update_servicios_table()
                self.update_totals()
            else:
                QMessageBox.warning(self, "Error", "No se pudo obtener la información del servicio")
                
    def edit_service(self):
        """Abre el diálogo para editar un servicio existente"""
        selected_rows = self.servicios_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selección requerida", "Por favor seleccione un servicio para editar")
            return
            
        row = selected_rows[0].row()
        service_data = self.servicios_list[row]
        
        dialog = ServiceDialog(self, service_data)
        if dialog.exec_():
            self.servicios_list[row] = dialog.get_service_data()
            self.update_servicios_table()
            self.update_totals()
    
    def update_servicios_table(self):
        """Actualiza la tabla de servicios"""
        self.servicios_table.setRowCount(0)
        
        for i, servicio in enumerate(self.servicios_list):
            self.servicios_table.insertRow(i)
            
            # Número de fila
            num_item = QTableWidgetItem(str(i + 1))
            num_item.setTextAlignment(Qt.AlignCenter)
            self.servicios_table.setItem(i, 0, num_item)
            
            # Datos del servicio
            self.servicios_table.setItem(i, 1, QTableWidgetItem(servicio["nombre_servicio"]))
            self.servicios_table.setItem(i, 2, QTableWidgetItem(servicio["descripcion_servicio"] or ""))
            self.servicios_table.setItem(i, 3, QTableWidgetItem(servicio["tipo_servicio"] or ""))
            
            costo = QTableWidgetItem(f"${servicio['costo_servicio']:.2f}")
            costo.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.servicios_table.setItem(i, 4, costo)
            
            cantidad = QTableWidgetItem(str(servicio["cantidad_servicio"]))
            cantidad.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.servicios_table.setItem(i, 5, cantidad)
            
            subtotal = servicio["costo_servicio"] * servicio["cantidad_servicio"]
            subtotal_item = QTableWidgetItem(f"${subtotal:.2f}")
            subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.servicios_table.setItem(i, 6, subtotal_item)
    
    def remove_service(self):
        """Elimina un servicio de la lista"""
        selected_rows = self.servicios_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selección requerida", "Por favor seleccione un servicio para eliminar")
            return
            
        row = selected_rows[0].row()
        
        confirm = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Está seguro de eliminar el servicio '{self.servicios_list[row]['nombre_servicio']}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self.servicios_list.pop(row)
            self.update_servicios_table()
            self.update_totals()
    
    def add_material(self):
        """Abre el diálogo para agregar un material"""
        if not self.current_client:
            QMessageBox.warning(self, "Cliente requerido", "Debe seleccionar un cliente antes de agregar materiales")
            return
            
        try:
            dialog = MaterialSelector(self.connection_string, self)
            if dialog.exec_():
                material = dialog.selected_material
                proveedor_material_id = dialog.selected_proveedor_material_id
                cantidad = dialog.selected_cantidad
                
                if not material or not proveedor_material_id:
                    QMessageBox.warning(self, "Error", "No se pudo obtener la información del material")
                    return
                    
                # Obtener el vínculo proveedor-material para obtener el precio
                proveedor_material = dialog.proveedor_material_repo.obtener_vinculo(proveedor_material_id)
                
                if not proveedor_material:
                    QMessageBox.warning(self, "Error", "No se pudo obtener la información del proveedor-material")
                    return
                    
                # Obtener el nombre del proveedor
                providers = dialog.proveedor_material_repo.obtener_proveedores_de_material(material.id_material)
                proveedor_nombre = ""
                
                for provider in providers:
                    if provider['id_proveedor_material'] == proveedor_material_id:
                        proveedor_nombre = provider['nombre']
                        break
                        
                material_info = {
                    "id_material": material.id_material,
                    "nombre_material": material.nombre,
                    "unidad_medida": material.unidad_medida,
                    "id_proveedor_material": proveedor_material_id,
                    "nombre_proveedor": proveedor_nombre,
                    "precio": float(proveedor_material.precio),
                    "cantidad": cantidad
                }
                
                self.materiales_list.append(material_info)
                self.update_materiales_table()
                self.update_totals()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar material: {str(e)}")
    
    def edit_material(self):
        """Edita la cantidad de un material existente"""
        selected_rows = self.materiales_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selección requerida", "Por favor seleccione un material para editar")
            return
            
        row = selected_rows[0].row()
        material = self.materiales_list[row]
        
        # Crear un diálogo para editar la cantidad
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Editar Cantidad - {material['nombre_material']}")
        dialog.setMinimumWidth(300)
        
        layout = QVBoxLayout(dialog)
        
        form_layout = QFormLayout()
        
        cantidad_spin = QDoubleSpinBox()
        cantidad_spin.setMinimum(0.01)
        cantidad_spin.setMaximum(9999.99)
        cantidad_spin.setValue(material['cantidad'])
        cantidad_spin.setDecimals(2)
        
        form_layout.addRow("Nueva cantidad:", cantidad_spin)
        
        layout.addLayout(form_layout)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        layout.addWidget(buttons)
        
        if dialog.exec_():
            material['cantidad'] = cantidad_spin.value()
            self.update_materiales_table()
            self.update_totals()
    
    def update_materiales_table(self):
        """Actualiza la tabla de materiales"""
        self.materiales_table.setRowCount(0)
        
        for i, material in enumerate(self.materiales_list):
            self.materiales_table.insertRow(i)
            
            # Número de fila
            num_item = QTableWidgetItem(str(i + 1))
            num_item.setTextAlignment(Qt.AlignCenter)
            self.materiales_table.setItem(i, 0, num_item)
            
            # Datos del material
            self.materiales_table.setItem(i, 1, QTableWidgetItem(material["nombre_material"]))
            self.materiales_table.setItem(i, 2, QTableWidgetItem(material["nombre_proveedor"]))
            self.materiales_table.setItem(i, 3, QTableWidgetItem(material["unidad_medida"]))
            
            cantidad = QTableWidgetItem(str(material["cantidad"]))
            cantidad.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.materiales_table.setItem(i, 4, cantidad)
            
            precio = QTableWidgetItem(f"${material['precio']:.2f}")
            precio.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.materiales_table.setItem(i, 5, precio)
            
            subtotal = material["precio"] * material["cantidad"]
            subtotal_item = QTableWidgetItem(f"${subtotal:.2f}")
            subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.materiales_table.setItem(i, 6, subtotal_item)
    
    def remove_material(self):
        """Elimina un material de la lista"""
        selected_rows = self.materiales_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selección requerida", "Por favor seleccione un material para eliminar")
            return
            
        row = selected_rows[0].row()
        
        confirm = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Está seguro de eliminar el material '{self.materiales_list[row]['nombre_material']}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self.materiales_list.pop(row)
            self.update_materiales_table()
            self.update_totals()
    
    def update_totals(self):
        """Actualiza los totales de la cotización"""
        try:
            # Calcular subtotal de servicios
            servicios_subtotal = sum(
                servicio["costo_servicio"] * servicio["cantidad_servicio"] 
                for servicio in self.servicios_list
            )
            
            # Calcular subtotal de materiales
            materiales_subtotal = sum(
                material["precio"] * material["cantidad"] 
                for material in self.materiales_list
            )
            
            # Calcular IVA de servicios (16%)
            iva_servicios = servicios_subtotal * 0.16
            
            # Calcular total con IVA
            total_servicios_iva = servicios_subtotal + iva_servicios
            
            # Calcular gran total
            gran_total = total_servicios_iva + materiales_subtotal
            
            # Actualizar etiquetas
            self.total_servicios_label.setText(f"${servicios_subtotal:,.2f}")
            self.iva_servicios_label.setText(f"${iva_servicios:,.2f}")
            self.total_servicios_iva_label.setText(f"${total_servicios_iva:,.2f}")
            self.total_materiales_label.setText(f"${materiales_subtotal:,.2f}")
            self.gran_total_label.setText(f"${gran_total:,.2f}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar totales: {str(e)}")
    
    def save_cotizacion(self):
        """Guarda la cotización en la base de datos"""
        try:
            if not self.current_client:
                QMessageBox.warning(self, "Error", "Debe seleccionar un cliente antes de guardar la cotización")
                return
                
            if not self.servicios_list and not self.materiales_list:
                QMessageBox.warning(self, "Error", "Debe agregar al menos un servicio o material antes de guardar la cotización")
                return
                
            # Verificar que el cliente tenga RFC
            if not self.current_client.rfc:
                QMessageBox.warning(self, "Error", "El cliente seleccionado debe tener un RFC válido")
                return
                
            # Verificar que el cliente tenga correo
            if not self.current_client.correo:
                QMessageBox.warning(self, "Error", "El cliente seleccionado debe tener un correo electrónico válido")
                return
                
            # Manejar el teléfono de manera explícita
            telefono_cliente = self.current_client.telefono
            if not telefono_cliente:
                telefono_cliente = "SIN TELÉFONO"
                
            # Manejar el tipo de cliente de manera explícita
            tipo_cliente = self.current_client.tipo_cliente
            if not tipo_cliente:
                tipo_cliente = "NO ESPECIFICADO"
                
            # Obtener los datos de la cotización
            cotizacion_data = {
                "id_cliente": self.current_client.id_cliente,
                "nombre_cliente": self.current_client.nombre,
                "rfc_cliente": self.current_client.rfc,
                "correo_cliente": self.current_client.correo,
                # Teléfono nunca debe ser None ni vacío
                "telefono_cliente": self.current_client.telefono if self.current_client.telefono else "SIN TELÉFONO",
                "tipo_cliente": tipo_cliente,
                "fecha_creacion": datetime.strptime(self.fecha_creacion_input.text(), '%Y-%m-%d'),
                "fecha_activacion": datetime.strptime(self.fecha_activacion_input.text(), '%Y-%m-%d'),
                "observaciones": self.observaciones_input.toPlainText(),
                "usuario_creador": self.usuario_creador_input.text(),
                "estado": "Activa"
            }
            
            # Imprimir los datos para depuración
            print("Datos de la cotización:", cotizacion_data)
            
            # Guardar la cotización
            cotizacion = self.controller.crear_cotizacion(cotizacion_data)
            
            if not cotizacion:
                QMessageBox.critical(self, "Error", "No se pudo guardar la cotización")
                return
                
            # Obtener el ID de la cotización
            cotizacion_id = cotizacion.id_cotizacion
                
            # Guardar los servicios
            for servicio in self.servicios_list:
                servicio_obj = CotizacionServicio(
                    id_cotizacion=int(cotizacion_id),  # Convertimos explícitamente a entero
                    nombre_servicio=servicio["nombre_servicio"],
                    descripcion_servicio=servicio["descripcion_servicio"],
                    tipo_servicio=servicio["tipo_servicio"],
                    costo_servicio=servicio["costo_servicio"],
                    cantidad_servicio=servicio["cantidad_servicio"],
                    fecha_creacion_servicio=datetime.now(),
                    usuario_creador_servicio=self.usuario_creador_input.text(),
                    activo=True
                )
                if not self.cotizacion_servicio_repo.create_cotizacion_servicio(servicio_obj):
                    QMessageBox.warning(self, "Error", f"No se pudo guardar el servicio: {servicio['nombre_servicio']}")
                    
            # Guardar los materiales
            for material in self.materiales_list:
                if not self.cotizacion_material_repo.agregar_material(
                    id_cotizacion=cotizacion_id,
                    id_proveedor_material=material["id_proveedor_material"],
                    cantidad=material["cantidad"]
                ):
                    QMessageBox.warning(self, "Error", f"No se pudo guardar el material: {material['nombre_material']}")
                    
            QMessageBox.information(self, "Éxito", "Cotización guardada correctamente")
            self.clear_form()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar la cotización: {str(e)}")
    
    def preview_cotizacion(self):
        """Muestra una vista previa de la cotización"""
        if not self.current_client:
            QMessageBox.warning(self, "Datos incompletos", "Debe seleccionar un cliente")
            return
            
        if not self.servicios_list:
            QMessageBox.warning(self, "Datos incompletos", "Debe agregar al menos un servicio")
            return
            
        # Crear diálogo para mostrar vista previa
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle("Vista Previa de Cotización")
        preview_dialog.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(preview_dialog)
        
        # Scroll area para todo el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Título
        title_layout = QHBoxLayout()
        title_label = QLabel("COTIZACIÓN")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Fecha
        date_label = QLabel(f"Fecha: {self.fecha_creacion_input.text()}")
        title_layout.addWidget(date_label)
        
        scroll_layout.addLayout(title_layout)
        
        # Datos del cliente
        client_group = QGroupBox("Datos del Cliente")
        client_layout = QFormLayout()
        
        client_layout.addRow("Nombre:", QLabel(self.current_client.nombre))
        client_layout.addRow("RFC:", QLabel(self.current_client.rfc or ""))
        client_layout.addRow("Teléfono:", QLabel(self.current_client.telefono or ""))
        client_layout.addRow("Correo:", QLabel(self.current_client.correo or ""))
        client_layout.addRow("Tipo:", QLabel(self.current_client.tipo_cliente or ""))
        
        client_group.setLayout(client_layout)
        scroll_layout.addWidget(client_group)
        
        # Datos de la cotización
        cotizacion_group = QGroupBox("Datos de la Cotización")
        cotizacion_layout = QFormLayout()
        
        cotizacion_layout.addRow("Fecha Creación:", QLabel(self.fecha_creacion_input.text()))
        cotizacion_layout.addRow("Fecha Activación:", QLabel(self.fecha_activacion_input.text()))
        cotizacion_layout.addRow("Observaciones:", QLabel(self.observaciones_input.toPlainText() or ""))
        cotizacion_layout.addRow("Usuario Creador:", QLabel(self.usuario_creador_input.text()))
        
        cotizacion_group.setLayout(cotizacion_layout)
        scroll_layout.addWidget(cotizacion_group)
        
        # Servicios
        servicios_group = QGroupBox("Servicios")
        servicios_layout = QVBoxLayout()
        
        servicios_table = QTableWidget()
        servicios_table.setColumnCount(6)
        servicios_table.setHorizontalHeaderLabels(["Nombre", "Descripción", "Tipo", "Costo", "Cantidad", "Subtotal"])
        servicios_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        servicios_table.setEditTriggers(QTableWidget.NoEditTriggers)
        servicios_table.setAlternatingRowColors(True)
        
        total_servicios = 0
        
        for i, servicio in enumerate(self.servicios_list):
            servicios_table.insertRow(i)
            
            servicios_table.setItem(i, 0, QTableWidgetItem(servicio["nombre_servicio"]))
            servicios_table.setItem(i, 1, QTableWidgetItem(servicio["descripcion_servicio"] or ""))
            servicios_table.setItem(i, 2, QTableWidgetItem(servicio["tipo_servicio"] or ""))
            
            costo = QTableWidgetItem(f"${servicio['costo_servicio']:.2f}")
            costo.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            servicios_table.setItem(i, 3, costo)
            
            cantidad = servicio["cantidad_servicio"]
            cantidad_item = QTableWidgetItem(str(cantidad))
            cantidad_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            servicios_table.setItem(i, 4, cantidad_item)
            
            subtotal = servicio["costo_servicio"] * cantidad
            total_servicios += subtotal
            
            subtotal_item = QTableWidgetItem(f"${subtotal:.2f}")
            subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            servicios_table.setItem(i, 5, subtotal_item)
            
        servicios_layout.addWidget(servicios_table)
        servicios_group.setLayout(servicios_layout)
        scroll_layout.addWidget(servicios_group)
        
        # Materiales
        materiales_group = QGroupBox("Materiales")
        materiales_layout = QVBoxLayout()
        
        materiales_table = QTableWidget()
        materiales_table.setColumnCount(6)
        materiales_table.setHorizontalHeaderLabels(["Nombre", "Proveedor", "Unidad", "Cantidad", "Precio", "Subtotal"])
        materiales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        materiales_table.setEditTriggers(QTableWidget.NoEditTriggers)
        materiales_table.setAlternatingRowColors(True)
        
        total_materiales = 0
        
        for i, material in enumerate(self.materiales_list):
            materiales_table.insertRow(i)
            
            materiales_table.setItem(i, 0, QTableWidgetItem(material["nombre_material"]))
            materiales_table.setItem(i, 1, QTableWidgetItem(material["nombre_proveedor"]))
            materiales_table.setItem(i, 2, QTableWidgetItem(material["unidad_medida"]))
            
            cantidad = QTableWidgetItem(str(material["cantidad"]))
            cantidad.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            materiales_table.setItem(i, 3, cantidad)
            
            precio = QTableWidgetItem(f"${material['precio']:.2f}")
            precio.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            materiales_table.setItem(i, 4, precio)
            
            subtotal = material["precio"] * material["cantidad"]
            total_materiales += subtotal
            
            subtotal_item = QTableWidgetItem(f"${subtotal:.2f}")
            subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            materiales_table.setItem(i, 5, subtotal_item)
            
        materiales_layout.addWidget(materiales_table)
        materiales_group.setLayout(materiales_layout)
        scroll_layout.addWidget(materiales_group)
        
        # Resumen
        resumen_group = QGroupBox("Resumen")
        resumen_layout = QFormLayout()
        
        iva_servicios = total_servicios * 0.16
        total_servicios_iva = total_servicios + iva_servicios
        gran_total = total_servicios_iva + total_materiales
        
        total_servicios_label = QLabel(f"${total_servicios:.2f}")
        iva_servicios_label = QLabel(f"${iva_servicios:.2f}")
        total_servicios_iva_label = QLabel(f"${total_servicios_iva:.2f}")
        total_materiales_label = QLabel(f"${total_materiales:.2f}")
        gran_total_label = QLabel(f"${gran_total:.2f}")
        
        font = QFont()
        font.setBold(True)
        gran_total_label.setFont(font)
        
        resumen_layout.addRow("Total Servicios (sin IVA):", total_servicios_label)
        resumen_layout.addRow("IVA 16% Servicios:", iva_servicios_label)
        resumen_layout.addRow("Total Servicios (con IVA):", total_servicios_iva_label)
        resumen_layout.addRow("Total Materiales:", total_materiales_label)
        resumen_layout.addRow("GRAN TOTAL:", gran_total_label)
        
        resumen_group.setLayout(resumen_layout)
        scroll_layout.addWidget(resumen_group)
        
        # Finalizar scroll area
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(preview_dialog.reject)
        
        layout.addWidget(buttons)
        
        preview_dialog.exec_()
    
    def clear_form(self):
        """Limpia el formulario de cotización"""
        # Limpiar cliente
        self.current_client = None
        self.client_id_input.clear()
        self.client_name_input.clear()
        self.client_rfc_input.clear()
        self.client_phone_input.clear()
        self.client_email_input.clear()
        
        # Limpiar datos de cotización
        self.fecha_creacion_input.setText(datetime.today().strftime('%Y-%m-%d'))
        self.fecha_activacion_input.setText(datetime.today().strftime('%Y-%m-%d'))
        self.observaciones_input.clear()
        
        # Limpiar servicios y materiales
        self.servicios_list = []
        self.materiales_list = []
        self.update_servicios_table()
        self.update_materiales_table()
        
        # Limpiar totales
        self.update_totals()
    
    def load_cotizaciones(self):
        """Carga las cotizaciones existentes en la tabla"""
        try:
            cotizaciones = self.controller.obtener_todas_cotizaciones(activas_only=False)
            self.display_cotizaciones(cotizaciones)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar cotizaciones: {str(e)}")
    
    def display_cotizaciones(self, cotizaciones):
        """Muestra las cotizaciones en la tabla"""
        self.cotizaciones_table.setRowCount(0)
        
        for i, cotizacion in enumerate(cotizaciones):
            self.cotizaciones_table.insertRow(i)
            
            # Determinar estado
            estado = "Activa"
            if cotizacion.fecha_cancelacion:
                estado = "Cancelada"
            elif cotizacion.fecha_finalizacion:
                estado = "Finalizada"
                
            # Obtener detalles para calcular el total
            detalles = self.controller.obtener_detalles_cotizacion(cotizacion.id_cotizacion)
            total = 0
            
            if detalles:
                # Calcular total de servicios con IVA
                if detalles["servicios"]:
                    total_servicios = sum(
                        servicio.costo_servicio * (servicio.cantidad_servicio or 1)
                        for servicio in detalles["servicios"]
                    )
                    total += total_servicios * 1.16  # Agregar IVA
                
                # Calcular total de materiales
                if detalles["materiales"]:
                    for material in detalles["materiales"]:
                        if "precio_unitario" in material and "cantidad" in material:
                            total += float(material["precio_unitario"]) * float(material["cantidad"])
            
            # ID
            id_item = QTableWidgetItem(str(cotizacion.id_cotizacion))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.cotizaciones_table.setItem(i, 0, id_item)
            
            # Cliente
            self.cotizaciones_table.setItem(i, 1, QTableWidgetItem(cotizacion.nombre_cliente))
            
            # Fecha
            fecha = cotizacion.fecha_creacion.strftime('%Y-%m-%d') if cotizacion.fecha_creacion else ""
            self.cotizaciones_table.setItem(i, 2, QTableWidgetItem(fecha))
            
            # Usuario
            self.cotizaciones_table.setItem(i, 3, QTableWidgetItem(cotizacion.usuario_creador or ""))
            
            # Estado
            estado_item = QTableWidgetItem(estado)
            if estado == "Activa":
                estado_item.setForeground(QColor("#2ecc71"))  # Verde
            elif estado == "Cancelada":
                estado_item.setForeground(QColor("#e74c3c"))  # Rojo
            self.cotizaciones_table.setItem(i, 4, estado_item)
            
            # Total
            total_item = QTableWidgetItem(f"${total:.2f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cotizaciones_table.setItem(i, 5, total_item)
            
            # Botones de acción
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            view_btn = QPushButton()
            view_btn.setText("Ver")
            view_btn.setToolTip("Ver detalles")
            view_btn.setProperty("id_cotizacion", cotizacion.id_cotizacion)
            view_btn.clicked.connect(lambda _, id=cotizacion.id_cotizacion: self.view_cotizacion_details(id))
            
            print_btn = QPushButton()
            print_btn.setText("PDF")
            print_btn.setToolTip("Generar PDF")
            print_btn.setProperty("id_cotizacion", cotizacion.id_cotizacion)
            print_btn.clicked.connect(lambda _, id=cotizacion.id_cotizacion: self.print_cotizacion(id))
            
            actions_layout.addWidget(view_btn)
            actions_layout.addWidget(print_btn)
            
            self.cotizaciones_table.setCellWidget(i, 6, actions_widget)
    
    def filter_cotizaciones(self):
        """Filtra las cotizaciones según los criterios seleccionados"""
        search_text = self.search_cotizacion_input.text().lower()
        estado_filter = self.estado_filter.currentText()
        
        try:
            cotizaciones = self.controller.obtener_todas_cotizaciones(activas_only=False)
            filtered_cotizaciones = []
            
            for cotizacion in cotizaciones:
                # Filtrar por texto de búsqueda
                if search_text:
                    if (search_text not in cotizacion.nombre_cliente.lower() and
                        search_text not in str(cotizacion.id_cotizacion)):
                        continue
                        
                # Filtrar por estado
                if estado_filter != "Todas":
                    estado_actual = "Activa"
                    if cotizacion.fecha_cancelacion:
                        estado_actual = "Cancelada"
                    elif cotizacion.fecha_finalizacion:
                        estado_actual = "Finalizada"
                        
                    if estado_filter != estado_actual:
                        continue
                        
                # Filtrar por fecha
                if self.fecha_desde.text() and self.fecha_hasta.text():
                    try:
                        fecha_desde = datetime.strptime(self.fecha_desde.text(), '%Y-%m-%d')
                        fecha_hasta = datetime.strptime(self.fecha_hasta.text(), '%Y-%m-%d')
                        
                        if not (fecha_desde <= cotizacion.fecha_creacion <= fecha_hasta):
                            continue
                    except ValueError:
                        # Si hay error en el formato de fecha, ignorar este filtro
                        pass
                        
                filtered_cotizaciones.append(cotizacion)
                
            self.display_cotizaciones(filtered_cotizaciones)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al filtrar cotizaciones: {str(e)}")
    
    def view_cotizacion_details(self, id_cotizacion=None):
        """Muestra los detalles de una cotización"""
        if id_cotizacion is None:
            selected_rows = self.cotizaciones_table.selectionModel().selectedRows()
            if not selected_rows:
                QMessageBox.warning(self, "Selección requerida", "Por favor seleccione una cotización para ver detalles")
                return
                
            row = selected_rows[0].row()
            id_cotizacion = int(self.cotizaciones_table.item(row, 0).text())
        
        try:
            # Obtener detalles de la cotización
            detalles = self.controller.obtener_detalles_cotizacion(id_cotizacion)
            if not detalles:
                QMessageBox.warning(self, "Error", "No se pudieron obtener los detalles de la cotización")
                return
                
            # Crear diálogo para mostrar detalles
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Detalles de Cotización #{id_cotizacion}")
            dialog.setMinimumSize(800, 600)
            
            layout = QVBoxLayout(dialog)
            
            # Scroll area para todo el contenido
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            
            # Título
            title_layout = QHBoxLayout()
            title_label = QLabel(f"COTIZACIÓN #{id_cotizacion}")
            title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
            title_layout.addWidget(title_label)
            title_layout.addStretch()
            
            # Estado
            estado = "Activa"
            if detalles["cotizacion"].fecha_cancelacion:
                estado = "Cancelada"
            elif detalles["cotizacion"].fecha_finalizacion:
                estado = "Finalizada"
                
            estado_label = QLabel(f"Estado: {estado}")
            if estado == "Activa":
                estado_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
            elif estado == "Cancelada":
                estado_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
                
            title_layout.addWidget(estado_label)
            
            scroll_layout.addLayout(title_layout)
            
            # Datos del cliente
            client_group = QGroupBox("Datos del Cliente")
            client_layout = QFormLayout()
            
            client_layout.addRow("Nombre:", QLabel(detalles["cotizacion"].nombre_cliente))
            client_layout.addRow("RFC:", QLabel(detalles["cotizacion"].rfc_cliente or ""))
            client_layout.addRow("Teléfono:", QLabel(detalles["cotizacion"].telefono_cliente or ""))
            client_layout.addRow("Correo:", QLabel(detalles["cotizacion"].correo_cliente or ""))
            client_layout.addRow("Tipo:", QLabel(detalles["cotizacion"].tipo_cliente or ""))
            
            client_group.setLayout(client_layout)
            scroll_layout.addWidget(client_group)
            
            # Datos de la cotización
            cotizacion_group = QGroupBox("Datos de la Cotización")
            cotizacion_layout = QFormLayout()
            
            fecha_creacion = detalles["cotizacion"].fecha_creacion.strftime('%Y-%m-%d') if detalles["cotizacion"].fecha_creacion else ""
            fecha_activacion = detalles["cotizacion"].fecha_activacion.strftime('%Y-%m-%d') if detalles["cotizacion"].fecha_activacion else ""
            
            cotizacion_layout.addRow("Fecha Creación:", QLabel(fecha_creacion))
            cotizacion_layout.addRow("Fecha Activación:", QLabel(fecha_activacion))
            cotizacion_layout.addRow("Observaciones:", QLabel(detalles["cotizacion"].observaciones or ""))
            cotizacion_layout.addRow("Usuario Creador:", QLabel(detalles["cotizacion"].usuario_creador or ""))
            
            cotizacion_group.setLayout(cotizacion_layout)
            scroll_layout.addWidget(cotizacion_group)
            
            # Servicios
            servicios_group = QGroupBox("Servicios")
            servicios_layout = QVBoxLayout()
            
            servicios_table = QTableWidget()
            servicios_table.setColumnCount(6)
            servicios_table.setHorizontalHeaderLabels(["Nombre", "Descripción", "Tipo", "Costo", "Cantidad", "Subtotal"])
            servicios_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            servicios_table.setEditTriggers(QTableWidget.NoEditTriggers)
            servicios_table.setAlternatingRowColors(True)
            
            total_servicios = 0
            
            if detalles["servicios"]:
                for i, servicio in enumerate(detalles["servicios"]):
                    servicios_table.insertRow(i)
                    
                    servicios_table.setItem(i, 0, QTableWidgetItem(servicio.nombre_servicio))
                    servicios_table.setItem(i, 1, QTableWidgetItem(servicio.descripcion_servicio or ""))
                    servicios_table.setItem(i, 2, QTableWidgetItem(servicio.tipo_servicio or ""))
                    
                    costo = QTableWidgetItem(f"${servicio.costo_servicio:.2f}")
                    costo.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    servicios_table.setItem(i, 3, costo)
                    
                    cantidad = servicio.cantidad_servicio or 1
                    cantidad_item = QTableWidgetItem(str(cantidad))
                    cantidad_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    servicios_table.setItem(i, 4, cantidad_item)
                    
                    subtotal = servicio.costo_servicio * cantidad
                    total_servicios += subtotal
                    
                    subtotal_item = QTableWidgetItem(f"${subtotal:.2f}")
                    subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    servicios_table.setItem(i, 5, subtotal_item)
                    
            servicios_layout.addWidget(servicios_table)
            servicios_group.setLayout(servicios_layout)
            scroll_layout.addWidget(servicios_group)
            
            # Materiales
            materiales_group = QGroupBox("Materiales")
            materiales_layout = QVBoxLayout()
            
            materiales_table = QTableWidget()
            materiales_table.setColumnCount(6)
            materiales_table.setHorizontalHeaderLabels(["Nombre", "Proveedor", "Unidad", "Cantidad", "Precio", "Subtotal"])
            materiales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            materiales_table.setEditTriggers(QTableWidget.NoEditTriggers)
            materiales_table.setAlternatingRowColors(True)
            
            total_materiales = 0
            
            if detalles["materiales"]:
                for i, material in enumerate(detalles["materiales"]):
                    try:
                        materiales_table.insertRow(i)
                        
                        nombre_material = material.get("nombre_material", "Desconocido")
                        materiales_table.setItem(i, 0, QTableWidgetItem(nombre_material))
                        
                        nombre_proveedor = material.get("nombre_proveedor", "")
                        materiales_table.setItem(i, 1, QTableWidgetItem(nombre_proveedor))
                        
                        unidad_medida = material.get("unidad_medida", "")
                        materiales_table.setItem(i, 2, QTableWidgetItem(unidad_medida))
                        
                        cantidad = float(material.get("cantidad", 0))
                        cantidad_item = QTableWidgetItem(str(cantidad))
                        cantidad_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        materiales_table.setItem(i, 3, cantidad_item)
                        
                        precio = float(material.get("precio_unitario", 0))
                        precio_item = QTableWidgetItem(f"${precio:.2f}")
                        precio_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        materiales_table.setItem(i, 4, precio_item)
                        
                        subtotal = cantidad * precio
                        total_materiales += subtotal
                        
                        subtotal_item = QTableWidgetItem(f"${subtotal:.2f}")
                        subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        materiales_table.setItem(i, 5, subtotal_item)
                    except Exception as e:
                        print(f"Error al procesar material {i}: {str(e)}")
                    
            materiales_layout.addWidget(materiales_table)
            materiales_group.setLayout(materiales_layout)
            scroll_layout.addWidget(materiales_group)
            
            # Resumen
            resumen_group = QGroupBox("Resumen")
            resumen_layout = QFormLayout()
            
            iva_servicios = total_servicios * 0.16
            total_servicios_iva = total_servicios + iva_servicios
            gran_total = total_servicios_iva + total_materiales
            
            total_servicios_label = QLabel(f"${total_servicios:.2f}")
            iva_servicios_label = QLabel(f"${iva_servicios:.2f}")
            total_servicios_iva_label = QLabel(f"${total_servicios_iva:.2f}")
            total_materiales_label = QLabel(f"${total_materiales:.2f}")
            gran_total_label = QLabel(f"${gran_total:.2f}")
            
            font = QFont()
            font.setBold(True)
            gran_total_label.setFont(font)
            
            resumen_layout.addRow("Total Servicios (sin IVA):", total_servicios_label)
            resumen_layout.addRow("IVA 16% Servicios:", iva_servicios_label)
            resumen_layout.addRow("Total Servicios (con IVA):", total_servicios_iva_label)
            resumen_layout.addRow("Total Materiales:", total_materiales_label)
            resumen_layout.addRow("GRAN TOTAL:", gran_total_label)
            
            resumen_group.setLayout(resumen_layout)
            scroll_layout.addWidget(resumen_group)
            
            # Finalizar scroll area
            scroll.setWidget(scroll_content)
            layout.addWidget(scroll)
            
            # Botones
            buttons_layout = QHBoxLayout()
            
            print_btn = QPushButton("Imprimir")
            print_btn.clicked.connect(lambda: self.print_cotizacion(id_cotizacion))
            
            export_btn = QPushButton("Exportar")
            export_btn.clicked.connect(lambda: self.export_cotizacion(id_cotizacion))
            
            close_btn = QPushButton("Cerrar")
            close_btn.clicked.connect(dialog.reject)
            
            buttons_layout.addWidget(print_btn)
            buttons_layout.addWidget(export_btn)
            buttons_layout.addStretch()
            buttons_layout.addWidget(close_btn)
            
            layout.addLayout(buttons_layout)
            
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar detalles: {str(e)}")
    
    def print_cotizacion(self, id_cotizacion=None):
        """Imprime una cotización"""
        if id_cotizacion is None:
            selected_rows = self.cotizaciones_table.selectionModel().selectedRows()
            if not selected_rows:
                QMessageBox.warning(self, "Selección requerida", "Por favor seleccione una cotización para imprimir")
                return
                
            row = selected_rows[0].row()
            id_cotizacion = int(self.cotizaciones_table.item(row, 0).text())
        
        # Generar PDF
        if PDF_AVAILABLE:
            self.generate_pdf(id_cotizacion)
        else:
            QMessageBox.information(self, "PDF", "La funcionalidad de PDF requiere la instalación de reportlab. Ejecute 'pip install reportlab'.")
    
    def generate_pdf(self, id_cotizacion):
        """Genera un PDF de la cotización"""
        try:
            # Obtener detalles de la cotización
            detalles = self.controller.obtener_detalles_cotizacion(id_cotizacion)
            if not detalles:
                QMessageBox.warning(self, "Error", "No se pudieron obtener los detalles de la cotización")
                return
            
            # Solicitar ubicación para guardar el PDF
            file_name = f"Cotizacion_{id_cotizacion}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            file_path, _ = QFileDialog.getSaveFileName(self, "Guardar PDF", file_name, "PDF Files (*.pdf)")
            
            if not file_path:
                return  # Usuario canceló
                
            # Crear el PDF
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []
            
            # Título
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Title'],
                alignment=1,  # Centrado
                spaceAfter=12
            )
            elements.append(Paragraph(f"COTIZACIÓN #{id_cotizacion}", title_style))
            elements.append(Spacer(1, 12))
            
            # Fecha
            fecha_creacion = detalles["cotizacion"].fecha_creacion.strftime('%d/%m/%Y') if detalles["cotizacion"].fecha_creacion else ""
            elements.append(Paragraph(f"Fecha: {fecha_creacion}", styles["Normal"]))
            elements.append(Spacer(1, 12))
            
            # Estado
            estado = "Activa"
            if detalles["cotizacion"].fecha_cancelacion:
                estado = "Cancelada"
            elif detalles["cotizacion"].fecha_finalizacion:
                estado = "Finalizada"
                
            estado_style = ParagraphStyle(
                'Estado',
                parent=styles['Normal'],
                textColor=colors.green if estado == "Activa" else colors.red,
                alignment=2  # Derecha
            )
            elements.append(Paragraph(f"Estado: {estado}", estado_style))
            elements.append(Spacer(1, 12))
            
            # Datos del cliente
            elements.append(Paragraph("DATOS DEL CLIENTE", styles["Heading2"]))
            client_data = [
                ["Nombre:", detalles["cotizacion"].nombre_cliente],
                ["RFC:", detalles["cotizacion"].rfc_cliente or ""],
                ["Teléfono:", detalles["cotizacion"].telefono_cliente or ""],
                ["Correo:", detalles["cotizacion"].correo_cliente or ""],
                ["Tipo:", detalles["cotizacion"].tipo_cliente or ""]
            ]
            client_table = Table(client_data, colWidths=[100, 400])
            client_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 6)
            ]))
            elements.append(client_table)
            elements.append(Spacer(1, 12))
            
            # Datos de la cotización
            elements.append(Paragraph("DATOS DE LA COTIZACIÓN", styles["Heading2"]))
            fecha_activacion = detalles["cotizacion"].fecha_activacion.strftime('%d/%m/%Y') if detalles["cotizacion"].fecha_activacion else ""
            cotizacion_data = [
                ["Fecha Creación:", fecha_creacion],
                ["Fecha Activación:", fecha_activacion],
                ["Observaciones:", detalles["cotizacion"].observaciones or ""],
                ["Usuario Creador:", detalles["cotizacion"].usuario_creador or ""]
            ]
            cotizacion_table = Table(cotizacion_data, colWidths=[100, 400])
            cotizacion_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 6)
            ]))
            elements.append(cotizacion_table)
            elements.append(Spacer(1, 12))
            
            # Servicios
            elements.append(Paragraph("SERVICIOS", styles["Heading2"]))
            
            total_servicios = 0
            if detalles["servicios"]:
                servicios_data = [["Nombre", "Descripción", "Tipo", "Costo", "Cantidad", "Subtotal"]]
                
                for servicio in detalles["servicios"]:
                    cantidad = servicio.cantidad_servicio or 1
                    subtotal = servicio.costo_servicio * cantidad
                    total_servicios += subtotal
                    
                    servicios_data.append([
                        servicio.nombre_servicio,
                        servicio.descripcion_servicio or "",
                        servicio.tipo_servicio or "",
                        f"${servicio.costo_servicio:.2f}",
                        str(cantidad),
                        f"${subtotal:.2f}"
                    ])
                
                servicios_table = Table(servicios_data, colWidths=[100, 150, 60, 60, 60, 70])
                servicios_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('PADDING', (0, 0), (-1, -1), 6),
                    ('ALIGN', (3, 1), (5, -1), 'RIGHT')
                ]))
                elements.append(servicios_table)
            else:
                elements.append(Paragraph("No hay servicios registrados para esta cotización", styles["Normal"]))
                
            elements.append(Spacer(1, 12))
            
            # Materiales
            elements.append(Paragraph("MATERIALES", styles["Heading2"]))
            
            total_materiales = 0
            if detalles["materiales"]:
                materiales_data = [["Nombre", "Proveedor", "Unidad", "Cantidad", "Precio", "Subtotal"]]
                
                for material in detalles["materiales"]:
                    try:
                        nombre_material = material.get("nombre_material", "Desconocido")
                        nombre_proveedor = material.get("nombre_proveedor", "")
                        unidad_medida = material.get("unidad_medida", "")
                        
                        cantidad = float(material.get("cantidad", 0))
                        precio = float(material.get("precio_unitario", 0))
                        
                        subtotal = cantidad * precio
                        total_materiales += subtotal
                        
                        materiales_data.append([
                            nombre_material,
                            nombre_proveedor,
                            unidad_medida,
                            str(cantidad),
                            f"${precio:.2f}",
                            f"${subtotal:.2f}"
                        ])
                    except Exception as e:
                        print(f"Error al procesar material para PDF: {str(e)}")
                
                materiales_table = Table(materiales_data, colWidths=[100, 100, 60, 60, 60, 70])
                materiales_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('PADDING', (0, 0), (-1, -1), 6),
                    ('ALIGN', (3, 1), (5, -1), 'RIGHT')
                ]))
                elements.append(materiales_table)
            else:
                elements.append(Paragraph("No hay materiales registrados para esta cotización", styles["Normal"]))
                
            elements.append(Spacer(1, 12))
            
            # Resumen
            elements.append(Paragraph("RESUMEN FINANCIERO", styles["Heading2"]))
            
            iva_servicios = total_servicios * 0.16
            total_servicios_iva = total_servicios + iva_servicios
            gran_total = total_servicios_iva + total_materiales
            
            resumen_data = [
                ["Total Servicios (sin IVA):", f"${total_servicios:.2f}"],
                ["IVA 16% Servicios:", f"${iva_servicios:.2f}"],
                ["Total Servicios (con IVA):", f"${total_servicios_iva:.2f}"],
                ["Total Materiales:", f"${total_materiales:.2f}"],
                ["GRAN TOTAL:", f"${gran_total:.2f}"]
            ]
            
            resumen_table = Table(resumen_data, colWidths=[200, 100])
            resumen_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightblue),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
            ]))
            elements.append(resumen_table)
            
            # Construir el PDF
            doc.build(elements)
            
            # Preguntar si desea abrir el PDF
            open_pdf = QMessageBox.question(
                self,
                "PDF Generado",
                f"El PDF se ha generado correctamente en:\n{file_path}\n\n¿Desea abrirlo ahora?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if open_pdf == QMessageBox.Yes:
                import os
                import platform
                
                if platform.system() == 'Windows':
                    os.startfile(file_path)
                elif platform.system() == 'Darwin':  # macOS
                    os.system(f'open "{file_path}"')
                else:  # Linux
                    os.system(f'xdg-open "{file_path}"')
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar PDF: {str(e)}")
    
    def export_cotizacion(self, id_cotizacion=None):
        """Exporta una cotización a PDF o Excel"""
        if id_cotizacion is None:
            selected_rows = self.cotizaciones_table.selectionModel().selectedRows()
            if not selected_rows:
                QMessageBox.warning(self, "Selección requerida", "Por favor seleccione una cotización para exportar")
                return
                
            row = selected_rows[0].row()
            id_cotizacion = int(self.cotizaciones_table.item(row, 0).text())
        
        # Por ahora, solo exportamos a PDF
        self.print_cotizacion(id_cotizacion)
    
    def cancel_cotizacion(self):
        """Cancela una cotización"""
        selected_rows = self.cotizaciones_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Selección requerida", "Por favor seleccione una cotización para cancelar")
            return
            
        row = selected_rows[0].row()
        id_cotizacion = int(self.cotizaciones_table.item(row, 0).text())
        
        # Verificar si ya está cancelada
        estado = self.cotizaciones_table.item(row, 4).text()
        if estado == "Cancelada":
            QMessageBox.information(self, "Información", "Esta cotización ya está cancelada")
            return
            
        confirm = QMessageBox.question(
            self,
            "Confirmar cancelación",
            f"¿Está seguro de cancelar la cotización #{id_cotizacion}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                # Solicitar motivo de cancelación
                motivo, ok = QInputDialog.getText(
                    self, 
                    "Motivo de Cancelación", 
                    "Ingrese el motivo de la cancelación (opcional):"
                )
                
                if ok:  # El usuario presionó OK (incluso si no ingresó un motivo)
                    # Si se proporcionó un motivo, actualizar las observaciones
                    if motivo:
                        cotizacion = self.controller.obtener_cotizacion(id_cotizacion)
                        observaciones_actuales = cotizacion.observaciones or ""
                        cotizacion.observaciones = f"{observaciones_actuales}\nMotivo de cancelación: {motivo}"
                        self.controller.repository.update_cotizacion(id_cotizacion, cotizacion)
                    
                    # Marcar como inactiva
                    if self.controller.marcar_cotizacion_como_inactiva(id_cotizacion):
                        QMessageBox.information(self, "Éxito", "La cotización ha sido cancelada correctamente")
                        self.load_cotizaciones()
                    else:
                        QMessageBox.critical(self, "Error", "No se pudo cancelar la cotización")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cancelar cotización: {str(e)}")

if __name__ == "__main__":
    from Database.Conexion import obtener_conexion
    
    # Obtener la cadena de conexión
    connection_string = obtener_conexion()
    
    if connection_string is None:
        print("❌ No se pudo obtener la conexión a la base de datos.")
        exit()
    
    print("✅ Conexión establecida correctamente")
    
    app = QApplication(sys.argv)
    ventana = CotizacionGUI(connection_string)
    ventana.show()
    sys.exit(app.exec_())