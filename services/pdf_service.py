# -*- coding: utf-8 -*-
"""
Servicio de PDF - Generación de Documentos
Materiales Ibarra, S.A.
"""

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from models.cotizacion import Cotizacion
from models.factura import Factura
import logging

logger = logging.getLogger(__name__)

class PDFService:
    """Servicio para generación de PDFs"""
    
    @staticmethod
    def generar_cotizacion_pdf(cotizacion: Cotizacion) -> bytes:
        """Genera un PDF de cotización"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
            elements = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1
            )
            
            elements.append(Paragraph("MATERIALES IBARRA, S.A.", title_style))
            elements.append(Paragraph("Cotización de Materiales", styles['Normal']))
            elements.append(Spacer(1, 20))
            
            info_data = [
                ['Cliente:', cotizacion.cliente_nombre],
                ['Cédula:', cotizacion.cliente_cedula or "N/A"],
                ['Teléfono:', cotizacion.cliente_telefono or "N/A"],
                ['Email:', cotizacion.cliente_email or "N/A"],
                ['Sucursal:', cotizacion.sucursal],
                ['Fecha:', cotizacion.created_at.strftime("%Y-%m-%d %H:%M:%S")]
            ]
            
            info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 20))
            
            elementos_tabla = [['Material', 'Cantidad', 'Precio', 'Subtotal']]
            for item in cotizacion.items:
                elementos_tabla.append([
                    item.nombre,
                    str(item.cantidad),
                    f"${item.precio_unitario:.2f}",
                    f"${item.subtotal:.2f}"
                ])
            
            tabla = Table(elementos_tabla, colWidths=[2.5*inch, 1*inch, 1.25*inch, 1.25*inch])
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
            ]))
            elements.append(tabla)
            elements.append(Spacer(1, 20))
            
            totales_data = [
                ['Subtotal:', f"${cotizacion.subtotal:.2f}"],
                ['ITBMS (7%):', f"${cotizacion.itbms:.2f}"],
                ['TOTAL:', f"${cotizacion.total:.2f}"]
            ]
            
            totales_table = Table(totales_data, colWidths=[4*inch, 2*inch])
            totales_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(totales_table)
            elements.append(Spacer(1, 30))
            
            footer_style = ParagraphStyle('Footer', fontSize=9, textColor=colors.gray)
            elements.append(Paragraph("Esta cotización tiene validez por 30 días. Subject to prior sale.", footer_style))
            
            doc.build(elements)
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error generando PDF de cotización: {e}")
            return None
    
    @staticmethod
    def generar_factura_pdf(factura: Factura) -> bytes:
        """Genera un PDF de factura fiscal"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
            elements = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, spaceAfter=30, alignment=1)
            elements.append(Paragraph("MATERIALES IBARRA, S.A.", title_style))
            elements.append(Paragraph("FACTURA FISCAL", styles['Normal']))
            elements.append(Paragraph(f"No. {factura.numero_factura}", styles['Normal']))
            elements.append(Spacer(1, 20))
            
            info_data = [
                ['RUC: XXXXXXXXXXXX', f"Fecha: {factura.created_at.strftime('%Y-%m-%d')}"],
                ['Dirección: Vía Panamericana, Chiriquí', f"Sucursal: {factura.sucursal}"],
            ]
            
            info_table = Table(info_data, colWidths=[4*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 15))
            
            elements.append(Paragraph("<b>DATOS DEL CLIENTE</b>", styles['Normal']))
            cliente_data = [
                ['Cliente:', factura.cliente_nombre],
                ['Cédula/RUC:', factura.cedula_cliente],
                ['Dirección:', factura.cliente_direccion],
                ['Teléfono:', factura.cliente_telefono]
            ]
            
            cliente_table = Table(cliente_data, colWidths=[1.5*inch, 4.5*inch])
            cliente_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(cliente_table)
            elements.append(Spacer(1, 20))
            
            elementos_tabla = [['Código', 'Descripción', 'Cant', 'P.Unit', 'ITBMS', 'Total']]
            for item in factura.items:
                elementos_tabla.append([
                    item.codigo,
                    item.descripcion[:25],
                    str(item.cantidad),
                    f"${item.precio_unitario:.2f}",
                    f"${item.itbms:.2f}",
                    f"${item.total:.2f}"
                ])
            
            tabla = Table(elementos_tabla, colWidths=[0.8*inch, 2.2*inch, 0.6*inch, 1*inch, 0.8*inch, 1*inch])
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ]))
            elements.append(tabla)
            elements.append(Spacer(1, 20))
            
            totales_data = [
                ['SUBTOTAL:', f"${factura.subtotal:.2f}"],
                ['ITBMS (7%):', f"${factura.itbms:.2f}"],
                ['TOTAL A PAGAR:', f"${factura.total:.2f}"]
            ]
            
            totales_table = Table(totales_data, colWidths=[4*inch, 2*inch])
            totales_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -2), 'Helvetica-Bold'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            elements.append(totales_table)
            elements.append(Spacer(1, 30))
            
            footer_style = ParagraphStyle('Footer', fontSize=8, textColor=colors.gray)
            elements.append(Paragraph("Documento tributario electrónico generado según normativa DGI.", footer_style))
            
            doc.build(elements)
            return buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Error generando PDF de factura: {e}")
            return None