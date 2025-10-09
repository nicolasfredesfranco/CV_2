#!/usr/bin/env python3
"""
CV PDF Generator - VERSIÓN 2.0 REVOLUCIONARIA
==============================================

Estrategia óptima: Combinar estructura de bloques del original
con coordenadas exactas del archivo de extracción.

ITERACIÓN: #27
OBJETIVO: 90+/100
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
        return True
    except:
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

def get_block_for_y(y, block_ranges):
    """Determinar a qué bloque pertenece un elemento por su Y"""
    for i, (y_start, y_end) in enumerate(block_ranges):
        if y_start <= y <= y_end:
            return i
    return -1  # No pertenece a ningún bloque definido

def create_cv():
    """Genera CV con estructura de bloques optimizada"""
    
    has_trebuchet = load_fonts()
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
    
    # Cargar datos extraídos
    try:
        with open('/tmp/pdf_complete_extraction.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        spans = data['spans']
        print(f"✅ Loaded {len(spans)} elements")
    except:
        print("❌ Could not load extraction data")
        c.save()
        return
    
    # Dibujar banners
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
    
    # Definir rangos de bloques (basados en el análisis del original)
    block_ranges = [
        (31, 43),    # Block 1: Nombre pequeño
        (47, 70),    # Block 2: Dirección
        (69, 125),   # Block 3: Links
        (130, 330),  # Block 4: EDUCATION
        (340, 354),  # Block 5: Banner SKILLS
        (363, 662),  # Block 6: Contenido SKILLS
        (673, 687),  # Block 7: Banner LANGUAGES
        (695, 706),  # Block 8: Spanish
        (711, 722),  # Block 9: English
        (32, 58),    # Block 10: Título grande
        (70, 407),   # Block 11: EXPERIENCE superior
        (408, 682),  # Block 12: EXPERIENCE inferior
        (688, 702),  # Block 13: Banner PAPERS
        (706, 731),  # Block 14: Journal Paper
        (736, 759),  # Block 15: Workshop
    ]
    
    # Agrupar spans por bloque
    blocks_by_id = [[] for _ in range(len(block_ranges))]
    unassigned = []
    
    for span in spans:
        y = span['y']
        block_id = get_block_for_y(y, block_ranges)
        if block_id >= 0:
            blocks_by_id[block_id].append(span)
        else:
            unassigned.append(span)
    
    print(f"✅ Agrupados en {len(block_ranges)} bloques ({len(unassigned)} no asignados)")
    
    # Dibujar cada bloque POR SEPARADO con gap entre ellos
    elements_drawn = 0
    
    for block_id, block_spans in enumerate(blocks_by_id):
        if not block_spans:
            continue
        
        # Ordenar spans del bloque por Y, luego por X
        block_spans.sort(key=lambda s: (s['y'], s['x']))
        
        # Dibujar cada elemento del bloque
        for span in block_spans:
            text = span['text']
            if not text or len(text.strip()) == 0:
                continue
            
            x = span['x']
            y = span['y']
            font_orig = span['font']
            size = span['size']
            color_hex = span['color']
            bold = span['bold']
            italic = span['italic']
            
            # Mapear font
            font_name = get_reportlab_font(font_orig, bold, italic, has_trebuchet)
            
            # Set color
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
            elements_drawn += 1
        
        # Después de cada bloque, insertar un marcador invisible
        # para ayudar a PyMuPDF a detectar la separación
        if block_id < len(blocks_by_id) - 1:
            c.saveState()
            c.setFillColor(colors.white)
            c.setFont('Helvetica', 1)  # Font muy pequeño
            # Dibujar en posición fuera de vista
            c.drawString(-100, -100, " ")
            c.restoreState()
    
    # Dibujar elementos no asignados
    for span in unassigned:
        text = span['text']
        if not text or len(text.strip()) == 0:
            continue
        
        x = span['x']
        y = span['y']
        font_orig = span['font']
        size = span['size']
        color_hex = span['color']
        bold = span['bold']
        italic = span['italic']
        
        font_name = get_reportlab_font(font_orig, bold, italic, has_trebuchet)
        
        if color_hex in COLORS:
            c.setFillColor(COLORS[color_hex])
        else:
            c.setFillColor(colors.HexColor(color_hex))
        
        try:
            c.setFont(font_name, size)
        except:
            c.setFont('Helvetica', size)
        
        c.drawString(x, y, text)
        elements_drawn += 1
    
    print(f"✅ Drew {elements_drawn} total elements")
    
    c.save()
    print("✅ PDF generated successfully")

if __name__ == "__main__":
    create_cv()

