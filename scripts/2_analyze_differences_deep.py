#!/usr/bin/env python3
"""
2_analyze_differences_deep.py
Análisis profundo de TODAS las diferencias entre PDFs
Genera score de similitud continuo y reporte detallado con coordenadas exactas
"""
import fitz  # PyMuPDF
import json
import numpy as np
from collections import defaultdict
import sys
from PIL import Image

def extract_all_elements(pdf_path):
    """Extrae TODOS los elementos con coordenadas, fuentes y colores exactos"""
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    elements = []
    text_dict = page.get_text('dict')
    
    for block in text_dict['blocks']:
        if 'lines' not in block:
            continue
            
        for line in block['lines']:
            for span in line['spans']:
                elem = {
                    'text': span['text'],
                    'x': round(span['bbox'][0], 2),
                    'y': round(span['bbox'][1], 2),
                    'x2': round(span['bbox'][2], 2),
                    'y2': round(span['bbox'][3], 2),
                    'width': round(span['bbox'][2] - span['bbox'][0], 2),
                    'height': round(span['bbox'][3] - span['bbox'][1], 2),
                    'font': span['font'],
                    'size': round(span['size'], 2),
                    'color': span['color']
                }
                elements.append(elem)
    
    doc.close()
    return elements

def calculate_pixel_similarity(gen_pdf, obj_pdf):
    """Calcula similitud pixel-a-pixel entre PDFs"""
    gen_doc = fitz.open(gen_pdf)
    obj_doc = fitz.open(obj_pdf)
    
    # Renderizar a alta resolución
    zoom = 2.0
    mat = fitz.Matrix(zoom, zoom)
    
    gen_pix = gen_doc[0].get_pixmap(matrix=mat)
    obj_pix = obj_doc[0].get_pixmap(matrix=mat)
    
    # Convertir a PIL Images
    gen_img = Image.frombytes('RGB', [gen_pix.width, gen_pix.height], gen_pix.samples)
    obj_img = Image.frombytes('RGB', [obj_pix.width, obj_pix.height], obj_pix.samples)
    
    # CORREGIR: Redimensionar generado al tamaño del objetivo si son diferentes
    if gen_img.size != obj_img.size:
        gen_img = gen_img.resize(obj_img.size, Image.Resampling.LANCZOS)
    
    # Convertir a numpy arrays
    gen_arr = np.array(gen_img)
    obj_arr = np.array(obj_img)
    
    # Calcular diferencia absoluta
    diff = np.abs(gen_arr.astype(float) - obj_arr.astype(float))
    max_diff = 255.0 * 3  # RGB channels
    
    # Score de similitud (0.0 a 1.0)
    pixel_similarity = 1.0 - (np.mean(diff) / max_diff)
    
    gen_doc.close()
    obj_doc.close()
    
    return pixel_similarity

def find_matching_element(elem, candidates, tolerance=100.0):
    """
    Encuentra el elemento más cercano en la lista de candidatos
    Versión permisiva: solo requiere texto igual
    """
    best_match = None
    best_dist = float('inf')
    
    elem_text = elem['text'].strip()
    
    if not elem_text:  # Ignorar elementos vacíos
        return None
    
    for cand in candidates:
        cand_text = cand['text'].strip()
        
        # Match por texto (debe ser EXACTO)
        if elem_text != cand_text:
            continue
        
        # Calcular distancia espacial
        dx = abs(elem['x'] - cand['x'])
        dy = abs(elem['y'] - cand['y'])
        dist = np.sqrt(dx**2 + dy**2)
        
        # Buscar el candidato más cercano espacialmente
        if dist < best_dist:
            best_dist = dist
            best_match = cand
    
    return best_match if best_dist < tolerance else None

def analyze_sections(gen_elements, obj_elements):
    """Agrupa elementos por sección y calcula métricas detalladas"""
    
    # Keywords para clasificación de secciones
    section_keywords = {
        'HEADER': ['Nicolás', 'Ignacio', 'Fredes', 'Franco'],
        'CONTACT': ['phone', 'email', '@', 'github', 'linkedin', 'twitter', 'Viña', 'Chile'],
        'EDUCATION': ['EDUCATION', 'University', 'B.S.', 'M.S.', 'Federico', 'Valparaíso', 'GPA'],
        'PAPERS': ['PAPERS', 'WORKSHOPS', 'IEEE', 'NeurIPS', 'HGAN'],
        'SKILLS': ['SKILLS', 'PROGRAMMING', 'LANGUAGES', 'FRAMEWORKS', 'CLOUD', 'CONCEPTS', 
                   'Python', 'C++', 'PyTorch', 'TensorFlow', 'Vertex', 'Google-ADK'],
        'LANGUAGE': ['Spanish', 'English', 'Native', 'CEFR'],
        'EXPERIENCE': ['EXPERIENCE'],
        'JOBSITY': ['JOBSITY', 'Jobsity'],
        'ZENTA': ['ZENTA'],
        'DEUNA': ['DEUNA', 'Mexico'],
        'SPOT': ['SPOT'],
        'EPAM': ['EPAM'],
        'WALMART': ['WALMART'],
        'LAMNGEN': ['LAMNGEN', 'Lamngen']
    }
    
    def classify_element(elem):
        text = elem['text']
        for section, keywords in section_keywords.items():
            if any(kw in text for kw in keywords):
                return section
        return 'OTHER'
    
    # Clasificar elementos
    gen_sections = defaultdict(list)
    obj_sections = defaultdict(list)
    
    for elem in gen_elements:
        section = classify_element(elem)
        gen_sections[section].append(elem)
    
    for elem in obj_elements:
        section = classify_element(elem)
        obj_sections[section].append(elem)
    
    return dict(gen_sections), dict(obj_sections)

def analyze_differences_comprehensive(gen_path, obj_path):
    """
    Análisis exhaustivo y detallado de diferencias
    Retorna score continuo de 0.0 a 1.0 y reporte completo
    """
    print("=" * 100)
    print("ANÁLISIS PROFUNDO DE DIFERENCIAS - CV PIXEL-PERFECT")
    print("=" * 100)
    
    # 1. Extracción de elementos
    print("\n[1/4] Extrayendo elementos textuales...")
    gen_elements = extract_all_elements(gen_path)
    obj_elements = extract_all_elements(obj_path)
    
    print(f"   📊 Generado: {len(gen_elements)} elementos")
    print(f"   📊 Objetivo: {len(obj_elements)} elementos")
    
    # 2. Similitud pixel-a-pixel
    print("\n[2/4] Calculando similitud pixel-a-pixel...")
    pixel_score = calculate_pixel_similarity(gen_path, obj_path)
    print(f"   🎯 Similitud de píxeles: {pixel_score*100:.4f}%")
    
    # 3. Clasificación por secciones
    print("\n[3/4] Clasificando por secciones...")
    gen_sections, obj_sections = analyze_sections(gen_elements, obj_elements)
    
    all_sections = sorted(set(list(gen_sections.keys()) + list(obj_sections.keys())))
    
    # 4. Análisis detallado por sección
    print("\n[4/4] Analizando diferencias por sección...")
    
    section_scores = {}
    section_deltas = {}
    detailed_diffs = {}
    
    for section in all_sections:
        gen_sec = gen_sections.get(section, [])
        obj_sec = obj_sections.get(section, [])
        
        print(f"\n{'─' * 100}")
        print(f"SECCIÓN: {section}")
        print(f"{'─' * 100}")
        print(f"   Generado: {len(gen_sec)} elementos | Objetivo: {len(obj_sec)} elementos")
        
        if len(obj_sec) == 0:
            section_scores[section] = 1.0 if len(gen_sec) == 0 else 0.0
            continue
        
        # Analizar cada elemento del objetivo
        matched = 0
        total_dx = 0
        total_dy = 0
        position_errors = []
        
        for obj_elem in obj_sec:
            match = find_matching_element(obj_elem, gen_sec)
            
            if match:
                matched += 1
                dx = match['x'] - obj_elem['x']
                dy = match['y'] - obj_elem['y']
                total_dx += dx
                total_dy += dy
                
                error = np.sqrt(dx**2 + dy**2)
                position_errors.append(error)
                
                if error > 1.0:  # Solo reportar desviaciones significativas
                    print(f"   ⚠️  '{obj_elem['text'][:30]}...' - Δx:{dx:+.2f}, Δy:{dy:+.2f}, dist:{error:.2f}pts")
        
        # Calcular score de la sección
        content_score = matched / len(obj_sec)
        
        if position_errors:
            avg_error = np.mean(position_errors)
            # Score de posición: decrece exponencialmente con el error
            # Error de 0pts = 1.0, Error de 5pts ≈ 0.37, Error de 10pts ≈ 0.13
            position_score = np.exp(-avg_error / 5.0)
        else:
            position_score = 1.0 if matched == len(obj_sec) else 0.0
        
        # Score combinado (70% contenido, 30% posición)
        section_score = 0.7 * content_score + 0.3 * position_score
        section_scores[section] = section_score
        
        # Deltas promedio
        if matched > 0:
            avg_dx = total_dx / matched
            avg_dy = total_dy / matched
            section_deltas[section] = {'dx': avg_dx, 'dy': avg_dy}
            
            print(f"   📍 Match: {matched}/{len(obj_sec)} ({content_score*100:.1f}%)")
            print(f"   📐 Δx promedio: {avg_dx:+.3f}pts | Δy promedio: {avg_dy:+.3f}pts")
            print(f"   🎯 Score sección: {section_score*100:.2f}%")
        else:
            section_deltas[section] = {'dx': 0.0, 'dy': 0.0}
            print(f"   ❌ Sin matches")
    
    # Score global
    if section_scores:
        structural_score = np.mean(list(section_scores.values()))
    else:
        structural_score = 0.0
    
    # Score final combinado (50% píxeles, 50% estructura)
    global_score = 0.5 * pixel_score + 0.5 * structural_score
    
    print(f"\n{'=' * 100}")
    print(f"RESULTADOS FINALES")
    print(f"{'=' * 100}")
    print(f"   🎨 Score Píxeles:     {pixel_score*100:.4f}%")
    print(f"   🏗️  Score Estructura:  {structural_score*100:.4f}%")
    print(f"   🌟 SCORE GLOBAL:      {global_score*100:.4f}%")
    print(f"{'=' * 100}\n")
    
    # Generar reporte JSON
    report = {
        'global_score': global_score,
        'pixel_score': pixel_score,
        'structural_score': structural_score,
        'section_scores': section_scores,
        'section_deltas': section_deltas,
        'element_counts': {
            'generated': len(gen_elements),
            'objective': len(obj_elements)
        }
    }
    
    # Guardar en el directorio padre si se ejecuta desde scripts/
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    report_path = os.path.join(parent_dir, 'analysis_report.json')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Reporte guardado: {report_path}\n")
    
    return report

if __name__ == "__main__":
    import os
    
    # Determinar rutas relativas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    gen_pdf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(parent_dir, 'outputs', 'Nicolas_Fredes_CV.pdf')
    obj_pdf = sys.argv[2] if len(sys.argv) > 2 else os.path.join(parent_dir, 'Objetivo_No_editar.pdf')
    
    analyze_differences_comprehensive(gen_pdf, obj_pdf)

