#!/usr/bin/env python3
"""
1_deploy_side_by_side.py
Despliega el PDF generado y el objetivo lado a lado para comparación visual
"""
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
import sys

def deploy_side_by_side(generated_path, objective_path, output_path, zoom=3.0, region=None):
    """
    Genera comparación lado a lado de alta resolución con crop opcional
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
    
    # Crop logic
    if region == 'left':
        # Crop Left Column (approx 0 to 200pts * zoom)
        # Adding some margin (220pts)
        crop_width = int(220 * zoom)
        crop_box = (0, 0, crop_width, gen_img.height)
        gen_img = gen_img.crop(crop_box)
        obj_img = obj_img.crop(crop_box)
    elif region == 'right':
        # Crop Right Column (approx 200 to end)
        crop_start = int(190 * zoom)
        crop_box = (crop_start, 0, gen_img.width, gen_img.height)
        gen_img = gen_img.crop(crop_box)
        obj_img = obj_img.crop(crop_box)
    elif region == 'full':
        # No crop
        pass
    
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
    title_suffix = f" ({region.upper()})" if region else ""
    draw.text((margin, 30), f"GENERADO{title_suffix}", fill='#FF0000', font=font_large)
    if region == 'left':
        # Adjust objective title position for narrow left column comparison
        draw.text((gen_img.width + margin * 2, 30), "OBJETIVO", fill='#00AA00', font=font_large)
    else:
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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('gen_pdf', nargs='?', default="Nicolas_Fredes_CV.pdf")
    parser.add_argument('obj_pdf', nargs='?', default="Objetivo_No_editar.pdf")
    parser.add_argument('out_img', nargs='?', default="comparison.png")
    parser.add_argument('--region', choices=['left', 'right', 'full'], help='Region to crop')
    
    args = parser.parse_args()
    
    deploy_side_by_side(args.gen_pdf, args.obj_pdf, args.out_img, region=args.region)
