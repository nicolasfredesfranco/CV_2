#!/usr/bin/env python3
"""
ULTRA-DETAILED PDF COMPARISON TOOL
Analyzes EVERYTHING in maximum detail:
- Exact margins (top, bottom, left, right)
- Column widths, positions, ratios, gutter
- All font sizes, families, styles (bold/italic)
- All colors with hex conversion
- Text content word-by-word and line-by-line
- Vertical spacing between all elements
- Section-by-section comparison
- Alignment analysis
- Bounding box positions for every element
- Area utilization and density
- Typographic consistency
- Complete statistical analysis
"""

import fitz  # PyMuPDF
import json
from collections import defaultdict, Counter
import sys
import numpy as np
from difflib import SequenceMatcher
import re

def color_int_to_hex(color_int):
    """Convert PyMuPDF color integer to hex color"""
    if color_int == 0:
        return "#000000"
    # PyMuPDF stores colors as BGR integer
    b = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    r = color_int & 0xFF
    return f"#{r:02x}{g:02x}{b:02x}"

def analyze_font_flags(flags):
    """Decode font flags to understand styling"""
    return {
        'superscript': bool(flags & 2**0),
        'italic': bool(flags & 2**1),
        'serifed': bool(flags & 2**2),
        'monospaced': bool(flags & 2**3),
        'bold': bool(flags & 2**4),
    }

def detect_section_headers(text_blocks):
    """Detect CV section headers (EDUCATION, EXPERIENCE, etc.)"""
    sections = []
    section_keywords = [
        'EDUCATION', 'EXPERIENCE', 'SKILLS', 'LANGUAGES', 'PAPERS', 
        'WORKSHOPS', 'PROJECTS', 'CERTIFICATIONS', 'CONTACT'
    ]
    
    for idx, block in enumerate(text_blocks):
        for line in block.get('lines', []):
            for span in line.get('spans', []):
                text = span.get('text', '').strip().upper()
                for keyword in section_keywords:
                    if keyword in text:
                        sections.append({
                            'section': keyword,
                            'block_index': idx,
                            'y_position': block['y'],
                            'bbox': block['bbox'],
                            'text': span.get('text', '')
                        })
                        break
    return sections

def extract_all_text_content(pages):
    """Extract all text content in order"""
    all_text = []
    for page in pages:
        for block in page.get('text_blocks', []):
            for line in block.get('lines', []):
                line_text = ""
                for span in line.get('spans', []):
                    line_text += span.get('text', '')
                if line_text.strip():
                    all_text.append(line_text.strip())
    return all_text

def calculate_margins(page_size, text_blocks):
    """Calculate exact margins from content"""
    if not text_blocks:
        return None
    
    xs = []
    ys = []
    x_rights = []
    y_bottoms = []
    
    for block in text_blocks:
        bbox = block['bbox']
        xs.append(bbox[0])
        ys.append(bbox[1])
        x_rights.append(bbox[2])
        y_bottoms.append(bbox[3])
    
    return {
        'left': round(min(xs), 2),
        'top': round(min(ys), 2),
        'right': round(page_size['width'] - max(x_rights), 2),
        'bottom': round(page_size['height'] - max(y_bottoms), 2),
        'content_width': round(max(x_rights) - min(xs), 2),
        'content_height': round(max(y_bottoms) - min(ys), 2)
    }

def calculate_vertical_spacings(text_blocks):
    """Calculate spacing between consecutive blocks"""
    spacings = []
    sorted_blocks = sorted(text_blocks, key=lambda b: b['y'])
    
    for i in range(len(sorted_blocks) - 1):
        current_bottom = sorted_blocks[i]['bbox'][3]
        next_top = sorted_blocks[i+1]['bbox'][1]
        spacing = round(next_top - current_bottom, 2)
        if spacing > 0:  # Only positive spacings
            spacings.append({
                'spacing': spacing,
                'after_block': i,
                'before_block': i+1,
                'current_y': sorted_blocks[i]['y'],
                'next_y': sorted_blocks[i+1]['y']
            })
    
    return spacings

def analyze_alignment(text_blocks, column_info):
    """Analyze text alignment patterns"""
    left_aligned = []
    right_aligned = []
    centered = []
    
    for block in text_blocks:
        x = block['x']
        width = block['width']
        x_end = x + width
        
        # Determine which column
        split = column_info.get('split_point', 245)  # Default to 40% of letter width
        if x < split:
            col_start = column_info.get('left_start', 0)
            col_end = column_info.get('left_end', 200)
        else:
            col_start = column_info.get('right_start', 200)
            col_end = column_info.get('right_end', 600)
        
        col_width = col_end - col_start
        
        # Check alignment (with 5pt tolerance)
        if abs(x - col_start) < 5:
            left_aligned.append(block)
        elif abs(x_end - col_end) < 5:
            right_aligned.append(block)
        elif abs((x + x_end)/2 - (col_start + col_end)/2) < 5:
            centered.append(block)
    
    return {
        'left_count': len(left_aligned),
        'right_count': len(right_aligned),
        'centered_count': len(centered),
        'total_blocks': len(text_blocks)
    }

def extract_ultra_detailed_pdf_info(pdf_path):
    """Extract MAXIMUM detail from PDF"""
    doc = fitz.open(pdf_path)
    details = {
        'pages': [],
        'page_count': len(doc),
        'page_size': None,
        'margins': None,
        'column_analysis': {},
        'font_analysis': {},
        'spacing_analysis': {},
        'color_analysis': {},
        'content_analysis': {},
        'section_analysis': {},
        'alignment_analysis': {},
        'density_analysis': {},
        'ratio_analysis': {}
    }
    
    all_fonts = []
    all_colors = []
    all_font_families = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        if page_num == 0:
            details['page_size'] = {
                'width': round(page.rect.width, 2),
                'height': round(page.rect.height, 2),
                'area': round(page.rect.width * page.rect.height, 2)
            }
        
        blocks = page.get_text("dict")["blocks"]
        
        page_info = {
            'page_num': page_num + 1,
            'text_blocks': [],
            'font_sizes': [],
            'colors': [],
            'line_spacings': [],
            'x_positions': [],
            'y_positions': [],
            'column_boundaries': {'left': [], 'right': []},
            'block_spacings': []
        }
        
        for block_idx, block in enumerate(blocks):
            if block.get('type') == 0:  # text block
                bbox = block['bbox']
                block_info = {
                    'block_id': block_idx,
                    'bbox': [round(b, 2) for b in bbox],
                    'x': round(bbox[0], 2),
                    'y': round(bbox[1], 2),
                    'width': round(bbox[2] - bbox[0], 2),
                    'height': round(bbox[3] - bbox[1], 2),
                    'x_end': round(bbox[2], 2),
                    'y_end': round(bbox[3], 2),
                    'area': round((bbox[2] - bbox[0]) * (bbox[3] - bbox[1]), 2),
                    'lines': [],
                    'text_content': '',
                    'dominant_font': None,
                    'dominant_size': None,
                    'dominant_color': None
                }
                
                # Determine column with smarter detection
                # For typical 2-column CVs: left column usually < 200pts, right > 200pts
                # Use 40% of page width as threshold (more accurate than 50%)
                split_point = page.rect.width * 0.40  # ~245pts for letter size
                if bbox[0] < split_point:
                    block_info['column'] = 'left'
                    page_info['column_boundaries']['left'].append({
                        'x': round(bbox[0], 2),
                        'x_end': round(bbox[2], 2),
                        'width': round(bbox[2] - bbox[0], 2),
                        'y': round(bbox[1], 2),
                        'y_end': round(bbox[3], 2)
                    })
                else:
                    block_info['column'] = 'right'
                    page_info['column_boundaries']['right'].append({
                        'x': round(bbox[0], 2),
                        'x_end': round(bbox[2], 2),
                        'width': round(bbox[2] - bbox[0], 2),
                        'y': round(bbox[1], 2),
                        'y_end': round(bbox[3], 2)
                    })
                
                prev_y = None
                block_fonts = []
                block_sizes = []
                block_colors = []
                
                for line in block.get('lines', []):
                    line_bbox = line['bbox']
                    line_y = round(line_bbox[1], 2)
                    
                    # Calculate line spacing
                    if prev_y is not None:
                        spacing = round(line_y - prev_y, 2)
                        if spacing > 0:
                            page_info['line_spacings'].append(spacing)
                    prev_y = round(line_bbox[3], 2)
                    
                    line_info = {
                        'bbox': [round(b, 2) for b in line_bbox],
                        'y': round(line_bbox[1], 2),
                        'height': round(line_bbox[3] - line_bbox[1], 2),
                        'spans': [],
                        'text': ''
                    }
                    
                    for span in line.get('spans', []):
                        font_size = round(span.get('size', 0), 2)
                        color = span.get('color', 0)
                        font_name = span.get('font', '')
                        flags = span.get('flags', 0)
                        text = span.get('text', '')
                        
                        page_info['font_sizes'].append(font_size)
                        page_info['colors'].append(color)
                        page_info['x_positions'].append(round(span['bbox'][0], 2))
                        page_info['y_positions'].append(round(span['bbox'][1], 2))
                        
                        all_fonts.append(font_size)
                        all_colors.append(color)
                        all_font_families.append(font_name)
                        
                        block_fonts.append(font_name)
                        block_sizes.append(font_size)
                        block_colors.append(color)
                        
                        span_info = {
                            'text': text,
                            'font': font_name,
                            'size': font_size,
                            'color': color,
                            'color_hex': color_int_to_hex(color),
                            'bbox': [round(b, 2) for b in span['bbox']],
                            'flags': flags,
                            'style': analyze_font_flags(flags)
                        }
                        
                        line_info['spans'].append(span_info)
                        line_info['text'] += text
                        block_info['text_content'] += text
                    
                    block_info['lines'].append(line_info)
                
                # Determine dominant characteristics
                if block_fonts:
                    block_info['dominant_font'] = Counter(block_fonts).most_common(1)[0][0]
                if block_sizes:
                    block_info['dominant_size'] = Counter(block_sizes).most_common(1)[0][0]
                if block_colors:
                    block_info['dominant_color'] = color_int_to_hex(Counter(block_colors).most_common(1)[0][0])
                
                page_info['text_blocks'].append(block_info)
        
        details['pages'].append(page_info)
    
    doc.close()
    
    # === GLOBAL ANALYSIS ===
    if details['pages']:
        page = details['pages'][0]
        text_blocks = page['text_blocks']
        
        # Margins
        details['margins'] = calculate_margins(details['page_size'], text_blocks)
        
        # Column analysis - LEFT
        if page['column_boundaries']['left']:
            left_data = page['column_boundaries']['left']
            left_xs = [b['x'] for b in left_data]
            left_x_ends = [b['x_end'] for b in left_data]
            left_widths = [b['width'] for b in left_data]
            left_ys = [b['y'] for b in left_data]
            
            details['column_analysis']['left'] = {
                'x_min': round(min(left_xs), 2),
                'x_max': round(max(left_xs), 2),
                'x_avg': round(np.mean(left_xs), 2),
                'x_std': round(np.std(left_xs), 2),
                'x_end_min': round(min(left_x_ends), 2),
                'x_end_max': round(max(left_x_ends), 2),
                'x_end_avg': round(np.mean(left_x_ends), 2),
                'width_min': round(min(left_widths), 2),
                'width_max': round(max(left_widths), 2),
                'width_avg': round(np.mean(left_widths), 2),
                'width_std': round(np.std(left_widths), 2),
                'y_start': round(min(left_ys), 2),
                'y_end': round(max([b['y_end'] for b in left_data]), 2),
                'height': round(max([b['y_end'] for b in left_data]) - min(left_ys), 2),
                'block_count': len(left_data)
            }
        
        # Column analysis - RIGHT
        if page['column_boundaries']['right']:
            right_data = page['column_boundaries']['right']
            right_xs = [b['x'] for b in right_data]
            right_x_ends = [b['x_end'] for b in right_data]
            right_widths = [b['width'] for b in right_data]
            right_ys = [b['y'] for b in right_data]
            
            details['column_analysis']['right'] = {
                'x_min': round(min(right_xs), 2),
                'x_max': round(max(right_xs), 2),
                'x_avg': round(np.mean(right_xs), 2),
                'x_std': round(np.std(right_xs), 2),
                'x_end_min': round(min(right_x_ends), 2),
                'x_end_max': round(max(right_x_ends), 2),
                'x_end_avg': round(np.mean(right_x_ends), 2),
                'width_min': round(min(right_widths), 2),
                'width_max': round(max(right_widths), 2),
                'width_avg': round(np.mean(right_widths), 2),
                'width_std': round(np.std(right_widths), 2),
                'y_start': round(min(right_ys), 2),
                'y_end': round(max([b['y_end'] for b in right_data]), 2),
                'height': round(max([b['y_end'] for b in right_data]) - min(right_ys), 2),
                'block_count': len(right_data)
            }
        
        # Calculate gutter (space between columns)
        if 'left' in details['column_analysis'] and 'right' in details['column_analysis']:
            left_end = details['column_analysis']['left']['x_end_avg']
            right_start = details['column_analysis']['right']['x_avg']
            details['column_analysis']['gutter'] = round(right_start - left_end, 2)
        
        # Font size analysis
        all_sizes = page['font_sizes']
        if all_sizes:
            details['font_analysis']['sizes'] = {
                'all_unique': sorted(list(set([round(s, 2) for s in all_sizes]))),
                'distribution': dict(Counter([round(s, 1) for s in all_sizes])),
                'min': round(min(all_sizes), 2),
                'max': round(max(all_sizes), 2),
                'avg': round(np.mean(all_sizes), 2),
                'median': round(np.median(all_sizes), 2),
                'std': round(np.std(all_sizes), 2),
                'total_count': len(all_sizes)
            }
        
        # Font family analysis
        if all_font_families:
            family_counter = Counter(all_font_families)
            details['font_analysis']['families'] = {
                'unique_fonts': list(family_counter.keys()),
                'distribution': dict(family_counter),
                'primary_font': family_counter.most_common(1)[0][0],
                'primary_font_count': family_counter.most_common(1)[0][1],
                'font_count': len(family_counter)
            }
        
        # Color analysis
        if all_colors:
            color_counter = Counter(all_colors)
            details['color_analysis'] = {
                'unique_colors_int': list(color_counter.keys()),
                'unique_colors_hex': [color_int_to_hex(c) for c in color_counter.keys()],
                'distribution': {color_int_to_hex(k): v for k, v in color_counter.items()},
                'primary_color': color_int_to_hex(color_counter.most_common(1)[0][0]),
                'primary_color_count': color_counter.most_common(1)[0][1],
                'color_count': len(color_counter),
                'all_colors_with_usage': [
                    {'color': color_int_to_hex(k), 'count': v, 'percentage': round(v/len(all_colors)*100, 2)}
                    for k, v in color_counter.most_common()
                ]
            }
        
        # Line spacing analysis
        if page['line_spacings']:
            details['spacing_analysis']['line_spacing'] = {
                'all_unique': sorted(list(set([round(s, 2) for s in page['line_spacings']]))),
                'distribution': dict(Counter([round(s, 1) for s in page['line_spacings']])),
                'min': round(min(page['line_spacings']), 2),
                'max': round(max(page['line_spacings']), 2),
                'avg': round(np.mean(page['line_spacings']), 2),
                'median': round(np.median(page['line_spacings']), 2),
                'std': round(np.std(page['line_spacings']), 2)
            }
        
        # Block vertical spacing
        block_spacings = calculate_vertical_spacings(text_blocks)
        if block_spacings:
            spacing_values = [s['spacing'] for s in block_spacings]
            details['spacing_analysis']['block_spacing'] = {
                'all_spacings': block_spacings,
                'unique_values': sorted(list(set([round(s, 2) for s in spacing_values]))),
                'min': round(min(spacing_values), 2),
                'max': round(max(spacing_values), 2),
                'avg': round(np.mean(spacing_values), 2),
                'median': round(np.median(spacing_values), 2),
                'std': round(np.std(spacing_values), 2)
            }
        
        # Content analysis
        all_text_lines = extract_all_text_content(details['pages'])
        details['content_analysis'] = {
            'total_lines': len(all_text_lines),
            'total_characters': sum(len(line) for line in all_text_lines),
            'total_words': sum(len(line.split()) for line in all_text_lines),
            'total_blocks': len(text_blocks),
            'avg_words_per_line': round(sum(len(line.split()) for line in all_text_lines) / max(len(all_text_lines), 1), 2),
            'first_10_lines': all_text_lines[:10],
            'last_10_lines': all_text_lines[-10:] if len(all_text_lines) > 10 else []
        }
        
        # Section detection
        sections = detect_section_headers(text_blocks)
        details['section_analysis'] = {
            'sections_found': sections,
            'section_count': len(sections),
            'section_names': [s['section'] for s in sections]
        }
        
        # Alignment analysis
        column_info = {
            'split_point': details['page_size']['width'] * 0.40,  # Same as column detection
            'left_start': details['column_analysis'].get('left', {}).get('x_avg', 0),
            'left_end': details['column_analysis'].get('left', {}).get('x_end_avg', 200),
            'right_start': details['column_analysis'].get('right', {}).get('x_avg', 200),
            'right_end': details['column_analysis'].get('right', {}).get('x_end_avg', 600)
        }
        details['alignment_analysis'] = analyze_alignment(text_blocks, column_info)
        
        # Density analysis
        if details['margins'] and details['page_size']:
            content_area = details['margins']['content_width'] * details['margins']['content_height']
            page_area = details['page_size']['area']
            details['density_analysis'] = {
                'content_area': content_area,
                'page_area': page_area,
                'utilization_percentage': round(content_area / page_area * 100, 2),
                'characters_per_area': round(details['content_analysis']['total_characters'] / content_area, 4) if content_area > 0 else 0,
                'words_per_area': round(details['content_analysis']['total_words'] / content_area, 4) if content_area > 0 else 0
            }
        
        # Ratio analysis
        if details['margins'] and 'left' in details['column_analysis'] and 'right' in details['column_analysis']:
            left_w = details['column_analysis']['left']['width_avg']
            right_w = details['column_analysis']['right']['width_avg']
            total_content_w = details['margins']['content_width']
            
            details['ratio_analysis'] = {
                'left_column_ratio': round(left_w / total_content_w, 4) if total_content_w > 0 else 0,
                'right_column_ratio': round(right_w / total_content_w, 4) if total_content_w > 0 else 0,
                'column_width_ratio': round(left_w / right_w, 4) if right_w > 0 else 0,
                'margin_left_ratio': round(details['margins']['left'] / details['page_size']['width'], 4),
                'margin_right_ratio': round(details['margins']['right'] / details['page_size']['width'], 4),
                'margin_top_ratio': round(details['margins']['top'] / details['page_size']['height'], 4),
                'margin_bottom_ratio': round(details['margins']['bottom'] / details['page_size']['height'], 4)
            }
        
        # ===================================================================
        # ANÁLISIS GLOBAL DEL DOCUMENTO COMPLETO (no por columnas)
        # ===================================================================
        details['global_document_analysis'] = {}
        
        if text_blocks:
            # 1. Límites globales del documento (bounds completos)
            all_x = [b['x'] for b in text_blocks]
            all_y = [b['y'] for b in text_blocks]
            all_x_end = [b['x_end'] for b in text_blocks]
            all_y_end = [b['y_end'] for b in text_blocks]
            
            details['global_document_analysis']['global_bounds'] = {
                'leftmost': round(min(all_x), 2),
                'rightmost': round(max(all_x_end), 2),
                'topmost': round(min(all_y), 2),
                'bottommost': round(max(all_y_end), 2),
                'total_width': round(max(all_x_end) - min(all_x), 2),
                'total_height': round(max(all_y_end) - min(all_y), 2)
            }
            
            # 2. Distribución vertical completa del contenido
            y_positions_all = sorted(all_y)
            details['global_document_analysis']['vertical_distribution'] = {
                'content_starts_at': round(min(all_y), 2),
                'content_ends_at': round(max(all_y_end), 2),
                'content_span': round(max(all_y_end) - min(all_y), 2),
                'top_quartile': round(np.percentile(y_positions_all, 25), 2),
                'median': round(np.median(y_positions_all), 2),
                'bottom_quartile': round(np.percentile(y_positions_all, 75), 2)
            }
            
            # 3. Distribución horizontal completa del contenido
            x_positions_all = sorted(all_x)
            details['global_document_analysis']['horizontal_distribution'] = {
                'content_starts_at': round(min(all_x), 2),
                'content_ends_at': round(max(all_x_end), 2),
                'content_span': round(max(all_x_end) - min(all_x), 2),
                'left_quartile': round(np.percentile(x_positions_all, 25), 2),
                'median': round(np.median(x_positions_all), 2),
                'right_quartile': round(np.percentile(x_positions_all, 75), 2)
            }
            
            # 4. Espaciado global entre TODOS los elementos (no solo dentro de columnas)
            sorted_blocks_global = sorted(text_blocks, key=lambda b: (b['y'], b['x']))
            global_spacings = []
            
            for i in range(len(sorted_blocks_global) - 1):
                current = sorted_blocks_global[i]
                next_block = sorted_blocks_global[i + 1]
                
                # Espaciado vertical si están en líneas diferentes
                if abs(current['y'] - next_block['y']) > 5:  # Diferentes líneas
                    v_spacing = round(next_block['y'] - current['y_end'], 2)
                    if v_spacing > 0:
                        global_spacings.append({
                            'type': 'vertical',
                            'spacing': v_spacing,
                            'from_block': i,
                            'to_block': i + 1
                        })
            
            if global_spacings:
                v_spacings = [s['spacing'] for s in global_spacings if s['type'] == 'vertical']
                if v_spacings:
                    details['global_document_analysis']['global_vertical_spacing'] = {
                        'min': round(min(v_spacings), 2),
                        'max': round(max(v_spacings), 2),
                        'avg': round(np.mean(v_spacings), 2),
                        'median': round(np.median(v_spacings), 2),
                        'std': round(np.std(v_spacings), 2),
                        'total_gaps': len(v_spacings)
                    }
            
            # 5. Balance global del documento (simetría y distribución)
            page_center_x = details['page_size']['width'] / 2
            page_center_y = details['page_size']['height'] / 2
            
            # Calcular centro de masa del contenido
            total_area = sum(b['area'] for b in text_blocks)
            weighted_x = sum(b['x'] * b['area'] for b in text_blocks) / total_area if total_area > 0 else 0
            weighted_y = sum(b['y'] * b['area'] for b in text_blocks) / total_area if total_area > 0 else 0
            
            details['global_document_analysis']['balance'] = {
                'content_center_x': round(weighted_x, 2),
                'content_center_y': round(weighted_y, 2),
                'page_center_x': round(page_center_x, 2),
                'page_center_y': round(page_center_y, 2),
                'horizontal_offset': round(weighted_x - page_center_x, 2),
                'vertical_offset': round(weighted_y - page_center_y, 2),
                'is_balanced_horizontally': abs(weighted_x - page_center_x) < 20,
                'is_balanced_vertically': abs(weighted_y - page_center_y) < 20
            }
            
            # 6. Consistencia de espaciado a nivel documento
            if page['line_spacings']:
                details['global_document_analysis']['spacing_consistency'] = {
                    'line_spacing_variance': round(np.var(page['line_spacings']), 2),
                    'line_spacing_cv': round(np.std(page['line_spacings']) / np.mean(page['line_spacings']) * 100, 2) if np.mean(page['line_spacings']) > 0 else 0
                }
            
            # 7. Análisis de whitespace (espacio negativo/en blanco)
            total_text_area = sum(b['area'] for b in text_blocks)
            content_area = details['margins']['content_width'] * details['margins']['content_height'] if details['margins'] else 0
            
            details['global_document_analysis']['whitespace'] = {
                'total_text_area': round(total_text_area, 2),
                'total_content_area': round(content_area, 2),
                'whitespace_area': round(content_area - total_text_area, 2) if content_area > 0 else 0,
                'whitespace_percentage': round((content_area - total_text_area) / content_area * 100, 2) if content_area > 0 else 0,
                'text_to_whitespace_ratio': round(total_text_area / (content_area - total_text_area), 4) if (content_area - total_text_area) > 0 else 0
            }
            
            # 8. Análisis de leading (relación entre line spacing y font size)
            if all_fonts and page['line_spacings']:
                avg_font_size = np.mean(all_fonts)
                avg_line_spacing = np.mean(page['line_spacings'])
                details['global_document_analysis']['leading_analysis'] = {
                    'avg_font_size': round(avg_font_size, 2),
                    'avg_line_spacing': round(avg_line_spacing, 2),
                    'leading_ratio': round(avg_line_spacing / avg_font_size, 4) if avg_font_size > 0 else 0,
                    'typical_leading': round(avg_font_size * 1.2, 2),  # 120% is standard
                    'leading_deviation': round(avg_line_spacing - (avg_font_size * 1.2), 2)
                }
            
            # 9. Peso visual por sección (análisis de cada sección del CV)
            sections_detected = detect_section_headers(text_blocks)
            section_weights = []
            
            for section in sections_detected:
                section_name = section['section']
                section_y = section['y_position']
                
                # Encontrar todos los bloques que pertenecen a esta sección
                section_blocks = []
                for block in text_blocks:
                    # Bloques después de este header y antes del siguiente
                    if block['y'] >= section_y:
                        section_blocks.append(block)
                
                if section_blocks:
                    section_area = sum(b['area'] for b in section_blocks)
                    section_height = max(b['y_end'] for b in section_blocks) - min(b['y'] for b in section_blocks)
                    
                    section_weights.append({
                        'section': section_name,
                        'area': round(section_area, 2),
                        'height': round(section_height, 2),
                        'block_count': len(section_blocks),
                        'y_start': round(section_y, 2)
                    })
            
            details['global_document_analysis']['section_weights'] = section_weights
            
            # 10. Análisis de jerarquía visual completa
            font_sizes_sorted = sorted(list(set(all_fonts)), reverse=True)
            visual_hierarchy = []
            
            for i, size in enumerate(font_sizes_sorted):
                count = all_fonts.count(size)
                percentage = round(count / len(all_fonts) * 100, 2)
                hierarchy_level = i + 1
                
                visual_hierarchy.append({
                    'level': hierarchy_level,
                    'font_size': round(size, 2),
                    'usage_count': count,
                    'usage_percentage': percentage,
                    'role': 'primary' if hierarchy_level == 1 else 'secondary' if hierarchy_level == 2 else 'tertiary' if hierarchy_level == 3 else 'detail'
                })
            
            details['global_document_analysis']['visual_hierarchy'] = visual_hierarchy
    
    return details

def ultra_detailed_comparison(orig, gen):
    """MAXIMUM detail comparison with specific recommendations"""
    report = {
        'page_size': {},
        'margins': {},
        'columns': {},
        'gutter': {},
        'fonts': {},
        'colors': {},
        'spacing': {},
        'content': {},
        'sections': {},
        'alignment': {},
        'density': {},
        'ratios': {},
        'global_document': {},  # NUEVO: análisis global del documento completo
        'block_by_block': {},
        'recommendations': [],
        'critical_issues': [],
        'minor_issues': []
    }
    
    # === PAGE SIZE ===
    if orig['page_size'] != gen['page_size']:
        report['page_size'] = {
            'match': False,
            'original': orig['page_size'],
            'generated': gen['page_size'],
            'diff_width': abs(orig['page_size']['width'] - gen['page_size']['width']),
            'diff_height': abs(orig['page_size']['height'] - gen['page_size']['height']),
            'diff_area': abs(orig['page_size']['area'] - gen['page_size']['area'])
        }
        report['critical_issues'].append(
            f"❌ Page size mismatch: {gen['page_size']['width']}x{gen['page_size']['height']} should be {orig['page_size']['width']}x{orig['page_size']['height']}"
        )
    else:
        report['page_size'] = {'match': True, 'value': orig['page_size']}
    
    # === MARGINS ===
    if orig['margins'] and gen['margins']:
        om = orig['margins']
        gm = gen['margins']
        report['margins'] = {
            'left': {
                'original': om['left'],
                'generated': gm['left'],
                'diff': round(abs(om['left'] - gm['left']), 2),
                'diff_percent': round(abs(om['left'] - gm['left']) / om['left'] * 100, 2) if om['left'] > 0 else 0
            },
            'top': {
                'original': om['top'],
                'generated': gm['top'],
                'diff': round(abs(om['top'] - gm['top']), 2),
                'diff_percent': round(abs(om['top'] - gm['top']) / om['top'] * 100, 2) if om['top'] > 0 else 0
            },
            'right': {
                'original': om['right'],
                'generated': gm['right'],
                'diff': round(abs(om['right'] - gm['right']), 2),
                'diff_percent': round(abs(om['right'] - gm['right']) / om['right'] * 100, 2) if om['right'] > 0 else 0
            },
            'bottom': {
                'original': om['bottom'],
                'generated': gm['bottom'],
                'diff': round(abs(om['bottom'] - gm['bottom']), 2),
                'diff_percent': round(abs(om['bottom'] - gm['bottom']) / om['bottom'] * 100, 2) if om['bottom'] > 0 else 0
            },
            'content_width': {
                'original': om['content_width'],
                'generated': gm['content_width'],
                'diff': round(abs(om['content_width'] - gm['content_width']), 2)
            },
            'content_height': {
                'original': om['content_height'],
                'generated': gm['content_height'],
                'diff': round(abs(om['content_height'] - gm['content_height']), 2)
            }
        }
        
        # Margin recommendations
        for margin in ['left', 'top', 'right', 'bottom']:
            if report['margins'][margin]['diff'] > 2:
            report['recommendations'].append(
                    f"⚠️ Margin {margin}: {gm[margin]:.2f}pt should be {om[margin]:.2f}pt "
                    f"(diff: {report['margins'][margin]['diff']:.2f}pt, {report['margins'][margin]['diff_percent']:.1f}%)"
                )
    
    # === COLUMNS ===
    for col in ['left', 'right']:
        if col in orig['column_analysis'] and col in gen['column_analysis']:
            oc = orig['column_analysis'][col]
            gc = gen['column_analysis'][col]
            
            report['columns'][col] = {
            'x_position': {
                    'original': oc['x_avg'],
                    'generated': gc['x_avg'],
                    'diff': round(abs(oc['x_avg'] - gc['x_avg']), 2),
                    'std_original': oc['x_std'],
                    'std_generated': gc['x_std']
                },
                'x_end_position': {
                    'original': oc['x_end_avg'],
                    'generated': gc['x_end_avg'],
                    'diff': round(abs(oc['x_end_avg'] - gc['x_end_avg']), 2)
            },
            'width': {
                    'original': oc['width_avg'],
                    'generated': gc['width_avg'],
                    'diff': round(abs(oc['width_avg'] - gc['width_avg']), 2),
                    'diff_percent': round(abs(oc['width_avg'] - gc['width_avg']) / oc['width_avg'] * 100, 2),
                    'std_original': oc['width_std'],
                    'std_generated': gc['width_std']
                },
                'height': {
                    'original': oc['height'],
                    'generated': gc['height'],
                    'diff': round(abs(oc['height'] - gc['height']), 2)
                },
                'y_start': {
                    'original': oc['y_start'],
                    'generated': gc['y_start'],
                    'diff': round(abs(oc['y_start'] - gc['y_start']), 2)
                },
                'y_end': {
                    'original': oc['y_end'],
                    'generated': gc['y_end'],
                    'diff': round(abs(oc['y_end'] - gc['y_end']), 2)
                },
                'block_count': {
                    'original': oc['block_count'],
                    'generated': gc['block_count'],
                    'diff': abs(oc['block_count'] - gc['block_count'])
                }
            }
            
            # Column width recommendations
            if report['columns'][col]['width']['diff'] > 2:
            report['recommendations'].append(
                    f"⚠️ {col.capitalize()} column width: {gc['width_avg']:.2f}pt should be {oc['width_avg']:.2f}pt "
                    f"(diff: {report['columns'][col]['width']['diff']:.2f}pt, {report['columns'][col]['width']['diff_percent']:.1f}%)"
                )
            
            # Column position recommendations
            if report['columns'][col]['x_position']['diff'] > 3:
                report['minor_issues'].append(
                    f"➖ {col.capitalize()} column X position: {gc['x_avg']:.2f}pt vs {oc['x_avg']:.2f}pt "
                    f"(diff: {report['columns'][col]['x_position']['diff']:.2f}pt)"
                )
    
    # === GUTTER ===
    if 'gutter' in orig['column_analysis'] and 'gutter' in gen['column_analysis']:
        og = orig['column_analysis']['gutter']
        gg = gen['column_analysis']['gutter']
        report['gutter'] = {
            'original': og,
            'generated': gg,
            'diff': round(abs(og - gg), 2),
            'diff_percent': round(abs(og - gg) / og * 100, 2) if og > 0 else 0
        }
        
        if report['gutter']['diff'] > 3:
            report['recommendations'].append(
                f"⚠️ Gutter (space between columns): {gg:.2f}pt should be {og:.2f}pt "
                f"(diff: {report['gutter']['diff']:.2f}pt)"
            )
    
    # === FONTS ===
    orig_font = orig['font_analysis']
    gen_font = gen['font_analysis']
    
    # Font sizes
    report['fonts']['sizes'] = {
        'original': orig_font['sizes']['all_unique'],
        'generated': gen_font['sizes']['all_unique'],
        'missing': [s for s in orig_font['sizes']['all_unique'] if s not in gen_font['sizes']['all_unique']],
        'extra': [s for s in gen_font['sizes']['all_unique'] if s not in orig_font['sizes']['all_unique']],
        'statistics': {
            'min': {
                'original': orig_font['sizes']['min'],
                'generated': gen_font['sizes']['min'],
                'diff': round(abs(orig_font['sizes']['min'] - gen_font['sizes']['min']), 2)
            },
            'max': {
                'original': orig_font['sizes']['max'],
                'generated': gen_font['sizes']['max'],
                'diff': round(abs(orig_font['sizes']['max'] - gen_font['sizes']['max']), 2)
            },
            'avg': {
                'original': orig_font['sizes']['avg'],
                'generated': gen_font['sizes']['avg'],
                'diff': round(abs(orig_font['sizes']['avg'] - gen_font['sizes']['avg']), 2)
            },
            'median': {
                'original': orig_font['sizes']['median'],
                'generated': gen_font['sizes']['median'],
                'diff': round(abs(orig_font['sizes']['median'] - gen_font['sizes']['median']), 2)
            },
            'std': {
                'original': orig_font['sizes']['std'],
                'generated': gen_font['sizes']['std'],
                'diff': round(abs(orig_font['sizes']['std'] - gen_font['sizes']['std']), 2)
            }
        }
    }
    
    # Font size recommendations
    if report['fonts']['sizes']['statistics']['max']['diff'] > 0.5:
        report['recommendations'].append(
            f"⚠️ Max font size: {gen_font['sizes']['max']:.2f}pt should be {orig_font['sizes']['max']:.2f}pt"
        )
    
    if report['fonts']['sizes']['statistics']['avg']['diff'] > 0.5:
        report['recommendations'].append(
            f"⚠️ Avg font size: {gen_font['sizes']['avg']:.2f}pt should be {orig_font['sizes']['avg']:.2f}pt"
        )
    
    if report['fonts']['sizes']['missing']:
        report['critical_issues'].append(
            f"❌ Missing font sizes: {report['fonts']['sizes']['missing']}"
        )
    
    if report['fonts']['sizes']['extra']:
        report['minor_issues'].append(
            f"➕ Extra font sizes: {report['fonts']['sizes']['extra']}"
        )
    
    # Font size distribution
    orig_dist = orig_font['sizes']['distribution']
    gen_dist = gen_font['sizes']['distribution']
    
    report['fonts']['distribution_diff'] = {}
    for size in set(list(orig_dist.keys()) + list(gen_dist.keys())):
        orig_count = orig_dist.get(size, 0)
        gen_count = gen_dist.get(size, 0)
        if orig_count != gen_count:
            report['fonts']['distribution_diff'][size] = {
                'original': orig_count,
                'generated': gen_count,
                'diff': gen_count - orig_count,
                'diff_percent': round((gen_count - orig_count) / orig_count * 100, 2) if orig_count > 0 else 100
            }
    
    # Font families
    if 'families' in orig_font and 'families' in gen_font:
        report['fonts']['families'] = {
            'original': orig_font['families']['unique_fonts'],
            'generated': gen_font['families']['unique_fonts'],
            'primary_original': orig_font['families']['primary_font'],
            'primary_generated': gen_font['families']['primary_font'],
            'match': orig_font['families']['primary_font'] == gen_font['families']['primary_font']
        }
        
        if not report['fonts']['families']['match']:
            report['critical_issues'].append(
                f"❌ Font family mismatch: using '{gen_font['families']['primary_font']}' "
                f"should use '{orig_font['families']['primary_font']}'"
            )
    
    # === COLORS ===
    orig_colors = orig['color_analysis']
    gen_colors = gen['color_analysis']
    
    report['colors'] = {
        'original_colors': orig_colors['unique_colors_hex'],
        'generated_colors': gen_colors['unique_colors_hex'],
        'original_count': orig_colors['color_count'],
        'generated_count': gen_colors['color_count'],
        'missing_colors': [c for c in orig_colors['unique_colors_hex'] if c not in gen_colors['unique_colors_hex']],
        'extra_colors': [c for c in gen_colors['unique_colors_hex'] if c not in orig_colors['unique_colors_hex']],
        'primary_original': orig_colors['primary_color'],
        'primary_generated': gen_colors['primary_color'],
        'distribution_comparison': {}
    }
    
    # Color distribution comparison
    for color in set(orig_colors['unique_colors_hex'] + gen_colors['unique_colors_hex']):
        orig_count = orig_colors['distribution'].get(color, 0)
        gen_count = gen_colors['distribution'].get(color, 0)
        if orig_count != gen_count:
            report['colors']['distribution_comparison'][color] = {
                'original': orig_count,
                'generated': gen_count,
                'diff': gen_count - orig_count
            }
    
    if report['colors']['missing_colors']:
        report['critical_issues'].append(
            f"❌ Missing colors: {report['colors']['missing_colors']}"
        )
    
    if report['colors']['extra_colors']:
        report['minor_issues'].append(
            f"➕ Extra colors: {report['colors']['extra_colors']}"
        )
    
    # === SPACING ===
    
    # Line spacing
    if 'line_spacing' in orig['spacing_analysis'] and 'line_spacing' in gen['spacing_analysis']:
        ols = orig['spacing_analysis']['line_spacing']
        gls = gen['spacing_analysis']['line_spacing']
        
        report['spacing']['line_spacing'] = {
            'statistics': {
                'min': {'original': ols['min'], 'generated': gls['min'], 'diff': round(abs(ols['min'] - gls['min']), 2)},
                'max': {'original': ols['max'], 'generated': gls['max'], 'diff': round(abs(ols['max'] - gls['max']), 2)},
                'avg': {'original': ols['avg'], 'generated': gls['avg'], 'diff': round(abs(ols['avg'] - gls['avg']), 2)},
                'median': {'original': ols['median'], 'generated': gls['median'], 'diff': round(abs(ols['median'] - gls['median']), 2)},
                'std': {'original': ols['std'], 'generated': gls['std'], 'diff': round(abs(ols['std'] - gls['std']), 2)}
            },
            'unique_values_original': ols['all_unique'],
            'unique_values_generated': gls['all_unique']
        }
        
        if report['spacing']['line_spacing']['statistics']['avg']['diff'] > 1.0:
            report['recommendations'].append(
                f"⚠️ Avg line spacing: {gls['avg']:.2f}pt should be {ols['avg']:.2f}pt"
            )
    
    # Block spacing
    if 'block_spacing' in orig['spacing_analysis'] and 'block_spacing' in gen['spacing_analysis']:
        obs = orig['spacing_analysis']['block_spacing']
        gbs = gen['spacing_analysis']['block_spacing']
        
        report['spacing']['block_spacing'] = {
            'statistics': {
                'min': {'original': obs['min'], 'generated': gbs['min'], 'diff': round(abs(obs['min'] - gbs['min']), 2)},
                'max': {'original': obs['max'], 'generated': gbs['max'], 'diff': round(abs(obs['max'] - gbs['max']), 2)},
                'avg': {'original': obs['avg'], 'generated': gbs['avg'], 'diff': round(abs(obs['avg'] - gbs['avg']), 2)},
                'median': {'original': obs['median'], 'generated': gbs['median'], 'diff': round(abs(obs['median'] - gbs['median']), 2)},
                'std': {'original': obs['std'], 'generated': gbs['std'], 'diff': round(abs(obs['std'] - gbs['std']), 2)}
            }
        }
        
        if report['spacing']['block_spacing']['statistics']['avg']['diff'] > 2.0:
            report['recommendations'].append(
                f"⚠️ Avg block spacing: {gbs['avg']:.2f}pt should be {obs['avg']:.2f}pt"
            )
    
    # === CONTENT ===
    orig_content = orig['content_analysis']
    gen_content = gen['content_analysis']
    
    report['content'] = {
        'total_lines': {
            'original': orig_content['total_lines'],
            'generated': gen_content['total_lines'],
            'diff': abs(orig_content['total_lines'] - gen_content['total_lines'])
        },
        'total_characters': {
            'original': orig_content['total_characters'],
            'generated': gen_content['total_characters'],
            'diff': abs(orig_content['total_characters'] - gen_content['total_characters'])
        },
        'total_words': {
            'original': orig_content['total_words'],
            'generated': gen_content['total_words'],
            'diff': abs(orig_content['total_words'] - gen_content['total_words'])
        },
        'total_blocks': {
            'original': orig_content['total_blocks'],
            'generated': gen_content['total_blocks'],
            'diff': abs(orig_content['total_blocks'] - gen_content['total_blocks'])
        }
    }
    
    # Text similarity
    orig_text = ' '.join(orig_content['first_10_lines'])
    gen_text = ' '.join(gen_content['first_10_lines'])
    text_similarity = SequenceMatcher(None, orig_text, gen_text).ratio()
    report['content']['text_similarity'] = round(text_similarity * 100, 2)
    
    if report['content']['text_similarity'] < 95:
        report['minor_issues'].append(
            f"➖ Text content similarity: {report['content']['text_similarity']:.1f}% (should be close to 100%)"
        )
    
    # === SECTIONS ===
    orig_sections = orig['section_analysis']
    gen_sections = gen['section_analysis']
    
    report['sections'] = {
        'original_sections': orig_sections['section_names'],
        'generated_sections': gen_sections['section_names'],
        'original_count': orig_sections['section_count'],
        'generated_count': gen_sections['section_count'],
        'missing_sections': [s for s in orig_sections['section_names'] if s not in gen_sections['section_names']],
        'extra_sections': [s for s in gen_sections['section_names'] if s not in orig_sections['section_names']],
        'match': orig_sections['section_names'] == gen_sections['section_names']
    }
    
    if report['sections']['missing_sections']:
        report['critical_issues'].append(
            f"❌ Missing sections: {report['sections']['missing_sections']}"
        )
    
    # === ALIGNMENT ===
    orig_align = orig['alignment_analysis']
    gen_align = gen['alignment_analysis']
    
    report['alignment'] = {
        'left_aligned': {
            'original': orig_align['left_count'],
            'generated': gen_align['left_count'],
            'diff': abs(orig_align['left_count'] - gen_align['left_count'])
        },
        'right_aligned': {
            'original': orig_align['right_count'],
            'generated': gen_align['right_count'],
            'diff': abs(orig_align['right_count'] - gen_align['right_count'])
        },
        'centered': {
            'original': orig_align['centered_count'],
            'generated': gen_align['centered_count'],
            'diff': abs(orig_align['centered_count'] - gen_align['centered_count'])
        }
    }
    
    # === DENSITY ===
    orig_density = orig['density_analysis']
    gen_density = gen['density_analysis']
    
    report['density'] = {
        'utilization_percentage': {
            'original': orig_density['utilization_percentage'],
            'generated': gen_density['utilization_percentage'],
            'diff': round(abs(orig_density['utilization_percentage'] - gen_density['utilization_percentage']), 2)
        },
        'words_per_area': {
            'original': orig_density['words_per_area'],
            'generated': gen_density['words_per_area'],
            'diff': round(abs(orig_density['words_per_area'] - gen_density['words_per_area']), 4)
        }
    }
    
    if report['density']['utilization_percentage']['diff'] > 3:
        report['recommendations'].append(
            f"⚠️ Page utilization: {gen_density['utilization_percentage']:.1f}% should be {orig_density['utilization_percentage']:.1f}%"
        )
    
    # === RATIOS ===
    if orig.get('ratio_analysis') and gen.get('ratio_analysis'):
        orig_ratios = orig['ratio_analysis']
        gen_ratios = gen['ratio_analysis']
        
        report['ratios'] = {
            'left_column_ratio': {
                'original': orig_ratios['left_column_ratio'],
                'generated': gen_ratios['left_column_ratio'],
                'diff': round(abs(orig_ratios['left_column_ratio'] - gen_ratios['left_column_ratio']), 4)
            },
            'right_column_ratio': {
                'original': orig_ratios['right_column_ratio'],
                'generated': gen_ratios['right_column_ratio'],
                'diff': round(abs(orig_ratios['right_column_ratio'] - gen_ratios['right_column_ratio']), 4)
            },
            'column_width_ratio': {
                'original': orig_ratios['column_width_ratio'],
                'generated': gen_ratios['column_width_ratio'],
                'diff': round(abs(orig_ratios['column_width_ratio'] - gen_ratios['column_width_ratio']), 4),
                'diff_percent': round(abs(orig_ratios['column_width_ratio'] - gen_ratios['column_width_ratio']) / orig_ratios['column_width_ratio'] * 100, 2) if orig_ratios['column_width_ratio'] > 0 else 0
            }
        }
        
        if report['ratios']['column_width_ratio']['diff_percent'] > 5:
            report['recommendations'].append(
                f"⚠️ Column width ratio: {gen_ratios['column_width_ratio']:.4f} should be {orig_ratios['column_width_ratio']:.4f} "
                f"(left:right proportion)"
            )
    
    # =========================================================================
    # === ANÁLISIS GLOBAL DEL DOCUMENTO COMPLETO ===
    # =========================================================================
    if orig.get('global_document_analysis') and gen.get('global_document_analysis'):
        orig_global = orig['global_document_analysis']
        gen_global = gen['global_document_analysis']
        
        # 1. Límites globales del documento
        if 'global_bounds' in orig_global and 'global_bounds' in gen_global:
            ob = orig_global['global_bounds']
            gb = gen_global['global_bounds']
            
            report['global_document']['bounds'] = {
                'leftmost': {
                    'original': ob['leftmost'],
                    'generated': gb['leftmost'],
                    'diff': round(abs(ob['leftmost'] - gb['leftmost']), 2)
                },
                'rightmost': {
                    'original': ob['rightmost'],
                    'generated': gb['rightmost'],
                    'diff': round(abs(ob['rightmost'] - gb['rightmost']), 2)
                },
                'topmost': {
                    'original': ob['topmost'],
                    'generated': gb['topmost'],
                    'diff': round(abs(ob['topmost'] - gb['topmost']), 2)
                },
                'bottommost': {
                    'original': ob['bottommost'],
                    'generated': gb['bottommost'],
                    'diff': round(abs(ob['bottommost'] - gb['bottommost']), 2)
                },
                'total_width': {
                    'original': ob['total_width'],
                    'generated': gb['total_width'],
                    'diff': round(abs(ob['total_width'] - gb['total_width']), 2),
                    'diff_percent': round(abs(ob['total_width'] - gb['total_width']) / ob['total_width'] * 100, 2) if ob['total_width'] > 0 else 0
                },
                'total_height': {
                    'original': ob['total_height'],
                    'generated': gb['total_height'],
                    'diff': round(abs(ob['total_height'] - gb['total_height']), 2),
                    'diff_percent': round(abs(ob['total_height'] - gb['total_height']) / ob['total_height'] * 100, 2) if ob['total_height'] > 0 else 0
                }
            }
            
            # Advertencias para límites globales
            if report['global_document']['bounds']['topmost']['diff'] > 3:
                report['minor_issues'].append(
                    f"➖ Document top boundary: {gb['topmost']:.2f}pt vs {ob['topmost']:.2f}pt"
                )
            if report['global_document']['bounds']['bottommost']['diff'] > 3:
                report['minor_issues'].append(
                    f"➖ Document bottom boundary: {gb['bottommost']:.2f}pt vs {ob['bottommost']:.2f}pt"
                )
        
        # 2. Distribución vertical global
        if 'vertical_distribution' in orig_global and 'vertical_distribution' in gen_global:
            ov = orig_global['vertical_distribution']
            gv = gen_global['vertical_distribution']
            
            report['global_document']['vertical_distribution'] = {
                'content_span': {
                    'original': ov['content_span'],
                    'generated': gv['content_span'],
                    'diff': round(abs(ov['content_span'] - gv['content_span']), 2)
                },
                'top_quartile': {
                    'original': ov['top_quartile'],
                    'generated': gv['top_quartile'],
                    'diff': round(abs(ov['top_quartile'] - gv['top_quartile']), 2)
                },
                'median': {
                    'original': ov['median'],
                    'generated': gv['median'],
                    'diff': round(abs(ov['median'] - gv['median']), 2)
                },
                'bottom_quartile': {
                    'original': ov['bottom_quartile'],
                    'generated': gv['bottom_quartile'],
                    'diff': round(abs(ov['bottom_quartile'] - gv['bottom_quartile']), 2)
                }
            }
        
        # 3. Distribución horizontal global
        if 'horizontal_distribution' in orig_global and 'horizontal_distribution' in gen_global:
            oh = orig_global['horizontal_distribution']
            gh = gen_global['horizontal_distribution']
            
            report['global_document']['horizontal_distribution'] = {
                'content_span': {
                    'original': oh['content_span'],
                    'generated': gh['content_span'],
                    'diff': round(abs(oh['content_span'] - gh['content_span']), 2)
                },
                'median': {
                    'original': oh['median'],
                    'generated': gh['median'],
                    'diff': round(abs(oh['median'] - gh['median']), 2)
                }
            }
        
        # 4. Espaciado vertical global
        if 'global_vertical_spacing' in orig_global and 'global_vertical_spacing' in gen_global:
            ovs = orig_global['global_vertical_spacing']
            gvs = gen_global['global_vertical_spacing']
            
            report['global_document']['global_vertical_spacing'] = {
                'avg': {
                    'original': ovs['avg'],
                    'generated': gvs['avg'],
                    'diff': round(abs(ovs['avg'] - gvs['avg']), 2)
                },
                'median': {
                    'original': ovs['median'],
                    'generated': gvs['median'],
                    'diff': round(abs(ovs['median'] - gvs['median']), 2)
                },
                'std': {
                    'original': ovs['std'],
                    'generated': gvs['std'],
                    'diff': round(abs(ovs['std'] - gvs['std']), 2)
                },
                'total_gaps': {
                    'original': ovs['total_gaps'],
                    'generated': gvs['total_gaps'],
                    'diff': abs(ovs['total_gaps'] - gvs['total_gaps'])
                }
            }
            
            if report['global_document']['global_vertical_spacing']['avg']['diff'] > 2:
                report['recommendations'].append(
                    f"⚠️ Global vertical spacing: {gvs['avg']:.2f}pt should be {ovs['avg']:.2f}pt"
                )
        
        # 5. Balance del documento
        if 'balance' in orig_global and 'balance' in gen_global:
            obal = orig_global['balance']
            gbal = gen_global['balance']
            
            report['global_document']['balance'] = {
                'horizontal_offset': {
                    'original': obal['horizontal_offset'],
                    'generated': gbal['horizontal_offset'],
                    'diff': round(abs(obal['horizontal_offset'] - gbal['horizontal_offset']), 2)
                },
                'vertical_offset': {
                    'original': obal['vertical_offset'],
                    'generated': gbal['vertical_offset'],
                    'diff': round(abs(obal['vertical_offset'] - gbal['vertical_offset']), 2)
                }
            }
            
            # Advertencia si el balance cambió significativamente
            if report['global_document']['balance']['horizontal_offset']['diff'] > 15:
                report['minor_issues'].append(
                    f"➖ Document horizontal balance shifted by {report['global_document']['balance']['horizontal_offset']['diff']:.2f}pt"
                )
        
        # 6. Consistencia de espaciado
        if 'spacing_consistency' in orig_global and 'spacing_consistency' in gen_global:
            osc = orig_global['spacing_consistency']
            gsc = gen_global['spacing_consistency']
            
            report['global_document']['spacing_consistency'] = {
                'line_spacing_variance': {
                    'original': osc['line_spacing_variance'],
                    'generated': gsc['line_spacing_variance'],
                    'diff': round(abs(osc['line_spacing_variance'] - gsc['line_spacing_variance']), 2)
                },
                'cv': {
                    'original': osc['line_spacing_cv'],
                    'generated': gsc['line_spacing_cv'],
                    'diff': round(abs(osc['line_spacing_cv'] - gsc['line_spacing_cv']), 2)
                }
            }
        
        # 7. Whitespace (espacio negativo) comparison
        if 'whitespace' in orig_global and 'whitespace' in gen_global:
            ow = orig_global['whitespace']
            gw = gen_global['whitespace']
            
            report['global_document']['whitespace'] = {
                'percentage': {
                    'original': ow['whitespace_percentage'],
                    'generated': gw['whitespace_percentage'],
                    'diff': round(abs(ow['whitespace_percentage'] - gw['whitespace_percentage']), 2)
                },
                'ratio': {
                    'original': ow['text_to_whitespace_ratio'],
                    'generated': gw['text_to_whitespace_ratio'],
                    'diff': round(abs(ow['text_to_whitespace_ratio'] - gw['text_to_whitespace_ratio']), 4)
                }
            }
            
            if report['global_document']['whitespace']['percentage']['diff'] > 5:
                report['minor_issues'].append(
                    f"➖ Whitespace: {gw['whitespace_percentage']:.1f}% vs {ow['whitespace_percentage']:.1f}%"
                )
        
        # 8. Leading analysis comparison
        if 'leading_analysis' in orig_global and 'leading_analysis' in gen_global:
            ol = orig_global['leading_analysis']
            gl = gen_global['leading_analysis']
            
            report['global_document']['leading'] = {
                'ratio': {
                    'original': ol['leading_ratio'],
                    'generated': gl['leading_ratio'],
                    'diff': round(abs(ol['leading_ratio'] - gl['leading_ratio']), 4)
                },
                'deviation': {
                    'original': ol['leading_deviation'],
                    'generated': gl['leading_deviation'],
                    'diff': round(abs(ol['leading_deviation'] - gl['leading_deviation']), 2)
                }
            }
        
        # 9. Section weights comparison (peso visual de cada sección)
        if 'section_weights' in orig_global and 'section_weights' in gen_global:
            orig_sections = {s['section']: s for s in orig_global['section_weights']}
            gen_sections = {s['section']: s for s in gen_global['section_weights']}
            
            section_comparison = {}
            for section_name in set(list(orig_sections.keys()) + list(gen_sections.keys())):
                if section_name in orig_sections and section_name in gen_sections:
                    os = orig_sections[section_name]
                    gs = gen_sections[section_name]
                    
                    section_comparison[section_name] = {
                        'area': {
                            'original': os['area'],
                            'generated': gs['area'],
                            'diff': round(abs(os['area'] - gs['area']), 2),
                            'diff_percent': round(abs(os['area'] - gs['area']) / os['area'] * 100, 2) if os['area'] > 0 else 0
                        },
                        'height': {
                            'original': os['height'],
                            'generated': gs['height'],
                            'diff': round(abs(os['height'] - gs['height']), 2)
                        }
                    }
            
            report['global_document']['section_weights'] = section_comparison
        
        # 10. Visual hierarchy comparison
        if 'visual_hierarchy' in orig_global and 'visual_hierarchy' in gen_global:
            orig_hierarchy = orig_global['visual_hierarchy']
            gen_hierarchy = gen_global['visual_hierarchy']
            
            hierarchy_match = len(orig_hierarchy) == len(gen_hierarchy)
            hierarchy_differences = []
            
            for i in range(min(len(orig_hierarchy), len(gen_hierarchy))):
                oh = orig_hierarchy[i]
                gh = gen_hierarchy[i]
                
                if oh['font_size'] != gh['font_size'] or abs(oh['usage_percentage'] - gh['usage_percentage']) > 5:
                    hierarchy_differences.append({
                        'level': i + 1,
                        'original_size': oh['font_size'],
                        'generated_size': gh['font_size'],
                        'original_usage': oh['usage_percentage'],
                        'generated_usage': gh['usage_percentage']
                    })
            
            report['global_document']['visual_hierarchy'] = {
                'levels_match': hierarchy_match,
                'differences': hierarchy_differences,
                'total_levels_original': len(orig_hierarchy),
                'total_levels_generated': len(gen_hierarchy)
            }
            
            if hierarchy_differences:
                report['minor_issues'].append(
                    f"➖ Visual hierarchy differs in {len(hierarchy_differences)} levels"
            )
    
    return report

def calculate_ultra_detailed_similarity(report, orig, gen):
    """
    MÉTRICA UNIFICADA ULTRA-DETALLADA: Combina TODAS las dimensiones posibles
    para generar un score único de 0 a 100 que mide la similitud total entre PDFs.
    
    Esta métrica analiza y pondera:
    - Geometría (página, márgenes, columnas)
    - Tipografía (tamaños, familias, distribución)
    - Colores (paleta, distribución)
    - Espaciado (líneas, bloques, consistencia)
    - Contenido (texto, bloques, palabras)
    - Estructura (secciones, alineación)
    - Densidad (uso de espacio)
    - Proporciones (ratios)
    - Posiciones exactas
    - Y todos los micro-detalles detectables
    
    Score: 100 = idénticos, 0 = totalmente diferentes
    """
    score = 100.0
    penalties = []
    detailed_breakdown = {}
    
    # ============================================================================
    # 1. GEOMETRÍA DE PÁGINA (peso: 3% del total)
    # ============================================================================
    geometry_penalty = 0
    
    # 1a. Dimensiones de página (max -2)
    if not report['page_size'].get('match', True):
        page_diff = report['page_size']['diff_width'] + report['page_size']['diff_height']
        geometry_penalty += min(2, page_diff / 30)
    
    # 1b. Área de página (max -1)
    if not report['page_size'].get('match', True):
        area_diff_pct = abs(report['page_size'].get('diff_area', 0)) / orig['page_size']['area'] * 100
        geometry_penalty += min(1, area_diff_pct / 5)
    
    if geometry_penalty > 0:
        score -= geometry_penalty
        penalties.append(f"Page geometry: -{geometry_penalty:.2f}")
        detailed_breakdown['page_geometry'] = geometry_penalty
    
    # ============================================================================
    # 2. MÁRGENES (peso: 8% del total) - CRÍTICO para layout
    # ============================================================================
    margin_penalty = 0
    
    if report['margins']:
        # Cada margen tiene peso diferente según impacto visual
        margin_weights = {
            'left': 2.5,    # Crítico para lectura
            'top': 2.0,     # Importante para balance
            'right': 1.5,   # Menos crítico
            'bottom': 2.0   # Importante para balance
        }
        
        for margin, weight in margin_weights.items():
            if margin in report['margins']:
                diff = report['margins'][margin]['diff']
                diff_pct = report['margins'][margin]['diff_percent']
                # Penalización progresiva: más error = más penalización
                margin_penalty += min(weight, (diff / 5) + (diff_pct / 30))
    
    if margin_penalty > 0:
        score -= margin_penalty
        penalties.append(f"Margins: -{margin_penalty:.2f}")
        detailed_breakdown['margins'] = margin_penalty
    
    # ============================================================================
    # 3. COLUMNAS (peso: 12% del total) - CRÍTICO para estructura
    # ============================================================================
    column_penalty = 0
    
    for col in ['left', 'right']:
        if col in report['columns']:
            c = report['columns'][col]
            col_weight = 6 if col == 'right' else 5  # Right más visible
            
            # 3a. Ancho de columna (lo más importante)
            width_diff_pct = c['width']['diff_percent']
            column_penalty += min(col_weight * 0.5, width_diff_pct / 4)
            
            # 3b. Posición X de columna
            x_diff = c['x_position']['diff']
            column_penalty += min(col_weight * 0.25, x_diff / 10)
            
            # 3c. Altura de columna (indica contenido mal distribuido)
            height_diff = c['height']['diff']
            column_penalty += min(col_weight * 0.15, height_diff / 20)
            
            # 3d. Consistencia de ancho (desviación estándar)
            std_diff = abs(c['width']['std_original'] - c['width']['std_generated'])
            column_penalty += min(col_weight * 0.1, std_diff / 3)
    
    # 3e. Gutter (espacio entre columnas) - CRÍTICO
    if 'diff' in report.get('gutter', {}):
        gutter_diff = report['gutter']['diff']
        gutter_pct = report['gutter']['diff_percent']
        column_penalty += min(1, (gutter_diff / 5) + (gutter_pct / 20))
    
    if column_penalty > 0:
        score -= column_penalty
        penalties.append(f"Columns & layout: -{column_penalty:.2f}")
        detailed_breakdown['columns'] = column_penalty
    
    # ============================================================================
    # 4. TIPOGRAFÍA - TAMAÑOS (peso: 12% del total) - MUY CRÍTICO
    # ============================================================================
    font_size_penalty = 0
    
    if 'sizes' in report['fonts']:
        fs = report['fonts']['sizes']['statistics']
        
        # 4a. Tamaño máximo (títulos) - MUY visible
        font_size_penalty += min(3, fs['max']['diff'] * 3)
        
        # 4b. Tamaño promedio (texto body) - MUY CRÍTICO
        font_size_penalty += min(3, fs['avg']['diff'] * 3)
        
        # 4c. Tamaño mínimo (detalles)
        font_size_penalty += min(2, fs['min']['diff'] * 2)
        
        # 4d. Mediana (balance general)
        font_size_penalty += min(2, fs['median']['diff'] * 2)
        
        # 4e. Desviación estándar (consistencia tipográfica)
        font_size_penalty += min(2, fs['std']['diff'] * 1.5)
    
    if font_size_penalty > 0:
        score -= font_size_penalty
        penalties.append(f"Font sizes: -{font_size_penalty:.2f}")
        detailed_breakdown['font_sizes'] = font_size_penalty
    
    # ============================================================================
    # 5. TIPOGRAFÍA - DISTRIBUCIÓN (peso: 10% del total)
    # ============================================================================
    font_dist_penalty = 0
    
    if report['fonts']['distribution_diff']:
        # Calcular diferencia ponderada por importancia de cada tamaño
        for size, diff_data in report['fonts']['distribution_diff'].items():
            diff_abs = abs(diff_data['diff'])
            orig_count = diff_data['original']
            
            # Tamaños más usados tienen más peso
            if orig_count > 50:  # Muy usado
                font_dist_penalty += diff_abs / 8
            elif orig_count > 20:  # Medianamente usado
                font_dist_penalty += diff_abs / 12
            else:  # Poco usado
                font_dist_penalty += diff_abs / 20
        
        font_dist_penalty = min(10, font_dist_penalty)
    
    if font_dist_penalty > 0:
        score -= font_dist_penalty
        penalties.append(f"Font distribution: -{font_dist_penalty:.2f}")
        detailed_breakdown['font_distribution'] = font_dist_penalty
    
    # ============================================================================
    # 6. TIPOGRAFÍA - FAMILIAS (peso: 8% del total) - CRÍTICO para apariencia
    # ============================================================================
    font_family_penalty = 0
    
    if 'families' in report['fonts']:
        if not report['fonts']['families']['match']:
            # Fuente diferente es MUY visible
            font_family_penalty = 8
        
        # Penalización adicional por cantidad de fuentes diferentes
        orig_fonts = set(report['fonts']['families']['original'])
        gen_fonts = set(report['fonts']['families']['generated'])
        missing_fonts = orig_fonts - gen_fonts
        extra_fonts = gen_fonts - orig_fonts
        
        if missing_fonts or extra_fonts:
            font_family_penalty += min(2, (len(missing_fonts) + len(extra_fonts)) * 0.5)
    
    if font_family_penalty > 0:
        score -= font_family_penalty
        penalties.append(f"Font families: -{font_family_penalty:.2f}")
        detailed_breakdown['font_families'] = font_family_penalty
    
    # ============================================================================
    # 7. COLORES (peso: 10% del total) - MUY visible
    # ============================================================================
    color_penalty = 0
    
    # 7a. Colores faltantes (CRÍTICO)
    if report['colors']['missing_colors']:
        # Cada color faltante es muy visible
        color_penalty += len(report['colors']['missing_colors']) * 2.5
    
    # 7b. Colores extra (problema menor)
    if report['colors']['extra_colors']:
        color_penalty += len(report['colors']['extra_colors']) * 1
    
    # 7c. Distribución de colores
    if report['colors']['distribution_comparison']:
        for color, diff_data in report['colors']['distribution_comparison'].items():
            diff_abs = abs(diff_data['diff'])
            orig_count = diff_data['original']
            
            # Colores muy usados tienen más peso
            if orig_count > 50:
                color_penalty += diff_abs / 15
            elif orig_count > 10:
                color_penalty += diff_abs / 25
            else:
                color_penalty += diff_abs / 40
    
    color_penalty = min(10, color_penalty)
    
    if color_penalty > 0:
        score -= color_penalty
        penalties.append(f"Colors: -{color_penalty:.2f}")
        detailed_breakdown['colors'] = color_penalty
    
    # ============================================================================
    # 8. ESPACIADO - LÍNEAS (peso: 7% del total)
    # ============================================================================
    line_spacing_penalty = 0
    
    if 'line_spacing' in report['spacing']:
        ls = report['spacing']['line_spacing']['statistics']
        
        # 8a. Promedio de interlineado (MUY visible)
        line_spacing_penalty += min(3, ls['avg']['diff'] * 2.5)
        
        # 8b. Máximo (espacios grandes muy visibles)
        line_spacing_penalty += min(2, ls['max']['diff'] / 2)
        
        # 8c. Desviación estándar (consistencia)
        line_spacing_penalty += min(1.5, ls['std']['diff'] * 1.5)
        
        # 8d. Mediana (balance general)
        line_spacing_penalty += min(0.5, ls['median']['diff'] / 2)
    
    if line_spacing_penalty > 0:
        score -= line_spacing_penalty
        penalties.append(f"Line spacing: -{line_spacing_penalty:.2f}")
        detailed_breakdown['line_spacing'] = line_spacing_penalty
    
    # ============================================================================
    # 9. ESPACIADO - BLOQUES (peso: 8% del total) - MUY visible
    # ============================================================================
    block_spacing_penalty = 0
    
    if 'block_spacing' in report['spacing']:
        bs = report['spacing']['block_spacing']['statistics']
        
        # 9a. Promedio (espaciado general entre secciones)
        block_spacing_penalty += min(3.5, bs['avg']['diff'] * 1.8)
        
        # 9b. Máximo (espacios grandes entre secciones)
        block_spacing_penalty += min(2, bs['max']['diff'] / 8)
        
        # 9c. Mínimo (espacios pequeños muy visibles)
        block_spacing_penalty += min(1.5, bs['min']['diff'] * 1.2)
        
        # 9d. Desviación estándar (consistencia crítica)
        block_spacing_penalty += min(1, bs['std']['diff'] / 3)
    
    if block_spacing_penalty > 0:
        score -= block_spacing_penalty
        penalties.append(f"Block spacing: -{block_spacing_penalty:.2f}")
        detailed_breakdown['block_spacing'] = block_spacing_penalty
    
    # ============================================================================
    # 10. CONTENIDO TEXTUAL (peso: 6% del total)
    # ============================================================================
    content_penalty = 0
    
    # 10a. Similitud textual (muy importante para CVs)
    if report['content']['text_similarity'] < 100:
        similarity_diff = 100 - report['content']['text_similarity']
        content_penalty += min(3, similarity_diff / 8)
    
    # 10b. Cantidad de palabras
    words_diff = report['content']['total_words']['diff']
    if words_diff > 0:
        words_diff_pct = words_diff / report['content']['total_words']['original'] * 100
        content_penalty += min(1.5, words_diff_pct / 5)
    
    # 10c. Cantidad de bloques (estructura)
    blocks_diff = report['content']['total_blocks']['diff']
    if blocks_diff > 0:
        content_penalty += min(1, blocks_diff / 3)
    
    # 10d. Cantidad de líneas
    lines_diff = report['content']['total_lines']['diff']
    if lines_diff > 0:
        content_penalty += min(0.5, lines_diff / 10)
    
    if content_penalty > 0:
        score -= content_penalty
        penalties.append(f"Content: -{content_penalty:.2f}")
        detailed_breakdown['content'] = content_penalty
    
    # ============================================================================
    # 11. SECCIONES (peso: 5% del total)
    # ============================================================================
    section_penalty = 0
    
    # 11a. Secciones faltantes (CRÍTICO)
    if report['sections']['missing_sections']:
        section_penalty += len(report['sections']['missing_sections']) * 2
    
    # 11b. Secciones extra (menos crítico)
    if report['sections']['extra_sections']:
        section_penalty += len(report['sections']['extra_sections']) * 0.5
    
    # 11c. Orden de secciones diferente (penalización menor)
    if not report['sections']['match'] and not report['sections']['missing_sections']:
        section_penalty += 0.5
    
    section_penalty = min(5, section_penalty)
    
    if section_penalty > 0:
        score -= section_penalty
        penalties.append(f"Sections: -{section_penalty:.2f}")
        detailed_breakdown['sections'] = section_penalty
    
    # ============================================================================
    # 12. ALINEACIÓN (peso: 3% del total)
    # ============================================================================
    alignment_penalty = 0
    
    # Diferencias en alineación afectan la apariencia profesional
    for align_type in ['left_aligned', 'right_aligned', 'centered']:
        if align_type in report['alignment']:
            diff = report['alignment'][align_type]['diff']
            if diff > 0:
                alignment_penalty += min(1, diff / 5)
    
    alignment_penalty = min(3, alignment_penalty)
    
    if alignment_penalty > 0:
        score -= alignment_penalty
        penalties.append(f"Alignment: -{alignment_penalty:.2f}")
        detailed_breakdown['alignment'] = alignment_penalty
    
    # ============================================================================
    # 13. DENSIDAD (peso: 4% del total)
    # ============================================================================
    density_penalty = 0
    
    # 13a. Utilización de página
    util_diff = report['density']['utilization_percentage']['diff']
    if util_diff > 0:
        density_penalty += min(2.5, util_diff / 2.5)
    
    # 13b. Palabras por área (densidad de contenido)
    wpa_diff = report['density']['words_per_area']['diff']
    if wpa_diff > 0:
        wpa_diff_pct = wpa_diff / report['density']['words_per_area']['original'] * 100 if report['density']['words_per_area']['original'] > 0 else 0
        density_penalty += min(1.5, wpa_diff_pct / 5)
    
    if density_penalty > 0:
        score -= density_penalty
        penalties.append(f"Density: -{density_penalty:.2f}")
        detailed_breakdown['density'] = density_penalty
    
    # ============================================================================
    # 14. PROPORCIONES Y RATIOS (peso: 4% del total)
    # ============================================================================
    ratio_penalty = 0
    
    if report['ratios'] and 'column_width_ratio' in report['ratios']:
        # 14a. Ratio entre columnas (CRÍTICO para balance visual)
        ratio_diff_pct = report['ratios']['column_width_ratio']['diff_percent']
        ratio_penalty += min(2.5, ratio_diff_pct / 3)
        
        # 14b. Ratios individuales de columnas
        if 'left_column_ratio' in report['ratios']:
            left_diff = report['ratios']['left_column_ratio']['diff']
            ratio_penalty += min(0.75, left_diff / 0.02)
        
        if 'right_column_ratio' in report['ratios']:
            right_diff = report['ratios']['right_column_ratio']['diff']
            ratio_penalty += min(0.75, right_diff / 0.02)
    
    if ratio_penalty > 0:
        score -= ratio_penalty
        penalties.append(f"Ratios: -{ratio_penalty:.2f}")
        detailed_breakdown['ratios'] = ratio_penalty
    
    # ============================================================================
    # 15. ANÁLISIS MICRO: Posiciones exactas de columnas (peso: 2% adicional)
    # ============================================================================
    position_penalty = 0
    
    for col in ['left', 'right']:
        if col in report['columns']:
            # Posición Y de inicio/fin de columnas
            y_start_diff = report['columns'][col]['y_start']['diff']
            y_end_diff = report['columns'][col]['y_end']['diff']
            
            position_penalty += min(0.5, y_start_diff / 10)
            position_penalty += min(0.5, y_end_diff / 10)
    
    position_penalty = min(2, position_penalty)
    
    if position_penalty > 0:
        score -= position_penalty
        penalties.append(f"Exact positions: -{position_penalty:.2f}")
        detailed_breakdown['positions'] = position_penalty
    
    # ============================================================================
    # 16. ANÁLISIS GLOBAL DEL DOCUMENTO COMPLETO (peso: 6% del total) 🔥
    # ============================================================================
    global_penalty = 0
    
    if report['global_document']:
        # 16a. Límites globales del documento (bounds completos)
        if 'bounds' in report['global_document']:
            bounds = report['global_document']['bounds']
            
            # Ancho y alto total del contenido
            if 'total_width' in bounds:
                width_diff_pct = bounds['total_width']['diff_percent']
                global_penalty += min(1.5, width_diff_pct / 10)
            
            if 'total_height' in bounds:
                height_diff_pct = bounds['total_height']['diff_percent']
                global_penalty += min(1.5, height_diff_pct / 10)
            
            # Límites superior e inferior
            if 'topmost' in bounds:
                global_penalty += min(0.5, bounds['topmost']['diff'] / 10)
            if 'bottommost' in bounds:
                global_penalty += min(0.5, bounds['bottommost']['diff'] / 10)
        
        # 16b. Espaciado vertical global (muy importante)
        if 'global_vertical_spacing' in report['global_document']:
            gvs = report['global_document']['global_vertical_spacing']
            
            # Promedio de espaciado global
            global_penalty += min(1.5, gvs['avg']['diff'] * 0.8)
            
            # Consistencia (desviación estándar)
            if 'std' in gvs:
                global_penalty += min(0.5, gvs['std']['diff'] / 5)
        
        # 16c. Balance del documento (simetría)
        if 'balance' in report['global_document']:
            bal = report['global_document']['balance']
            
            # Balance horizontal
            if 'horizontal_offset' in bal:
                global_penalty += min(0.5, bal['horizontal_offset']['diff'] / 30)
            
            # Balance vertical
            if 'vertical_offset' in bal:
                global_penalty += min(0.5, bal['vertical_offset']['diff'] / 30)
        
        # 16d. Distribución vertical del contenido
        if 'vertical_distribution' in report['global_document']:
            vd = report['global_document']['vertical_distribution']
            
            # Span total de contenido
            if 'content_span' in vd:
                span_diff = vd['content_span']['diff']
                global_penalty += min(0.5, span_diff / 20)
        
        # 16e. Whitespace (espacio en blanco) - crítico para legibilidad
        if 'whitespace' in report['global_document']:
            ws = report['global_document']['whitespace']
            
            # Diferencia en porcentaje de whitespace
            ws_diff = ws['percentage']['diff']
            global_penalty += min(0.8, ws_diff / 8)
            
            # Diferencia en ratio texto:whitespace
            ratio_diff = ws['ratio']['diff']
            global_penalty += min(0.4, ratio_diff / 0.3)
        
        # 16f. Leading (relación line spacing / font size)
        if 'leading' in report['global_document']:
            lead = report['global_document']['leading']
            
            # Diferencia en el ratio de leading
            lead_ratio_diff = lead['ratio']['diff']
            global_penalty += min(0.5, lead_ratio_diff / 0.1)
        
        # 16g. Peso visual de secciones específicas del CV
        if 'section_weights' in report['global_document']:
            sw = report['global_document']['section_weights']
            
            # Penalizar diferencias significativas en las secciones
            for section_name, section_data in sw.items():
                area_diff_pct = section_data['area']['diff_percent']
                if area_diff_pct > 20:  # Más de 20% de diferencia es notable
                    global_penalty += min(0.3, area_diff_pct / 50)
        
        # 16h. Jerarquía visual
        if 'visual_hierarchy' in report['global_document']:
            vh = report['global_document']['visual_hierarchy']
            
            # Si hay diferencias en la jerarquía
            if vh['differences']:
                diff_count = len(vh['differences'])
                global_penalty += min(0.5, diff_count * 0.15)
    
    global_penalty = min(8, global_penalty)  # Aumentado de 6 a 8 para incluir nuevos análisis
    
    if global_penalty > 0:
        score -= global_penalty
        penalties.append(f"Global document: -{global_penalty:.2f}")
        detailed_breakdown['global_document'] = global_penalty
    
    # ============================================================================
    # CÁLCULO FINAL
    # ============================================================================
    
    # Asegurar que el score nunca sea negativo
    final_score = max(0.0, min(100.0, score))
    
    # Agregar breakdown detallado a penalties para debugging
    if detailed_breakdown:
        total_penalties = sum(detailed_breakdown.values())
        penalties.append(f"TOTAL PENALTIES: -{total_penalties:.2f} pts")
        penalties.append(f"Categories affected: {len(detailed_breakdown)}")
    
    return final_score, penalties

def print_ultra_detailed_report(orig, gen, report, score, penalties):
    """Print comprehensive comparison report"""
    print("=" * 120)
    print(" " * 35 + "🔬 ULTRA-DETAILED PDF COMPARISON REPORT")
    print("=" * 120)
    print(f"\n{'🎯 OVERALL SIMILARITY SCORE:':^120}")
    print(f"{'═' * 120}")
    print(f"{score:.2f}/100".center(120))
    print()
    
    if penalties:
        print("📉 PENALTIES BREAKDOWN:")
        for p in penalties:
            print(f"   • {p}")
        print()
    
    # Critical issues
    if report['critical_issues']:
        print("=" * 120)
        print("🚨 CRITICAL ISSUES (Must Fix)")
        print("=" * 120)
        for issue in report['critical_issues']:
            print(f"   {issue}")
        print()
    
    # Recommendations
    if report['recommendations']:
        print("=" * 120)
        print("⚠️  RECOMMENDATIONS (Should Fix)")
        print("=" * 120)
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"   {i}. {rec}")
        print()
    
    # Minor issues
    if report['minor_issues']:
        print("=" * 120)
        print("ℹ️  MINOR ISSUES (Optional)")
        print("=" * 120)
        for issue in report['minor_issues'][:10]:  # Show first 10
            print(f"   {issue}")
        if len(report['minor_issues']) > 10:
            print(f"   ... and {len(report['minor_issues']) - 10} more minor issues")
        print()
    
    print("=" * 120)
    print("📐 PAGE & MARGINS")
    print("=" * 120)
    
    # Page size
    if report['page_size'].get('match'):
        print(f"✅ Page size: {orig['page_size']['width']} x {orig['page_size']['height']} pts")
    else:
        ps = report['page_size']
        print(f"❌ Page size:")
        print(f"   Original:  {ps['original']['width']} x {ps['original']['height']} pts")
        print(f"   Generated: {ps['generated']['width']} x {ps['generated']['height']} pts")
        print(f"   Diff:      {ps['diff_width']:.2f} x {ps['diff_height']:.2f} pts")
    
    # Margins
    if report['margins']:
        print(f"\n📏 Margins:")
        for margin in ['left', 'top', 'right', 'bottom']:
            m = report['margins'][margin]
            status = "✅" if m['diff'] < 2 else "⚠️"
            print(f"   {status} {margin.capitalize():8s}: {m['generated']:6.2f}pt  (orig: {m['original']:6.2f}pt, diff: {m['diff']:5.2f}pt, {m['diff_percent']:5.1f}%)")
    
    print("\n" + "=" * 120)
    print("📊 COLUMNS & LAYOUT")
    print("=" * 120)
    
    for col in ['left', 'right']:
        if col in report['columns']:
            c = report['columns'][col]
            print(f"\n📌 {col.upper()} COLUMN:")
            print(f"   X position:    {c['x_position']['generated']:6.2f}pt  (orig: {c['x_position']['original']:6.2f}pt, diff: {c['x_position']['diff']:5.2f}pt)")
            print(f"   Width:         {c['width']['generated']:6.2f}pt  (orig: {c['width']['original']:6.2f}pt, diff: {c['width']['diff']:5.2f}pt, {c['width']['diff_percent']:5.1f}%)")
            print(f"   Height:        {c['height']['generated']:6.2f}pt  (orig: {c['height']['original']:6.2f}pt, diff: {c['height']['diff']:5.2f}pt)")
            print(f"   Y start:       {c['y_start']['generated']:6.2f}pt  (orig: {c['y_start']['original']:6.2f}pt, diff: {c['y_start']['diff']:5.2f}pt)")
            print(f"   Y end:         {c['y_end']['generated']:6.2f}pt  (orig: {c['y_end']['original']:6.2f}pt, diff: {c['y_end']['diff']:5.2f}pt)")
            print(f"   Block count:   {c['block_count']['generated']:3d}      (orig: {c['block_count']['original']:3d}, diff: {c['block_count']['diff']:3d})")
    
    if 'diff' in report.get('gutter', {}):
        g = report['gutter']
        status = "✅" if g['diff'] < 3 else "⚠️"
        print(f"\n{status} GUTTER (space between columns): {g['generated']:.2f}pt  (orig: {g['original']:.2f}pt, diff: {g['diff']:.2f}pt, {g['diff_percent']:.1f}%)")
    
    print("\n" + "=" * 120)
    print("🔤 TYPOGRAPHY & FONTS")
    print("=" * 120)
    
    # Font sizes
    fs = report['fonts']['sizes']
    print(f"\nFont Size Statistics:")
    for stat in ['min', 'max', 'avg', 'median', 'std']:
        s = fs['statistics'][stat]
        status = "✅" if s['diff'] < 0.5 else "⚠️"
        print(f"   {status} {stat.capitalize():8s}: {s['generated']:6.2f}pt  (orig: {s['original']:6.2f}pt, diff: {s['diff']:5.2f}pt)")
    
    print(f"\n📋 Font Sizes Used:")
    print(f"   Original:  {fs['original']}")
    print(f"   Generated: {fs['generated']}")
    
    if fs['missing']:
        print(f"   ❌ Missing:  {fs['missing']}")
    if fs['extra']:
        print(f"   ➕ Extra:    {fs['extra']}")
    
    # Font families
    if 'families' in report['fonts']:
        ff = report['fonts']['families']
        print(f"\n🔠 Font Families:")
        print(f"   Original:  {ff['original']}")
        print(f"   Generated: {ff['generated']}")
        status = "✅" if ff['match'] else "❌"
        match_text = "✓" if ff['match'] else f"should be '{ff['primary_original']}'"
        print(f"   {status} Primary font: '{ff['primary_generated']}' {match_text}")
    
    # Font distribution (top differences)
    if report['fonts']['distribution_diff']:
        print(f"\n📊 Font Size Distribution Differences (top 15):")
        sorted_diffs = sorted(report['fonts']['distribution_diff'].items(),
                            key=lambda x: abs(x[1]['diff']), reverse=True)[:15]
        print(f"   {'Size':>6s}  {'Original':>8s}  {'Generated':>8s}  {'Diff':>8s}  {'%':>7s}")
        print(f"   {'-'*47}")
        for size, diff in sorted_diffs:
            print(f"   {size:6.1f}pt  {diff['original']:8d}  {diff['generated']:8d}  {diff['diff']:+8d}  {diff['diff_percent']:+6.1f}%")
    
    print("\n" + "=" * 120)
    print("🎨 COLORS")
    print("=" * 120)
    
    c = report['colors']
    print(f"\n📊 Color Summary:")
    print(f"   Original colors:  {c['original_count']} unique → {c['original_colors']}")
    print(f"   Generated colors: {c['generated_count']} unique → {c['generated_colors']}")
    print(f"   Primary original:  {c['primary_original']}")
    print(f"   Primary generated: {c['primary_generated']}")
    
    if c['missing_colors']:
        print(f"   ❌ Missing: {c['missing_colors']}")
    if c['extra_colors']:
        print(f"   ➕ Extra:   {c['extra_colors']}")
    
    if c['distribution_comparison']:
        print(f"\n📊 Color Usage Differences:")
        for color, diff in list(c['distribution_comparison'].items())[:10]:
            print(f"   {color}:  orig={diff['original']:4d}, gen={diff['generated']:4d}, diff={diff['diff']:+4d}")
    
    print("\n" + "=" * 120)
    print("📏 SPACING ANALYSIS")
    print("=" * 120)
    
    # Line spacing
    if 'line_spacing' in report['spacing']:
        ls = report['spacing']['line_spacing']
        print(f"\n📐 Line Spacing (between consecutive lines):")
        for stat in ['min', 'max', 'avg', 'median', 'std']:
            s = ls['statistics'][stat]
            status = "✅" if s['diff'] < 1.0 else "⚠️"
            print(f"   {status} {stat.capitalize():8s}: {s['generated']:6.2f}pt  (orig: {s['original']:6.2f}pt, diff: {s['diff']:5.2f}pt)")
        
        print(f"\n   Unique line spacings:")
        print(f"   Original:  {ls['unique_values_original'][:10]}{'...' if len(ls['unique_values_original']) > 10 else ''}")
        print(f"   Generated: {ls['unique_values_generated'][:10]}{'...' if len(ls['unique_values_generated']) > 10 else ''}")
    
    # Block spacing
    if 'block_spacing' in report['spacing']:
        bs = report['spacing']['block_spacing']
        print(f"\n📦 Block Spacing (between consecutive blocks):")
        for stat in ['min', 'max', 'avg', 'median', 'std']:
            s = bs['statistics'][stat]
            status = "✅" if s['diff'] < 2.0 else "⚠️"
            print(f"   {status} {stat.capitalize():8s}: {s['generated']:6.2f}pt  (orig: {s['original']:6.2f}pt, diff: {s['diff']:5.2f}pt)")
    
    print("\n" + "=" * 120)
    print("📝 CONTENT ANALYSIS")
    print("=" * 120)
    
    cont = report['content']
    print(f"\n📊 Content Statistics:")
    print(f"   Lines:      {cont['total_lines']['generated']:4d}  (orig: {cont['total_lines']['original']:4d}, diff: {cont['total_lines']['diff']:3d})")
    print(f"   Characters: {cont['total_characters']['generated']:4d}  (orig: {cont['total_characters']['original']:4d}, diff: {cont['total_characters']['diff']:3d})")
    print(f"   Words:      {cont['total_words']['generated']:4d}  (orig: {cont['total_words']['original']:4d}, diff: {cont['total_words']['diff']:3d})")
    print(f"   Blocks:     {cont['total_blocks']['generated']:4d}  (orig: {cont['total_blocks']['original']:4d}, diff: {cont['total_blocks']['diff']:3d})")
    
    status = "✅" if cont['text_similarity'] > 95 else "⚠️"
    print(f"\n{status} Text Similarity: {cont['text_similarity']:.2f}%")
    
    print("\n" + "=" * 120)
    print("📑 SECTIONS")
    print("=" * 120)
    
    sec = report['sections']
    print(f"\n📋 Section Detection:")
    print(f"   Original:  {sec['original_sections']}")
    print(f"   Generated: {sec['generated_sections']}")
    
    status = "✅" if sec['match'] else "⚠️"
    print(f"\n{status} Sections match: {sec['match']}")
    
    if sec['missing_sections']:
        print(f"   ❌ Missing: {sec['missing_sections']}")
    if sec['extra_sections']:
        print(f"   ➕ Extra:   {sec['extra_sections']}")
    
    print("\n" + "=" * 120)
    print("↔️  ALIGNMENT")
    print("=" * 120)
    
    al = report['alignment']
    print(f"\n📊 Alignment Distribution:")
    print(f"   Left-aligned:   {al['left_aligned']['generated']:3d}  (orig: {al['left_aligned']['original']:3d}, diff: {al['left_aligned']['diff']:3d})")
    print(f"   Right-aligned:  {al['right_aligned']['generated']:3d}  (orig: {al['right_aligned']['original']:3d}, diff: {al['right_aligned']['diff']:3d})")
    print(f"   Centered:       {al['centered']['generated']:3d}  (orig: {al['centered']['original']:3d}, diff: {al['centered']['diff']:3d})")
    
    print("\n" + "=" * 120)
    print("📊 DENSITY & RATIOS")
    print("=" * 120)
    
    dens = report['density']
    print(f"\n📏 Page Density:")
    status = "✅" if dens['utilization_percentage']['diff'] < 3 else "⚠️"
    print(f"   {status} Utilization:   {dens['utilization_percentage']['generated']:6.2f}%  (orig: {dens['utilization_percentage']['original']:6.2f}%, diff: {dens['utilization_percentage']['diff']:5.2f}%)")
    print(f"   Words/area:    {dens['words_per_area']['generated']:6.4f}  (orig: {dens['words_per_area']['original']:6.4f}, diff: {dens['words_per_area']['diff']:6.4f})")
    
    if report['ratios']:
        rat = report['ratios']
        print(f"\n⚖️  Column Ratios:")
        print(f"   Left column ratio:   {rat['left_column_ratio']['generated']:.4f}  (orig: {rat['left_column_ratio']['original']:.4f}, diff: {rat['left_column_ratio']['diff']:.4f})")
        print(f"   Right column ratio:  {rat['right_column_ratio']['generated']:.4f}  (orig: {rat['right_column_ratio']['original']:.4f}, diff: {rat['right_column_ratio']['diff']:.4f})")
        status = "✅" if rat['column_width_ratio']['diff_percent'] < 5 else "⚠️"
        print(f"   {status} Width ratio (L:R): {rat['column_width_ratio']['generated']:.4f}  (orig: {rat['column_width_ratio']['original']:.4f}, diff: {rat['column_width_ratio']['diff_percent']:.1f}%)")
    else:
        print(f"\n⚖️  Column Ratios: (not available)")
    
    # === GLOBAL DOCUMENT ANALYSIS (additional details) ===
    if report['global_document']:
        print("\n" + "=" * 120)
        print("🌍 GLOBAL DOCUMENT ANALYSIS")
        print("=" * 120)
        
        gd = report['global_document']
        
        # Whitespace
        if 'whitespace' in gd:
            ws = gd['whitespace']
            print(f"\n📄 Whitespace (Negative Space):")
            print(f"   Whitespace:    {ws['percentage']['generated']:6.2f}%  (orig: {ws['percentage']['original']:6.2f}%, diff: {ws['percentage']['diff']:5.2f}%)")
            print(f"   Text/WS ratio: {ws['ratio']['generated']:6.4f}  (orig: {ws['ratio']['original']:6.4f}, diff: {ws['ratio']['diff']:6.4f})")
        
        # Leading
        if 'leading' in gd:
            lead = gd['leading']
            print(f"\n📏 Leading (Line Spacing / Font Size Ratio):")
            print(f"   Leading ratio: {lead['ratio']['generated']:.4f}  (orig: {lead['ratio']['original']:.4f}, diff: {lead['ratio']['diff']:.4f})")
            print(f"   Standard leading is 1.2 (120% of font size)")
        
        # Section weights
        if 'section_weights' in gd:
            sw = gd['section_weights']
            if sw:
                print(f"\n🎯 Visual Weight by Section:")
                for section_name, section_data in sorted(sw.items()):
                    area_diff_pct = section_data['area']['diff_percent']
                    status = "✅" if area_diff_pct < 20 else "⚠️"
                    print(f"   {status} {section_name:12s}: area {section_data['area']['generated']:6.0f}  (orig: {section_data['area']['original']:6.0f}, diff: {area_diff_pct:5.1f}%)")
        
        # Visual hierarchy
        if 'visual_hierarchy' in gd:
            vh = gd['visual_hierarchy']
            if vh['differences']:
                print(f"\n👁️  Visual Hierarchy Differences:")
                for diff in vh['differences']:
                    print(f"   Level {diff['level']}: {diff['generated_size']:.1f}pt ({diff['generated_usage']:.1f}%) vs {diff['original_size']:.1f}pt ({diff['original_usage']:.1f}%)")
            else:
                print(f"\n👁️  Visual Hierarchy: ✅ Matches perfectly")
        
        # Global vertical spacing
        if 'global_vertical_spacing' in gd:
            gvs = gd['global_vertical_spacing']
            print(f"\n📊 Global Vertical Spacing:")
            print(f"   Average:  {gvs['avg']['generated']:6.2f}pt  (orig: {gvs['avg']['original']:6.2f}pt, diff: {gvs['avg']['diff']:5.2f}pt)")
            print(f"   Median:   {gvs['median']['generated']:6.2f}pt  (orig: {gvs['median']['original']:6.2f}pt, diff: {gvs['median']['diff']:5.2f}pt)")
            print(f"   Std Dev:  {gvs['std']['generated']:6.2f}pt  (orig: {gvs['std']['original']:6.2f}pt, diff: {gvs['std']['diff']:5.2f}pt)")
        
        # Global bounds
        if 'bounds' in gd:
            bounds = gd['bounds']
            print(f"\n🔲 Document Boundaries:")
            print(f"   Top:      {bounds['topmost']['generated']:6.2f}pt  (orig: {bounds['topmost']['original']:6.2f}pt, diff: {bounds['topmost']['diff']:5.2f}pt)")
            print(f"   Bottom:   {bounds['bottommost']['generated']:6.2f}pt  (orig: {bounds['bottommost']['original']:6.2f}pt, diff: {bounds['bottommost']['diff']:5.2f}pt)")
            print(f"   Left:     {bounds['leftmost']['generated']:6.2f}pt  (orig: {bounds['leftmost']['original']:6.2f}pt, diff: {bounds['leftmost']['diff']:5.2f}pt)")
            print(f"   Right:    {bounds['rightmost']['generated']:6.2f}pt  (orig: {bounds['rightmost']['original']:6.2f}pt, diff: {bounds['rightmost']['diff']:5.2f}pt)")
            print(f"   Width:    {bounds['total_width']['generated']:6.2f}pt  (orig: {bounds['total_width']['original']:6.2f}pt, diff: {bounds['total_width']['diff_percent']:5.1f}%)")
            print(f"   Height:   {bounds['total_height']['generated']:6.2f}pt  (orig: {bounds['total_height']['original']:6.2f}pt, diff: {bounds['total_height']['diff_percent']:5.1f}%)")
        
        # Balance
        if 'balance' in gd:
            bal = gd['balance']
            print(f"\n⚖️  Document Balance (Center of Mass):")
            print(f"   Horizontal offset: {bal['horizontal_offset']['generated']:6.2f}pt  (orig: {bal['horizontal_offset']['original']:6.2f}pt, diff: {bal['horizontal_offset']['diff']:5.2f}pt)")
            print(f"   Vertical offset:   {bal['vertical_offset']['generated']:6.2f}pt  (orig: {bal['vertical_offset']['original']:6.2f}pt, diff: {bal['vertical_offset']['diff']:5.2f}pt)")
    
    print("\n" + "=" * 120)
    print(f"{'End of Report':^120}")
    print("=" * 120 + "\n")

def main():
    original_path = "EN_NicolasFredes_CV.pdf"
    generated_path = "generated.pdf"
    
    print("\n" + "=" * 120)
    print("🔬 ULTRA-DETAILED PDF COMPARISON TOOL".center(120))
    print("=" * 120 + "\n")
    
    print("📖 [1/4] Extracting ultra-detailed information from ORIGINAL PDF...")
    orig = extract_ultra_detailed_pdf_info(original_path)
    print(f"      ✓ Extracted {orig['page_count']} page(s), {orig['content_analysis']['total_blocks']} blocks, "
          f"{orig['content_analysis']['total_words']} words")
    
    print("\n📖 [2/4] Extracting ultra-detailed information from GENERATED PDF...")
    gen = extract_ultra_detailed_pdf_info(generated_path)
    print(f"      ✓ Extracted {gen['page_count']} page(s), {gen['content_analysis']['total_blocks']} blocks, "
          f"{gen['content_analysis']['total_words']} words")
    
    print("\n🔍 [3/4] Performing ultra-detailed comparison across all dimensions...")
    report = ultra_detailed_comparison(orig, gen)
    print(f"      ✓ Analyzed: page, margins, columns, fonts, colors, spacing, content, sections, alignment, density, ratios")
    
    print("\n🎯 [4/4] Calculating similarity score...")
    score, penalties = calculate_ultra_detailed_similarity(report, orig, gen)
    print(f"      ✓ Score calculated: {score:.2f}/100\n")
    
    print_ultra_detailed_report(orig, gen, report, score, penalties)
    
    # Save ultra-detailed report
    output = {
        'metadata': {
            'comparison_version': '2.0_ultra_detailed',
            'original_file': original_path,
            'generated_file': generated_path
        },
        'score': score,
        'penalties': penalties,
        'original_analysis': orig,
        'generated_analysis': gen,
        'comparison_report': report
    }
    
    output_file = 'detailed_comparison.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Ultra-detailed report saved to: {output_file}")
    print(f"   File size: {len(json.dumps(output)) / 1024:.1f} KB\n")
    
    return score

if __name__ == "__main__":
    try:
        score = main()
        # Always exit 0 if comparison completed successfully
        # Score is informational, not an error condition
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
