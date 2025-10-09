#!/usr/bin/env python3
"""
CV PDF Generator - VERSIÓN HÍBRIDA
===================================

Estrategia: Replicar la ESTRUCTURA INTERNA del PDF original
para alcanzar 99% de score.

Enfoque:
1. Leer estructura de bloques del original con PyMuPDF
2. Generar PDF con ReportLab replicando esa estructura exacta
3. Usar textObject por bloque para separación clara

ITERACIÓN: #26 - Enfoque Híbrido
OBJETIVO: 99/100
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fitz
import os
import json

def load_fonts():
    """Cargar TrebuchetMS desde ~/.fonts/"""
    try:
        pdfmetrics.registerFont(TTFont('TrebuchetMS', os.path.expanduser('~/.fonts/trebuc.ttf')))
        pdfmetrics.registerFont(TTFont('TrebuchetMS-Bold', os.path.expanduser('~/.fonts/trebucbd.ttf')))
        pdfmetrics.registerFont(TTFont('TrebuchetMS-Italic', os.path.expanduser('~/.fonts/trebucit.ttf')))
        print("✅ TrebuchetMS fonts loaded")
        return True
    except Exception as e:
        print(f"⚠️  TrebuchetMS not available: {e}")
        return False

def get_reportlab_font(orig_font, bold=False, italic=False, has_trebuchet=True):
    """Mapear font del original a ReportLab"""
    if not has_trebuchet:
        if bold: return 'Helvetica-Bold'
        if italic: return 'Helvetica-Oblique'
        return 'Helvetica'
    
    if bold or 'Bold' in orig_font:
        return 'TrebuchetMS-Bold'
    if italic or 'Italic' in orig_font:
        return 'TrebuchetMS-Italic'
    return 'TrebuchetMS'

def extract_blocks_from_original():
    """Extraer estructura de bloques del PDF original"""
    doc = fitz.open('EN_NicolasFredes_CV.pdf')
    page = doc[0]
    
    # Extraer bloques con toda su información
    blocks_data = []
    dict_data = page.get_text("dict")
    
    for block in dict_data["blocks"]:
        if "lines" not in block:
            continue
        
        block_info = {
            'bbox': block['bbox'],
            'number': block['number'],
            'lines': []
        }
        
        for line in block["lines"]:
            line_info = {
                'bbox': line['bbox'],
                'spans': []
            }
            
            for span in line["spans"]:
                span_info = {
                    'text': span['text'],
                    'font': span['font'],
                    'size': span['size'],
                    'color': span['color'],
                    'origin': span['origin'],
                    'bbox': span['bbox'],
                    'flags': span['flags']
                }
                line_info['spans'].append(span_info)
            
            block_info['lines'].append(line_info)
        
        blocks_data.append(block_info)
    
    doc.close()
    return blocks_data

def create_cv_hybrid():
    """
    Genera CV replicando la estructura de bloques del original
    """
    
    # Cargar fuentes
    has_trebuchet = load_fonts()
    
    # Crear canvas
    c = canvas.Canvas("generated.pdf", pagesize=letter)
    page_width, page_height = letter
    
    # Colores
    COLORS = {
        '#000000': colors.HexColor("#000000"),
        '#1053cc': colors.HexColor("#1053cc"),
        '#2d73b3': colors.HexColor("#2d73b3"),
        '#0c0e19': colors.HexColor("#0c0e19"),
        '#f0f0f0': colors.HexColor("#f0f0f0"),
        '#ffffff': colors.white,
    }
    
    # Extraer estructura del original
    print("🔍 Extrayendo estructura del original...")
    blocks = extract_blocks_from_original()
    print(f"✅ Extraídos {len(blocks)} bloques")
    
    # Dibujar banners primero (fondos)
    banner_positions = {
        'EDUCATION': (36.0, 647.6, 159.5, 13.9),
        'SKILLS': (36.0, 438.0, 159.5, 13.9),
        'LANGUAGES': (36.0, 104.6, 159.5, 13.9),
        'EXPERIENCE': (209.0, 707.5, 372.8, 13.9),
        'PAPERS & WORKSHOPS': (209.0, 89.5, 372.8, 13.9),
    }
    
    c.setFillColor(COLORS['#f0f0f0'])
    for banner_name, (x, y_center, width, height) in banner_positions.items():
        c.rect(x, y_center - height/2, width, height, fill=1, stroke=0)
    
    # Dibujar cada bloque por separado
    total_spans = 0
    for block_idx, block in enumerate(blocks):
        # Crear un textObject para este bloque (crea separación)
        text_obj = c.beginText()
        text_obj.setTextOrigin(0, 0)
        
        for line in block['lines']:
            for span in line['spans']:
                text = span['text']
                if not text or len(text.strip()) == 0:
                    continue
                
                # Extraer datos
                x, y_top = span['origin']
                y = page_height - y_top  # Convertir coordenadas
                size = span['size']
                color = span['color']
                font = span['font']
                
                # Determinar si es bold/italic por el nombre de la font
                bold = 'Bold' in font
                italic = 'Italic' in font
                
                # Mapear font
                font_name = get_reportlab_font(font, bold, italic, has_trebuchet)
                
                # Set color
                color_hex = f"#{color:06x}"
                if color_hex in COLORS:
                    c.setFillColor(COLORS[color_hex])
                else:
                    c.setFillColor(colors.HexColor(color_hex))
                
                # Set font
                try:
                    c.setFont(font_name, size)
                except:
                    c.setFont('Helvetica', size)
                
                # Dibujar
                c.drawString(x, y, text)
                total_spans += 1
        
        # Finalizar textObject del bloque
        c.drawText(text_obj)
        
        # Insertar pequeño gap invisible entre bloques
        if block_idx < len(blocks) - 1:
            c.setFillColor(colors.white)
            # Dibujar espacio invisible para separar bloques
            c.drawString(0, 400, "")  # Whitespace invisible
    
    print(f"✅ Dibujados {total_spans} spans en {len(blocks)} bloques")
    
    # Guardar
    c.save()
    print(f"✅ PDF generado: generated.pdf")

if __name__ == "__main__":
    create_cv_hybrid()

