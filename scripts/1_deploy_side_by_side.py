#!/usr/bin/env python3
"""
1_deploy_side_by_side.py
Despliega el PDF generado y el objetivo lado a lado para comparación visual
"""
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import sys

def deploy_side_by_side(generated_path, objective_path, output_path, zoom=3.0):
    """
    Genera comparación lado a lado de alta resolución
    
    Args:
        generated_path: Path al PDF generado
        objective_path: Path al PDF objetivo
        output_path: Path donde guardar la comparación
        zoom: Factor de zoom (por defecto 3.0 para alta resolución)
    """
    print(f"📄 Abriendo PDFs...")
    gen_doc = fitz.open(generated_path)
    obj_doc = fitz.open(objective_path)
    
    # Renderizar con alta resolución
    mat = fitz.Matrix(zoom, zoom)
    
    gen_pix = gen_doc[0].get_pixmap(matrix=mat)
    obj_pix = obj_doc[0].get_pixmap(matrix=mat)
    
    # Convertir a PIL Images
    gen_img = Image.frombytes('RGB', [gen_pix.width, gen_pix.height], gen_pix.samples)
    obj_img = Image.frombytes('RGB', [obj_pix.width, obj_pix.height], obj_pix.samples)
    
    # Crear composición
    margin = 60
    header_height = 120
    total_width = gen_img.width + obj_img.width + margin * 3
    total_height = max(gen_img.height, obj_img.height) + header_height + margin * 2
    
    composite = Image.new('RGB', (total_width, total_height), 'white')
    draw = ImageDraw.Draw(composite)
    
    # Cargar fuente
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Títulos
    draw.text((margin, 30), "GENERADO", fill='#FF0000', font=font_large)
    draw.text((gen_img.width + margin * 2, 30), "OBJETIVO", fill='#00AA00', font=font_large)
    
    # Subtítulos con paths
    draw.text((margin, 85), generated_path.split('/')[-1], fill='#666666', font=font_small)
    draw.text((gen_img.width + margin * 2, 85), objective_path.split('/')[-1], fill='#666666', font=font_small)
    
    # Pegar imágenes
    composite.paste(gen_img, (margin, header_height))
    composite.paste(obj_img, (gen_img.width + margin * 2, header_height))
    
    # Línea divisoria
    draw.line([(gen_img.width + margin * 2 - 5, header_height), 
               (gen_img.width + margin * 2 - 5, total_height - margin)], 
              fill='#CCCCCC', width=3)
    
    # Guardar
    composite.save(output_path, quality=95, optimize=False)
    
    gen_doc.close()
    obj_doc.close()
    
    print(f"✅ Comparación guardada: {output_path}")
    print(f"   Resolución: {total_width}x{total_height}px")
    return output_path

if __name__ == "__main__":
    gen_pdf = sys.argv[1] if len(sys.argv) > 1 else "Nicolas_Fredes_CV.pdf"
    obj_pdf = sys.argv[2] if len(sys.argv) > 2 else "Objetivo_No_editar.pdf"
    out_img = sys.argv[3] if len(sys.argv) > 3 else "comparison.png"
    
    deploy_side_by_side(gen_pdf, obj_pdf, out_img)
