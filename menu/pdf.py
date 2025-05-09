from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
import os
from datetime import datetime

def generar_pdf_cotizacion(cotizacion, cliente, servicios, materiales, ruta_salida=None):
    """
    Genera un PDF con los detalles de la cotización
    
    Args:
        cotizacion: Objeto o diccionario con los datos de la cotización
        cliente: Objeto o diccionario con los datos del cliente
        servicios: Lista de servicios de la cotización
        materiales: Lista de materiales de la cotización
        ruta_salida: Ruta donde se guardará el PDF (opcional)
        
    Returns:
        str: Ruta del archivo PDF generado
    """
    # Determinar la ruta de salida
    if not ruta_salida:
        # Crear carpeta 'cotizaciones' si no existe
        if not os.path.exists('cotizaciones'):
            os.makedirs('cotizaciones')
        
        # Generar nombre de archivo con fecha y hora actual
        fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"Cotizacion_{fecha_hora}.pdf"
        ruta_salida = os.path.join('cotizaciones', nombre_archivo)
    
    # Crear el documento
    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Contenedor para los elementos del PDF
    elementos = []
    
    # Estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        'TituloCentrado',
        parent=estilos['Heading1'],
        alignment=TA_CENTER,
        spaceAfter=12
    )
    estilo_subtitulo = ParagraphStyle(
        'Subtitulo',
        parent=estilos['Heading2'],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=6
    )
    estilo_normal = estilos['Normal']
    estilo_derecha = ParagraphStyle(
        'Derecha', 
        parent=estilo_normal,
        alignment=TA_RIGHT
    )
    
    # Título del documento
    elementos.append(Paragraph("COTIZACIÓN", estilo_titulo))
    elementos.append(Spacer(1, 0.25*inch))
    
    # Información de la empresa (puedes personalizarla)
    elementos.append(Paragraph("TU EMPRESA S.A. DE C.V.", estilos['Heading3']))
    elementos.append(Paragraph("Dirección: Calle Principal #123", estilo_normal))
    elementos.append(Paragraph("Teléfono: (81) 1234-5678", estilo_normal))
    elementos.append(Paragraph("Email: contacto@tuempresa.com", estilo_normal))
    elementos.append(Spacer(1, 0.25*inch))
    
    # Datos de la cotización
    fecha_creacion = cotizacion.fecha_creacion.strftime('%d/%m/%Y') if hasattr(cotizacion, 'fecha_creacion') else cotizacion["fecha_creacion"].strftime('%d/%m/%Y')
    elementos.append(Paragraph(f"Cotización #: {getattr(cotizacion, 'id_cotizacion', 'Nueva')}", estilo_normal))
    elementos.append(Paragraph(f"Fecha: {fecha_creacion}", estilo_normal))
    elementos.append(Paragraph(f"Creado por: {getattr(cotizacion, 'usuario_creador', cotizacion.get('usuario_creador', ''))}", estilo_normal))
    elementos.append(Spacer(1, 0.25*inch))
    
    # Datos del cliente
    elementos.append(Paragraph("DATOS DEL CLIENTE", estilo_subtitulo))
    
    nombre_cliente = getattr(cliente, 'nombre', cliente.get('nombre', ''))
    tipo_cliente = getattr(cliente, 'tipo_cliente', cliente.get('tipo_cliente', ''))
    rfc_cliente = getattr(cliente, 'rfc', cliente.get('rfc', 'No especificado'))
    telefono_cliente = getattr(cliente, 'telefono', cliente.get('telefono', 'No especificado'))
    correo_cliente = getattr(cliente, 'correo', cliente.get('correo', 'No especificado'))
    
    datos_cliente = [
        ["Nombre:", nombre_cliente],
        ["Tipo:", tipo_cliente],
        ["RFC:", rfc_cliente],
        ["Teléfono:", telefono_cliente],
        ["Correo:", correo_cliente]
    ]
    
    tabla_cliente = Table(datos_cliente, colWidths=[1.5*inch, 4*inch])
    tabla_cliente.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))
    elementos.append(tabla_cliente)
    elementos.append(Spacer(1, 0.25*inch))
    
    # Servicios
    elementos.append(Paragraph("SERVICIOS (MANO DE OBRA)", estilo_subtitulo))
    
    if servicios:
        # Encabezados de la tabla
        datos_servicios = [["#", "Nombre", "Tipo", "Costo Unit.", "Cantidad", "Subtotal"]]
        
        # Datos de servicios
        total_servicios = 0
        for i, servicio in enumerate(servicios, 1):
            if isinstance(servicio, dict):
                nombre = servicio.get('nombre_servicio', '')[:20]
                tipo = servicio.get('tipo_servicio', '-')[:10]
                costo = servicio.get('costo_servicio', 0)
                cantidad = servicio.get('cantidad_servicio', 1) or 1
            else:
                nombre = getattr(servicio, 'nombre_servicio', '')[:20]
                tipo = getattr(servicio, 'tipo_servicio', '-')[:10]
                costo = getattr(servicio, 'costo_servicio', 0)
                cantidad = getattr(servicio, 'cantidad_servicio', 1) or 1
            
            subtotal = costo * cantidad
            total_servicios += subtotal
            
            datos_servicios.append([
                str(i),
                nombre,
                tipo,
                f"${costo:.2f}",
                str(cantidad),
                f"${subtotal:.2f}"
            ])
        
        # Agregar fila de total
        datos_servicios.append(["", "", "", "", "Total:", f"${total_servicios:.2f}"])
        
        # Crear tabla de servicios
        tabla_servicios = Table(datos_servicios, colWidths=[0.3*inch, 2*inch, 1*inch, 1*inch, 0.7*inch, 1*inch])
        tabla_servicios.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -2), 0.25, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
            ('ALIGN', (-2, -1), (-1, -1), 'RIGHT'),
            ('BACKGROUND', (-2, -1), (-1, -1), colors.lightgrey),
        ]))
        elementos.append(tabla_servicios)
    else:
        elementos.append(Paragraph("No se agregaron servicios", estilo_normal))
    
    elementos.append(Spacer(1, 0.25*inch))
    
    # Materiales
    elementos.append(Paragraph("MATERIALES", estilo_subtitulo))
    
    if materiales:
        # Encabezados de la tabla
        datos_materiales = [["#", "Nombre Material", "Cantidad", "Precio", "Subtotal"]]
        
        # Datos de materiales
        total_materiales = 0
        for i, material in enumerate(materiales, 1):
            if isinstance(material, dict):
                nombre = material.get('nombre_material', '')[:20]
                cantidad = float(material.get('cantidad', 0))
                precio = float(material.get('precio_unitario', 0))
            else:
                nombre = getattr(material, 'nombre_material', '')[:20]
                cantidad = float(getattr(material, 'cantidad', 0))
                precio = float(getattr(material, 'precio_unitario', 0))
            
            subtotal = cantidad * precio
            total_materiales += subtotal
            
            datos_materiales.append([
                str(i),
                nombre,
                str(cantidad),
                f"${precio:.2f}",
                f"${subtotal:.2f}"
            ])
        
        # Agregar fila de total
        datos_materiales.append(["", "", "", "Total:", f"${total_materiales:.2f}"])
        
        # Crear tabla de materiales
        tabla_materiales = Table(datos_materiales, colWidths=[0.3*inch, 2.5*inch, 0.7*inch, 1*inch, 1.5*inch])
        tabla_materiales.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -2), 0.25, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
            ('ALIGN', (-2, -1), (-1, -1), 'RIGHT'),
            ('BACKGROUND', (-2, -1), (-1, -1), colors.lightgrey),
        ]))
        elementos.append(tabla_materiales)
    else:
        elementos.append(Paragraph("No se agregaron materiales", estilo_normal))
    
    elementos.append(Spacer(1, 0.5*inch))
    
    # Resumen final
    elementos.append(Paragraph("RESUMEN FINAL", estilo_subtitulo))
    
    # Calcular totales
    total_servicios = 0
    for servicio in servicios:
        if isinstance(servicio, dict):
            costo = servicio.get('costo_servicio', 0)
            cantidad = servicio.get('cantidad_servicio', 1) or 1
        else:
            costo = getattr(servicio, 'costo_servicio', 0)
            cantidad = getattr(servicio, 'cantidad_servicio', 1) or 1
        total_servicios += costo * cantidad
    
    total_materiales = 0
    for material in materiales:
        if isinstance(material, dict):
            cantidad = float(material.get('cantidad', 0))
            precio = float(material.get('precio_unitario', 0))
        else:
            cantidad = float(getattr(material, 'cantidad', 0))
            precio = float(getattr(material, 'precio_unitario', 0))
        total_materiales += cantidad * precio
    
    iva_servicios = total_servicios * 0.16
    total_servicios_con_iva = total_servicios + iva_servicios
    gran_total = total_servicios_con_iva + total_materiales
    
    # Tabla de resumen
    datos_resumen = [
        ["Total Servicios (sin IVA):", f"${total_servicios:.2f}"],
        ["IVA 16% Servicios:", f"${iva_servicios:.2f}"],
        ["Total Servicios (con IVA):", f"${total_servicios_con_iva:.2f}"],
        ["Total Materiales:", f"${total_materiales:.2f}"],
        ["GRAN TOTAL:", f"${gran_total:.2f}"]
    ]
    
    tabla_resumen = Table(datos_resumen, colWidths=[4*inch, 2*inch])
    tabla_resumen.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))
    elementos.append(tabla_resumen)
    
    # Observaciones
    elementos.append(Spacer(1, 0.5*inch))
    elementos.append(Paragraph("OBSERVACIONES:", estilo_subtitulo))
    observaciones = getattr(cotizacion, 'observaciones', cotizacion.get('observaciones', ''))
    elementos.append(Paragraph(observaciones or "Sin observaciones", estilo_normal))
    
    # Términos y condiciones
    elementos.append(Spacer(1, 0.5*inch))
    elementos.append(Paragraph("TÉRMINOS Y CONDICIONES:", estilo_subtitulo))
    elementos.append(Paragraph("1. Precios sujetos a cambio sin previo aviso.", estilo_normal))
    elementos.append(Paragraph("2. Cotización válida por 30 días.", estilo_normal))
    elementos.append(Paragraph("3. Forma de pago: 50% anticipo, 50% contra entrega.", estilo_normal))
    
    # Construir el PDF
    doc.build(elementos)
    
    return ruta_salida