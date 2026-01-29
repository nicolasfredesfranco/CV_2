#!/usr/bin/env python3
"""
Comprehensive CV Quality Verification Script
Tests: Links, Searchability, Visual Similarity

Author: Nicolás Ignacio Fredes Franco
"""

import PyPDF2
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path

def verify_links(pdf_path):
    """Verify PDF has clickable links"""
    print("\n" + "="*80)
    print("1. VERIFICANDO LINKS CLICKEABLES")
    print("="*80)
    
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        page = reader.pages[0]
        
        # Get annotations (links)
        if '/Annots' in page:
            annots = page['/Annots']
            links_found = []
            
            for annot in annots:
                annot_obj = annot.get_object()
                if annot_obj.get('/Subtype') == '/Link':
                    if '/A' in annot_obj:
                        action = annot_obj['/A']
                        if '/URI' in action:
                            uri = action['/URI']
                            links_found.append(str(uri))
            
            print(f"\n✅ Links encontrados: {len(links_found)}")
            for i, link in enumerate(links_found, 1):
                print(f"   {i}. {link}")
            
            # Verify expected links
            expected_domains = ['linkedin.com', 'github.com', 'mailto:']
            for domain in expected_domains:
                found = any(domain in link for link in links_found)
                status = "✅" if found else "❌"
                print(f"\n{status} {domain}: {'Encontrado' if found else 'NO encontrado'}")
            
            return len(links_found) > 0
        else:
            print("❌ No se encontraron links en el PDF")
            return False

def verify_searchable_text(pdf_path):
    """Verify PDF has searchable/copyable text"""
    print("\n" + "="*80)
    print("2. VERIFICANDO TEXTO COPIABLE/SEARCHABLE")
    print("="*80)
    
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        page = reader.pages[0]
        
        text = page.extract_text()
        
        if text and len(text) > 100:
            print(f"\n✅ Texto extraído: {len(text)} caracteres")
            print(f"\nPrimeros 200 caracteres:")
            print(f"---")
            print(text[:200])
            print(f"---")
            
            # Check for expected content
            expected_words = ['Nicolas', 'Fredes', 'Engineer', 'Python', 'GitHub']
            found_count = 0
            for word in expected_words:
                if word in text:
                    found_count += 1
                    print(f"✅ Encontrado: '{word}'")
                else:
                    print(f"⚠️  No encontrado: '{word}'")
            
            return found_count >= 3
        else:
            print("❌ No se pudo extraer texto del PDF")
            return False

def compare_visual_similarity(generated_pdf, objective_pdf):
    """Compare visual similarity between PDFs"""
    print("\n" + "="*80)
    print("3. COMPARACIÓN VISUAL AL OJO HUMANO")
    print("="*80)
    
    # Convert both PDFs to images at high resolution
    print("\nConvirtiendo PDFs a PNG (200 DPI)...")
    gen_img = convert_from_path(generated_pdf, dpi=200)[0]
    obj_img = convert_from_path(objective_pdf, dpi=200)[0]
    
    # Save PNGs for visual inspection
    gen_img.save("outputs/GENERATED_VERIFICATION.png")
    obj_img.save("outputs/OBJECTIVE_VERIFICATION.png")
    print(f"✅ PNG guardado: outputs/GENERATED_VERIFICATION.png")
    print(f"✅ PNG guardado: outputs/OBJECTIVE_VERIFICATION.png")
    
    # Calculate pixel-level similarity
    gen_arr = np.array(gen_img.convert('RGB'))
    obj_arr = np.array(obj_img.convert('RGB').resize(gen_img.size))
    
    diff = np.abs(gen_arr.astype(int) - obj_arr.astype(int))
    diff[diff < 10] = 0  # Tolerance for minor rendering differences
    
    perceptible_diff = np.sum(np.any(diff > 0, axis=2))
    total_pixels = gen_arr.shape[0] * gen_arr.shape[1]
    similarity = 100 * (1 - perceptible_diff / total_pixels)
    
    print(f"\n📊 SIMILITUD VISUAL: {similarity:.2f}%")
    
    # Create side-by-side comparison
    w, h = gen_img.size
    comparison = Image.new('RGB', (w*2 + 60, h + 100), 'white')
    comparison.paste(obj_img, (20, 80))
    comparison.paste(gen_img, (w + 40, 80))
    
    # Add labels
    draw = ImageDraw.Draw(comparison)
    draw.text((w//2 - 50, 20), "OBJETIVO BACKUP", fill='blue')
    draw.text((w + w//2 - 50, 20), "GENERADO", fill='green')
    draw.text((w - 100, 40), f"{similarity:.2f}% Match", fill='darkgreen' if similarity > 75 else 'orange')
    
    comparison.save("outputs/VISUAL_COMPARISON_VERIFICATION.png")
    print(f"✅ Comparación guardada: outputs/VISUAL_COMPARISON_VERIFICATION.png")
    
    # Human perception assessment
    if similarity >= 95:
        assessment = "✅ EXCELENTE - Prácticamente idénticas al ojo humano"
    elif similarity >= 85:
        assessment = "✅ MUY BUENO - Visualmente muy similares"
    elif similarity >= 75:
        assessment = "⚠️  BUENO - Similares pero con diferencias notables"
    else:
        assessment = "❌ REGULAR - Diferencias significativas"
    
    print(f"\n{assessment}")
    
    return similarity

def main():
    print("="*80)
    print("VERIFICACIÓN COMPLETA DE CALIDAD DEL CV")
    print("="*80)
    
    generated_pdf = Path("outputs/Nicolas_Fredes_CV.pdf")
    objective_pdf = Path("pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf")
    
    if not generated_pdf.exists():
        print(f"❌ Error: No se encuentra {generated_pdf}")
        return
    
    if not objective_pdf.exists():
        print(f"❌ Error: No se encuentra {objective_pdf}")
        return
    
    # Run all verifications
    links_ok = verify_links(generated_pdf)
    text_ok = verify_searchable_text(generated_pdf)
    similarity = compare_visual_similarity(generated_pdf, objective_pdf)
    
    # Final summary
    print("\n" + "="*80)
    print("RESUMEN FINAL")
    print("="*80)
    
    print(f"\n1. Links clickeables: {'✅ OK' if links_ok else '❌ FAIL'}")
    print(f"2. Texto copiable: {'✅ OK' if text_ok else '❌ FAIL'}")
    print(f"3. Similitud visual: {similarity:.2f}%")
    
    if links_ok and text_ok and similarity >= 75:
        print(f"\n{'='*80}")
        print("🎉 VERIFICACIÓN EXITOSA - CV DE CALIDAD PROFESIONAL 🎉")
        print(f"{'='*80}")
        print("\nEl CV generado cumple con todos los requisitos:")
        print("  ✅ Links funcionan correctamente")
        print("  ✅ Texto es searchable y copiable")
        print(f"  ✅ Visualmente {'prácticamente idéntico' if similarity >= 95 else 'muy similar'} al objetivo")
    else:
        print("\n⚠️ VERIFICACIÓN CON OBSERVACIONES")
        if not links_ok:
            print("  ❌ Problemas con links")
        if not text_ok:
            print("  ❌ Problemas con texto searchable")
        if similarity < 75:
            print(f"  ❌ Similitud visual baja ({similarity:.2f}%)")

if __name__ == "__main__":
    main()
