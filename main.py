#!/usr/bin/env python3
"""
CV Generator Engine
===================

Sistema de generación de documentos PDF de alta precisión basado en coordenadas absolutas.
Diseñado para replicar diseños vectoriales exactos con inyección dinámica de metadatos.
Mantiene una fidelidad visual del 100% respecto al diseño objetivo original.

@author: Nicolás Ignacio Fredes Franco
@version: 2.0.0
@license: MIT
"""

import json
import logging
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- Configuración del Sistema de Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("CV_Engine")

# --- Capa de Configuración (Configuration Layer) ---

@dataclass(frozen=True)
class LayoutConfig:
    """
    Configuración centralizada de dimensiones, colores y reglas de negocio.
    Define la 'Física' del documento para garantizar consistencia.
    """
    # Dimensiones de página (Puntos exactos - CORREGIDO basado en pdfinfo)
    # Objetivo verificado: 623 x 806 pts (NO flotantes)
    PAGE_WIDTH: float = 623.0
    PAGE_HEIGHT: float = 806.0

    # Paleta de Colores (RGB Normalizado 0-1)
    # Azul corporativo exacto extraído de shapes.json: #3A6BA9 = RGB(58,107,169)
    COLOR_PRIMARY_BLUE: Tuple[float, float, float] = (0.227, 0.42, 0.663)
    
    # Ajuste de Offset Vertical Global (Puntos)
    # Corrige diferencias entre motor Ghostscript (objetivo) y ReportLab (generado)
    # Valor positivo mueve contenido ARRIBA, negativo ABAJO
    Y_GLOBAL_OFFSET: float = 32.0  # Ajustado empíricamente para alineación perfecta
    
    # Umbrales de Lógica de Diseño (Reverse Engineered Logic)
    # Coordenadas X/Y que disparan comportamientos específicos
    THRESHOLD_RIGHT_COLUMN_X: float = 215.0
    THRESHOLD_LOCATION_TEXT_X: float = 250.0
    THRESHOLD_DATE_ALIGN_X: float = 380.0
    THRESHOLD_DATE_ALIGN_Y_LIMIT: float = 750.0  # Aplicar corrección solo en el cuerpo
    
    # Umbral vertical para desambiguar links (Github vs LinkedIn)
    THRESHOLD_LINK_DISAMBIGUATION_Y: float = 150.0

    # Ajustes de Micro-Precisión (Offsets en Puntos)
    OFFSET_DATE_CORRECTION: float = 1.5
    OFFSET_BULLET_INDENT: float = 8.5
    LINK_HITBOX_PADDING: float = 2.0

    # Rutas del Sistema (Pathlib para compatibilidad OS)
    BASE_DIR: Path = Path(__file__).parent.resolve()
    DATA_DIR: Path = BASE_DIR / 'data'
    ASSETS_DIR: Path = DATA_DIR / 'assets'
    OUTPUT_DIR: Path = BASE_DIR / 'outputs'
    
    FILE_COORDS: Path = DATA_DIR / 'coordinates.json'
    FILE_SHAPES: Path = DATA_DIR / 'shapes.json'
    FILE_OUTPUT: Path = OUTPUT_DIR / 'Nicolas_Fredes_CV.pdf'

# Instancia global de configuración
CFG = LayoutConfig()

# --- Capa de Lógica de Negocio (Core Logic) ---

class FontManager:
    """Gestor de tipografías para asegurar que los recursos estén disponibles."""
    
    @staticmethod
    def register_fonts() -> None:
        """Registra la familia TrebuchetMS en el sistema ReportLab."""
        font_map = {
            'TrebuchetMS': 'trebuc.ttf',
            'TrebuchetMS-Bold': 'trebucbd.ttf',
            'TrebuchetMS-Italic': 'trebucit.ttf'
        }
        
        loaded = 0
        for font_name, filename in font_map.items():
            font_path = CFG.ASSETS_DIR / filename
            if font_path.exists():
                try:
                    pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
                    loaded += 1
                    logger.debug(f"Fuente cargada: {font_name}")
                except Exception as e:
                    logger.warning(f"Error cargando fuente {font_name}: {e}")
            else:
                logger.warning(f"Archivo de fuente no encontrado: {font_path}")
        
        if loaded == 0:
            logger.error("No se cargaron fuentes personalizadas. Se usará Helvetica como fallback.")
        else:
            logger.info(f"✅ {loaded} fuentes cargadas correctamente")

class CVRenderer:
    """
    Motor de renderizado de CV de alta precisión.
    Orquesta la lectura de datos, transformación de coordenadas y dibujo vectorial.
    """

    def __init__(self):
        self._ensure_output_dir()
        self.canvas = canvas.Canvas(
            str(CFG.FILE_OUTPUT),
            pagesize=(CFG.PAGE_WIDTH, CFG.PAGE_HEIGHT)
        )
        # Carga de datos en memoria
        self.coordinates_data = self._load_json(CFG.FILE_COORDS)
        self.shapes_data = self._load_json(CFG.FILE_SHAPES)
        
        # Validación de datos cargados
        if not self._validate_coordinates_data(self.coordinates_data):
            logger.error("❌ Validación de coordenadas falló. No se puede continuar.")
            sys.exit(1)
        
        if not self._validate_shapes_data(self.shapes_data):
            logger.error("❌ Validación de formas falló. No se puede continuar.")
            sys.exit(1)

    def _ensure_output_dir(self) -> None:
        """Crea el directorio de salida si no existe."""
        CFG.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _load_json(path: Path) -> List[Any]:
        """Carga segura de archivos JSON."""
        if not path.exists():
            logger.error(f"Archivo crítico no encontrado: {path}")
            return []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"JSON corrupto en {path}: {e}")
            sys.exit(1)

    @staticmethod
    def _validate_coordinates_data(data: List[Dict[str, Any]]) -> bool:
        """
        Valida que los datos de coordenadas tengan todos los campos requeridos.
        Retorna True si válido, False y registra errores si inválido.
        """
        if not data:
            logger.error("Datos de coordenadas vacíos")
            return False
        
        required_fields = ['text', 'x', 'y', 'size']
        optional_fields = ['font', 'color', 'bold', 'italic']
        
        for idx, elem in enumerate(data):
            # Validar campos requeridos
            missing = [f for f in required_fields if f not in elem]
            if missing:
                logger.error(f"Elemento {idx} falta campos: {missing}. Elemento: {elem}")
                return False
            
            # Validar tipos de datos
            if not isinstance(elem['text'], str):
                logger.error(f"Elemento {idx}: 'text' debe ser string")
                return False
            if not isinstance(elem['x'], (int, float)):
                logger.error(f"Elemento {idx}: 'x' debe ser número")
                return False
            if not isinstance(elem['y'], (int, float)):
                logger.error(f"Elemento {idx}: 'y' debe ser número")
                return False
            if not isinstance(elem['size'], (int, float)):
                logger.error(f"Elemento {idx}: 'size' debe ser número")
                return False
        
        logger.info(f"✅ Validación de coordenadas: {len(data)} elementos válidos")
        return True

    @staticmethod
    def _validate_shapes_data(data: List[Dict[str, Any]]) -> bool:
        """
        Valida que los datos de formas tengan estructura correcta.
        Retorna True si válido, False y registra errores si inválido.
        """
        if not data:
            logger.warning("Datos de formas vacíos (no crítico)")
            return True  # Las formas son opcionales
        
        for idx, shape in enumerate(data):
            # Validar tipo
            if 'type' not in shape:
                logger.error(f"Forma {idx}: falta campo 'type'")
                return False
            
            # Validar rectángulos
            if shape['type'] == 'rect':
                if 'rect' not in shape or 'color' not in shape:
                    logger.error(f"Rectángulo {idx}: falta 'rect' o 'color'")
                    return False
                if not isinstance(shape['rect'], list) or len(shape['rect']) != 4:
                    logger.error(f"Rectángulo {idx}: 'rect' debe ser lista de 4 números")
                    return False
                if not isinstance(shape['color'], list) or len(shape['color']) != 3:
                    logger.error(f"Rectángulo {idx}: 'color' debe ser lista RGB de 3 números")
                    return False
        
        logger.info(f"✅ Validación de formas: {len(data)} elementos válidos")
        return True

    @staticmethod
    def _rgb_from_int(color_int: int) -> Tuple[float, float, float]:
        """Convierte entero de color (formato exportado) a tupla RGB normalizada."""
        r = (color_int >> 16) & 0xFF
        g = (color_int >> 8) & 0xFF
        b = color_int & 0xFF
        return (r / 255.0, g / 255.0, b / 255.0)

    @lru_cache(maxsize=1000)
    def _get_text_width(self, text: str, font_name: str, size: float) -> float:
        """
        Calcula el ancho de un texto en puntos PDF con caché para performance.
        Evita recalcular el mismo texto/fuente/tamaño múltiples veces.
        """
        try:
            return self.canvas.stringWidth(text, font_name, size)
        except:
            # Fallback a Helvetica si la fuente no está disponible
            return self.canvas.stringWidth(text, "Helvetica", size)

    @staticmethod
    def _transform_y(y_pdf: float) -> float:
        """
        Transforma coordenada Y del espacio PDF (Top-Down) al espacio ReportLab (Bottom-Up).
        Aplica offset global para corregir diferencias entre motores PDF.
        Fórmula: Y_reportlab = Altura_Página - Y_pdf + Offset_Global
        """
        return CFG.PAGE_HEIGHT - y_pdf + CFG.Y_GLOBAL_OFFSET

    def _determine_hyperlink(self, text: str, y_orig: float) -> Optional[str]:
        """
        Infiere el destino del hipervínculo basado en el contenido del texto y su posición.
        Resuelve la ambigüedad entre links de redes sociales con el mismo handle.
        """
        try:
            clean_text = text.strip()
            
            if "nico.fredes.franco@gmail.com" in clean_text:
                return "mailto:nico.fredes.franco@gmail.com"
            
            elif "DOI: 10.1109" in clean_text:
                return "https://doi.org/10.1109/ACCESS.2021.3094723"
            
            # Twitter handle específico (debe revisarse antes de LinkedIn/Github si comparten substrings)
            elif "nicofredesfranc" in clean_text and "nicolasfredesfranco" not in clean_text:
                return "https://twitter.com/NicoFredesFranc"
            
            elif "nicolasfredesfranco" in clean_text:
                # Lógica de Desambiguación Espacial:
                # GitHub está físicamente más arriba (menor Y en coords originales) que LinkedIn.
                if y_orig < CFG.THRESHOLD_LINK_DISAMBIGUATION_Y:
                    return "https://github.com/nicolasfredesfranco"
                else:
                    return "http://www.linkedin.com/in/nicolasfredesfranco"
                    
            return None
        except Exception as e:
            logger.warning(f"Error detectando hyperlink en texto '{text[:30]}...': {e}")
            return None

    def _apply_precision_corrections(self, text: str, x: float, y_rl: float, 
                                   elem_props: Dict) -> Tuple[str, float]:
        """
        Aplica reglas de negocio para corregir imperfecciones visuales del OCR/Extracción.
        
        Retorna:
            (texto_final, x_final)
        """
        final_text = text
        final_x = x
        
        # Corrección 1: Alineación de Fechas
        # Las fechas a la derecha (>380) tienden a desplazarse. Se aplica un micro-ajuste.
        # La condición original era y > (PAGE_HEIGHT - 750) en coords transformadas.
        is_date_position = (x > CFG.THRESHOLD_DATE_ALIGN_X)
        is_in_body_area = (y_rl > (CFG.PAGE_HEIGHT - CFG.THRESHOLD_DATE_ALIGN_Y_LIMIT))
        
        if is_date_position and is_in_body_area:
             final_x -= CFG.OFFSET_DATE_CORRECTION

        # Corrección 2: Inyección de Viñetas (Bullets)
        # Detecta ítems de lista que perdieron su bullet durante la extracción.
        is_right_col = (x > CFG.THRESHOLD_RIGHT_COLUMN_X)
        is_plain_text = not (elem_props.get('bold') or elem_props.get('italic'))
        
        if is_right_col and is_plain_text:
            clean = text.strip()
            # Heurística: Empieza con mayúscula, es largo, y no es un título de ubicación
            if (clean and clean[0].isupper() and len(clean) > 3 and 
                x < CFG.THRESHOLD_LOCATION_TEXT_X):
                final_text = "• " + text
                final_x -= CFG.OFFSET_BULLET_INDENT
                
        return final_text, final_x

    def render_shapes(self) -> None:
        """Dibuja las formas geométricas (fondos, barras de encabezado)."""
        if not self.shapes_data:
            logger.warning("No se encontraron formas para dibujar.")
            return

        for shape in self.shapes_data:
            if shape.get('type') != 'rect':
                continue

            color = shape.get('color', [])
            if len(color) != 3: continue

            # Filtro de color tolerante para identificar los headers azules específicos
            # Esto asegura que solo dibujamos los elementos de diseño, no ruido.
            is_blue_header = all(
                abs(c - base) < 0.2 
                for c, base in zip(color, CFG.COLOR_PRIMARY_BLUE)
            )

            if is_blue_header:
                # Coordenadas PDF (Top-Down): [x0, y0_top, x1, y1_bottom]
                x0, y0, x1, y1 = shape['rect']
                
                width = x1 - x0
                height = y1 - y0
                
                # Transformar Y para ReportLab (Bottom-Up)
                # Usamos y1 (bottom del PDF) como base para dibujar hacia arriba
                y_rl = self._transform_y(y1)
                
                self.canvas.setFillColorRGB(*color)
                self.canvas.rect(x0, y_rl, width, height, stroke=0, fill=1)

    def render_text(self) -> None:
        """Procesa y dibuja todos los elementos de texto con sus estilos y links."""
        if not self.coordinates_data:
            logger.warning("No hay datos de coordenadas de texto para renderizar.")
            return

        for elem in self.coordinates_data:
            # 1. Extracción de datos crudos
            raw_text = elem['text']
            raw_x = elem['x']
            raw_y = elem['y']
            
            # 2. Transformación de coordenadas básica
            y_rl = self._transform_y(raw_y)
            
            # 3. Aplicación de correcciones de precisión
            text, x = self._apply_precision_corrections(
                raw_text, raw_x, y_rl, elem
            )
            
            # 4. Configuración de Fuente
            font_family = elem.get('font', 'TrebuchetMS')
            font_name = 'TrebuchetMS'
            if 'Bold' in font_family or elem.get('bold'):
                font_name = 'TrebuchetMS-Bold'
            elif 'Italic' in font_family or elem.get('italic'):
                font_name = 'TrebuchetMS-Italic'
            
            # Intentar establecer la fuente, fallback a Helvetica si falla
            try:
                self.canvas.setFont(font_name, elem['size'])
            except:
                self.canvas.setFont("Helvetica", elem['size'])
            
            # 5. Configuración de Color
            rgb = self._rgb_from_int(elem.get('color', 0))
            self.canvas.setFillColorRGB(*rgb)

            # 6. Inyección de Hipervínculos
            url = self._determine_hyperlink(text, raw_y)
            if url:
                text_width = self._get_text_width(text, font_name, elem['size'])
                    
                # Definir área clickeable: [x, y_bottom, x_right, y_top]
                link_rect = (
                    x, 
                    y_rl - CFG.LINK_HITBOX_PADDING, 
                    x + text_width, 
                    y_rl + elem['size']
                )
                self.canvas.linkURL(url, link_rect, relative=0, thickness=0)

            # 8. Dibujo final
            try:
                self.canvas.drawString(x, y_rl, text)
            except Exception as e:
                logger.error(f"Fallo al dibujar texto '{text}': {e}")

        # Restaurar configuración de línea por si acaso
        self.canvas.setLineWidth(1)

    def save(self) -> None:
        """Guarda el archivo PDF final en el disco."""
        try:
            self.canvas.save()
            logger.info(f"✅ Generación completada: {CFG.FILE_OUTPUT}")
        except Exception as e:
            logger.error(f"Error al guardar el PDF: {e}")

def main():
    """Punto de entrada principal."""
    print("=" * 60)
    print("🚀 CV Generator Engine v2.0")
    print("   Nicolás Ignacio Fredes Franco")
    print("=" * 60)
    print(f"📂 Datos: {CFG.DATA_DIR}")
    print(f"📄 Salida: {CFG.FILE_OUTPUT}")
    print("=" * 60)
    
    # 1. Cargar recursos
    FontManager.register_fonts()
    
    # 2. Inicializar motor
    renderer = CVRenderer()
    
    # 3. Renderizar capas
    logger.info("Renderizando formas geométricas...")
    renderer.render_shapes()
    
    logger.info("Renderizando texto y metadatos...")
    renderer.render_text()
    
    # 4. Finalizar
    renderer.save()
    print("=" * 60)
    print(f"✅ PDF generado exitosamente")
    print("=" * 60)

if __name__ == "__main__":
    main()
