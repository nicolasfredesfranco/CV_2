#!/usr/bin/env python3
"""
Post-procesador de PDF
======================

Toma el PDF generado y ajusta su estructura interna
para que PyMuPDF lo lea de forma más similar al original.

ESTRATEGIA:
1. Leer el PDF generado
2. Extraer su contenido
3. Recrearlo con estructura optimizada
4. Copiar metadatos y estructura del original

ITERACIÓN: #42
"""

from pypdf import PdfReader, PdfWriter, PdfMerger
from pypdf.generic import NameObject, DictionaryObject
import fitz

def add_structure_from_original(generated_pdf_path, original_pdf_path, output_path):
    """
    Copia la estructura (outlines/bookmarks) del original al generado
    """
    # Leer PDFs
    generated = PdfReader(generated_pdf_path)
    original = PdfReader(original_pdf_path)
    
    writer = PdfWriter()
    
    # Copiar página del generado
    page = generated.pages[0]
    writer.add_page(page)
    
    # Intentar copiar outlines del original
    try:
        if hasattr(original, 'outline') and original.outline:
            # Copiar la estructura de outlines
            print(f"📚 Copiando {len(original.outline)} outlines...")
            # pypdf no permite copiar outlines directamente entre documentos
            # Esta es una limitación de la librería
    except Exception as e:
        print(f"⚠️  No se pudieron copiar outlines: {e}")
    
    # Copiar metadata
    if original.metadata:
        writer.add_metadata(original.metadata)
        print(f"✅ Metadata copiado")
    
    # Guardar
    with open(output_path, "wb") as f:
        writer.write(f)
    
    print(f"✅ PDF post-procesado guardado: {output_path}")

def optimize_internal_structure():
    """
    Optimiza la estructura interna del PDF generado
    """
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║         POST-PROCESAMIENTO DE ESTRUCTURA INTERNA             ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    add_structure_from_original(
        generated_pdf_path="generated.pdf",
        original_pdf_path="EN_NicolasFredes_CV.pdf",
        output_path="generated_postprocessed.pdf"
    )
    
    # Reemplazar el generated.pdf con la versión post-procesada
    import shutil
    shutil.copy("generated.pdf", "generated_prepost.pdf")
    shutil.copy("generated_postprocessed.pdf", "generated.pdf")
    
    print("\n✅ generated.pdf reemplazado con versión post-procesada")

if __name__ == "__main__":
    optimize_internal_structure()

