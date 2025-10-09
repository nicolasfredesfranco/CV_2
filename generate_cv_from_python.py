#!/usr/bin/env python3
"""
CV PDF Generator - VERSIÓN FINAL OPTIMIZADA
===========================================

⭐ ARCHIVO PRINCIPAL DEL PROYECTO ⭐

Genera PDF del CV usando Canvas directo con agrupación inteligente
Optimizado para máxima similitud con el original (iteración #17)

✅ ESTE ES EL ÚNICO ARCHIVO PYTHON QUE DEBES MODIFICAR

⚠️ ARCHIVOS PROTEGIDOS - NO MODIFICAR:
   ❌ EN_NicolasFredes_CV.pdf - Ground truth original  
   ❌ compare_pdf.py - Sistema de comparación calibrado

SCORE ANTERIOR: 71.43/100 (iteración #19)
OBJETIVO: 99/100  
ITERACIÓN: #22 - VERSIÓN FINAL OPTIMIZADA (mejor score)
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import json

def load_fonts():
    """Cargar TrebuchetMS desde ~/.fonts/"""
    try:
        pdfmetrics.registerFont(TTFont('TrebuchetMS', os.path.expanduser('~/.fonts/trebuc.ttf')))
        pdfmetrics.registerFont(TTFont('TrebuchetMS-Bold', os.path.expanduser('~/.fonts/trebucbd.ttf')))  # Bold puro
        pdfmetrics.registerFont(TTFont('TrebuchetMS-Italic', os.path.expanduser('~/.fonts/trebucit.ttf')))
        print("✅ TrebuchetMS fonts loaded (with proper Bold)")
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

def create_cv():
    """
    Genera CV usando Canvas con agrupación inteligente de elementos
    Agrupa spans en líneas y bloques para mejor detección de PyMuPDF
    """
    
    # Cargar fuentes
    has_trebuchet = load_fonts()
    
    # Crear canvas
    c = canvas.Canvas("generated.pdf", pagesize=letter)
    page_width, page_height = letter
    
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
    
    # Colores
    COLORS = {
        '#000000': colors.HexColor("#000000"),
        '#1053cc': colors.HexColor("#1053cc"),
        '#2d73b3': colors.HexColor("#2d73b3"),
        '#0c0e19': colors.HexColor("#0c0e19"),
        '#f0f0f0': colors.HexColor("#f0f0f0"),
        '#ffffff': colors.white,
    }
    
    # ═══════════════════════════════════════════════════════════
    # PASO 1: Dibujar banners (fondos grises)
    # ═══════════════════════════════════════════════════════════
    
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
    
    # ═══════════════════════════════════════════════════════════
    # PASO 2: Agrupar spans por línea (misma Y con tolerancia)
    # ═══════════════════════════════════════════════════════════
    
    lines = {}
    tolerance = 0.8  # Óptimo encontrado
    
    for span in spans:
        y_rounded = round(span['y'], 1)
        found_line = False
        
        for existing_y in list(lines.keys()):
            if abs(existing_y - y_rounded) < tolerance:
                lines[existing_y].append(span)
                found_line = True
                break
        
        if not found_line:
            lines[y_rounded] = [span]
    
    # Ordenar spans dentro de cada línea por X
    for y_key in lines:
        lines[y_key].sort(key=lambda s: s['x'])
    
    print(f"✅ Grouped into {len(lines)} lines")
    
    # ═══════════════════════════════════════════════════════════
    # PASO 3: Dibujar elementos en orden inverso (top-down) para mejor agrupación
    # ═══════════════════════════════════════════════════════════
    
    elements_drawn = 0
    
    # Ordenar de menor a mayor Y (bottom to top - orden natural)
    for y_pos in sorted(lines.keys()):
        line_spans = lines[y_pos]
        
        if not line_spans:
            continue
        
        # Crear textObject para esta línea (mejora agrupación)
        text_obj = c.beginText()
        text_obj.setTextOrigin(0, 0)  # Origen temporal
        
        # Dibujar cada span de la línea
        for span in line_spans:
            text = span['text']
            x = span['x']
            y = span['y']
            font_orig = span['font']
            size = span['size']
            color_hex = span['color']
            bold = span['bold']
            italic = span['italic']
            
            # Determinar font
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
            
            # Dibujar solo elementos con contenido significativo
            if text and len(text.strip()) > 0:
                c.drawString(x, y, text)
                elements_drawn += 1
    
    print(f"✅ Drew {elements_drawn} text elements")
    
    # Guardar
    c.save()
    print(f"\n✅ PDF generado: generated.pdf")
    print(f"🎯 Elementos dibujados: {elements_drawn}")
    print(f"📏 Líneas agrupadas: {len(lines)}")

if __name__ == "__main__":
    create_cv()
