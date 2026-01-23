#!/usr/bin/env python3
"""
3_generate_cv_precise.py
Generador de CV usando coordenadas EXACTAS del objetivo
Implementa sistema de corrección automática de offsets
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json
import sys

# Configuración de fuentes
FONT_PATHS = {
    'TrebuchetMS': '/home/nicofredes/.fonts/trebuc.ttf',
    'TrebuchetMS-Bold': '/home/nicofredes/.fonts/trebucbd.ttf',
    'TrebuchetMS-Italic': '/home/nicofredes/.fonts/trebucit.ttf',
}

# Registrar fuentes
fonts_loaded = []
for font_name, font_path in FONT_PATHS.items():
    try:
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        fonts_loaded.append(font_name)
    except Exception as e:
        print(f"⚠️  No se pudo cargar fuente {font_name}: {e}")

if fonts_loaded:
    print(f"✅ Fuentes cargadas: {', '.join(fonts_loaded)}")
else:
    print("❌ No se cargaron fuentes personalizadas, usando fuentes por defecto")

# Parámetros de transformación (ajustables por el iterador)
GLOBAL_X_OFFSET = 0.0   # Desplazamiento horizontal global
GLOBAL_Y_OFFSET = 0.0   # Desplazamiento vertical global  
SCALE_FACTOR = 1.0      # Factor de escala global

def rgb_from_int(color_int):
    """Convierte color entero a tupla RGB normalizada (0.0-1.0)"""
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    return (r/255.0, g/255.0, b/255.0)

def generate_cv_from_coords(coords_file, output_pdf, config=None):
    """
    Genera PDF usando coordenadas exactas del archivo JSON
    
    Args:
        coords_file: Path al JSON con coordenadas del objetivo
        output_pdf: Path del PDF de salida
        config: Dict con configuración de transformación (opcional)
    """
    # Cargar configuración (usar variables locales, no modificar globales)
    x_offset = GLOBAL_X_OFFSET
    y_offset = GLOBAL_Y_OFFSET
    scale_factor = SCALE_FACTOR
    
    if config:
        x_offset = config.get('x_offset', x_offset)
        y_offset = config.get('y_offset', y_offset)
        scale_factor = config.get('scale', scale_factor)
    
    # Cargar coordenadas
    with open(coords_file, 'r', encoding='utf-8') as f:
        elements = json.load(f)
    
    print(f"\n{'='*80}")
    print(f"GENERANDO CV DESDE COORDENADAS")
    print(f"{'='*80}")
    print(f"Archivo de coordenadas: {coords_file}")
    print(f"Total de elementos: {len(elements)}")
    print(f"Configuración:")
    print(f"  - X Offset: {x_offset:+.2f}pts")
    print(f"  - Y Offset: {y_offset:+.2f}pts")
    print(f"  - Scale: {scale_factor:.4f}")
    print(f"{'='*80}\n")
    
    # Crear canvas
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4  # 595.27 x 841.89 pts
    
    # Estadísticas
    elements_drawn = 0
    font_fallbacks = 0
    
    for i, elem in enumerate(elements):
        text = elem['text']
        
        # Coordenadas originales del JSON
        x_orig = elem['x']
        y_orig = elem['y']
        
        # Transformación de coordenadas:
        # El JSON tiene coordenadas PDF estándar (origen arriba-izquierda, Y crece hacia abajo)
        # ReportLab usa origen abajo-izquierda, Y crece hacia arriba
        # Fórmula: y_reportlab = height - y_pdf
        
        x = x_orig + x_offset
        
        # Calcular offset Y total (Global + Sección)
        y_section_offset = 0.0
        if config and 'sections' in config:
            from cv_utils import classify_element
            section = classify_element(elem)
            if section in config['sections']:
                sec_config = config['sections'][section]
                x += sec_config.get('x', 0.0)
                y_section_offset = sec_config.get('y', 0.0)
        
        y = (height - y_orig) - (y_offset + y_section_offset)   # NOTA: RESTAR ambos offsets
        
        # Tamaño de fuente
        size = elem['size']
        
        # Determinar fuente
        font_family = elem.get('font', 'TrebuchetMS')
        is_bold = elem.get('bold', False)
        is_italic = elem.get('italic', False)
        
        # Mapeo de fuentes
        if 'Bold' in font_family or is_bold:
            font_name = 'TrebuchetMS-Bold'
        elif 'Italic' in font_family or is_italic:
            font_name = 'TrebuchetMS-Italic'
        else:
            if 'TrebuchetMS' in font_family:
                font_name = 'TrebuchetMS'
            else:
                # Fonts como AbyssinicaSIL-Regular -> usar Trebuchet como fallback
                font_name = 'TrebuchetMS'
        
        # Setear fuente
        try:
            c.setFont(font_name, size)
        except:
            # Fallback a Helvetica si falla
            font_fallbacks += 1
            if is_bold:
                c.setFont('Helvetica-Bold', size)
            elif is_italic:
                c.setFont('Helvetica-Oblique', size)
            else:
                c.setFont('Helvetica', size)
        
        # Color
        color = elem.get('color', 0)
        rgb = rgb_from_int(color)
        c.setFillColorRGB(*rgb)
        
        # Dibujar texto
        try:
            c.drawString(x, y, text)
            elements_drawn += 1
        except Exception as e:
            print(f"⚠️  Error al dibujar elemento {i}: {e}")
    
    # Guardar PDF
    c.save()
    
    print(f"\n{'='*80}")
    print(f"CV GENERADO EXITOSAMENTE")
    print(f"{'='*80}")
    print(f"Archivo: {output_pdf}")
    print(f"Elementos dibujados: {elements_drawn}/{len(elements)}")
    if font_fallbacks > 0:
        print(f"⚠️  Fuente fallbacks: {font_fallbacks}")
    print(f"{'='*80}\n")
    
    return output_pdf

if __name__ == "__main__":
    import os
    
    # Determinar rutas basadas en la ubicación del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    coords_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(parent_dir, "objetivo_coords.json")
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else os.path.join(parent_dir, "outputs", "Nicolas_Fredes_CV.pdf")
    config_file = os.path.join(parent_dir, 'generation_config.json')
    
    # Cargar configuración desde archivo si existe
    config = None
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            print(f"📋 Configuración cargada desde {config_file}")
    except:
        pass
    
    generate_cv_from_coords(coords_file, output_pdf, config)

