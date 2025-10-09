#!/usr/bin/env python3
"""
Sistema de Iteración Inteligente para Optimización de PDF
Realiza 100 iteraciones guiadas por análisis del reporte de comparación
"""

import json
import subprocess
import os
import sys
from datetime import datetime
import re

class IntelligentIterator:
    def __init__(self):
        self.iteration = 0
        self.best_score = 71.43
        self.current_score = 71.43
        self.history = []
        self.no_improvement_count = 0
        self.modifications_tried = set()
        
    def run_comparison(self):
        """Ejecuta compare_pdf.py y extrae el score"""
        result = subprocess.run(['python3', 'compare_pdf.py'], 
                              capture_output=True, text=True)
        
        # Extraer score del output
        for line in result.stdout.split('\n'):
            if 'SIMILARITY SCORE:' in line:
                match = re.search(r'(\d+\.\d+)/100', line)
                if match:
                    return float(match.group(1))
        return None
    
    def load_comparison_report(self):
        """Carga el reporte detallado de comparación"""
        try:
            with open('detailed_comparison.json', 'r') as f:
                return json.load(f)
        except:
            return None
    
    def identify_biggest_penalty(self, report):
        """Identifica la penalty más grande del reporte"""
        if not report or 'penalties' not in report:
            return None
        
        penalties = report['penalties']
        # Parsear penalties del formato "Category: -X.XX"
        penalty_dict = {}
        for p in penalties:
            if ':' in p:
                name, value = p.split(':', 1)
                try:
                    val = float(value.strip())
                    # Solo penalties negativas
                    if val < 0:
                        penalty_dict[name.strip()] = val
                except:
                    continue
        
        if not penalty_dict:
            return None
        
        biggest = max(penalty_dict.items(), key=lambda x: abs(x[1]))
        return biggest[0], abs(biggest[1])
    
    def generate_modification(self, penalty_name, penalty_value, report):
        """Genera una modificación específica basada en la penalty"""
        
        modifications = []
        
        # Usar un ciclo de valores para explorar el espacio de soluciones
        cycle_index = self.iteration % 20
        
        if penalty_name == 'Block spacing':
            # Explorar diferentes valores de tolerance
            tolerances = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.05, 
                         1.1, 1.15, 1.2, 0.62, 0.78, 0.88, 0.72, 0.82, 0.92, 1.02]
            new_tolerance = tolerances[cycle_index]
            
            modifications.append({
                'type': 'tolerance',
                'new_value': new_tolerance,
                'description': f'Tolerance = {new_tolerance}'
            })
        
        elif penalty_name == 'Global document':
            # Explorar ajustes verticales
            adjustments = [0.1, -0.1, 0.2, -0.2, 0.3, -0.3, 0.5, -0.5, 0.15, -0.15,
                          0.25, -0.25, 0.35, -0.35, 0.4, -0.4, 0.05, -0.05, 0.45, -0.45]
            adjustment = adjustments[cycle_index]
            
            modifications.append({
                'type': 'y_global_shift',
                'adjustment': adjustment,
                'description': f'Desplazamiento Y global: {adjustment:+.2f}'
            })
        
        elif penalty_name == 'Columns & layout':
            # Explorar ajustes de columnas y banners
            adjustments = [0.5, -0.5, 1.0, -1.0, 1.5, -1.5, 2.0, -2.0, 0.25, -0.25,
                          0.75, -0.75, 1.25, -1.25, 1.75, -1.75, 0.3, -0.3, 0.8, -0.8]
            adjustment = adjustments[cycle_index]
            
            modifications.append({
                'type': 'column_adjustment',
                'adjustment': adjustment,
                'description': f'Ajuste de columnas: {adjustment:+.2f}px'
            })
        
        elif penalty_name == 'Content':
            # Explorar diferentes órdenes de dibujo y filtros
            strategies = ['normal', 'reverse', 'filter_empty', 'no_filter', 
                         'sort_xy', 'sort_yx', 'group_tolerance_1', 'group_tolerance_05',
                         'normal', 'reverse', 'filter_empty', 'no_filter', 
                         'sort_xy', 'sort_yx', 'group_tolerance_1', 'group_tolerance_05',
                         'normal', 'reverse']
            strategy = strategies[cycle_index]
            
            modifications.append({
                'type': 'content_strategy',
                'strategy': strategy,
                'description': f'Estrategia de contenido: {strategy}'
            })
        
        elif penalty_name == 'Margins':
            # Explorar ajustes de márgenes
            adjustments = [0.2, -0.2, 0.4, -0.4, 0.6, -0.6, 0.8, -0.8, 1.0, -1.0,
                          0.3, -0.3, 0.5, -0.5, 0.7, -0.7, 0.1, -0.1, 0.15, -0.15]
            adjustment = adjustments[cycle_index]
            
            modifications.append({
                'type': 'margin_shift',
                'adjustment': adjustment,
                'description': f'Ajuste de márgenes: {adjustment:+.2f}px'
            })
        
        elif penalty_name == 'Font families' or penalty_name == 'Font sizes' or penalty_name == 'Font distribution':
            # Explorar ajustes de fuentes
            adjustments = [0.05, -0.05, 0.1, -0.1, 0.15, -0.15, 0.2, -0.2, 0.02, -0.02,
                          0.08, -0.08, 0.12, -0.12, 0.03, -0.03, 0.07, -0.07, 0.04, -0.04]
            adjustment = adjustments[cycle_index]
            
            modifications.append({
                'type': 'font_adjustment',
                'adjustment': adjustment,
                'penalty_name': penalty_name,
                'description': f'Ajuste de fuente ({penalty_name}): {adjustment:+.3f}'
            })
        
        elif penalty_name == 'Colors':
            # Explorar ajustes de colores
            adjustments = [1, -1, 2, -2, 3, -3, 4, -4, 5, -5,
                          1, -1, 2, -2, 3, -3, 4, -4, 5, -5]
            adjustment = adjustments[cycle_index]
            
            modifications.append({
                'type': 'color_adjustment',
                'adjustment': adjustment,
                'description': f'Ajuste de color: {adjustment:+d} niveles'
            })
        
        else:
            # Para otras penalties, probar ajustes generales
            modifications.append({
                'type': 'general_adjustment',
                'target': penalty_name,
                'cycle': cycle_index,
                'description': f'Ajuste general para {penalty_name} (ciclo {cycle_index})'
            })
        
        return modifications
    
    def apply_modification(self, modification):
        """Aplica una modificación al archivo generate_cv_from_python.py"""
        
        with open('generate_cv_from_python.py', 'r') as f:
            content = f.read()
        
        modified = False
        
        try:
            if modification['type'] == 'tolerance':
                # Cambiar valor de tolerance
                new_val = modification['new_value']
                pattern = r'tolerance = [\d\.]+\s+#.*\n'
                replacement = f'    tolerance = {new_val}  # Óptimo encontrado\n'
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    modified = True
            
            elif modification['type'] == 'y_global_shift':
                # Ajustar todas las posiciones Y
                adjustment = modification['adjustment']
                # Modificar la línea y = span['y']
                pattern = r"y = span\['y'\]"
                replacement = f"y = span['y'] + {adjustment}"
                if pattern in content:
                    # Primero revertir cualquier ajuste previo
                    content = re.sub(r"y = span\['y'\] [+\-] [\d\.]+", "y = span['y']", content)
                    # Luego aplicar el nuevo
                    content = content.replace("y = span['y']", replacement)
                    modified = True
            
            elif modification['type'] == 'column_adjustment':
                # Ajustar anchos de banners
                adjustment = modification['adjustment']
                # Modificar todos los anchos de banners
                def adjust_banner_width(match):
                    name, x, y, w, h = match.groups()
                    new_w = float(w) + adjustment
                    return f"'{name}': ({x}, {y}, {new_w}, {h})"
                
                pattern = r"'(\w[\w\s&]+)': \(([\d\.]+), ([\d\.]+), ([\d\.]+), ([\d\.]+)\)"
                if re.search(pattern, content):
                    content = re.sub(pattern, adjust_banner_width, content)
                    modified = True
            
            elif modification['type'] == 'content_strategy':
                # Modificar estrategia de orden de contenido
                strategy = modification['strategy']
                
                if strategy == 'reverse':
                    # Invertir orden de dibujo
                    content = content.replace(
                        'for y_pos in sorted(lines.keys()):',
                        'for y_pos in sorted(lines.keys(), reverse=True):'
                    )
                    modified = True
                elif strategy == 'normal':
                    # Orden normal
                    content = content.replace(
                        'for y_pos in sorted(lines.keys(), reverse=True):',
                        'for y_pos in sorted(lines.keys()):'
                    )
                    modified = True
                elif strategy == 'filter_empty':
                    # Filtrar elementos vacíos más agresivamente
                    pattern = r"if text and len\(text\.strip\(\)\) > 0:"
                    replacement = "if text and len(text.strip()) > 2:"  # Requiere al menos 3 chars
                    if pattern in content:
                        content = content.replace(pattern, replacement)
                        modified = True
                elif strategy == 'no_filter':
                    # No filtrar elementos vacíos
                    pattern = r"if text and len\(text\.strip\(\)\) > \d+:"
                    replacement = "if text and len(text.strip()) >= 0:"
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        modified = True
            
            elif modification['type'] == 'margin_shift':
                # Ajustar posiciones de banners en Y
                adjustment = modification['adjustment']
                
                def adjust_banner_y(match):
                    name, x, y, w, h = match.groups()
                    new_y = float(y) + adjustment
                    return f"'{name}': ({x}, {new_y}, {w}, {h})"
                
                pattern = r"'(\w[\w\s&]+)': \(([\d\.]+), ([\d\.]+), ([\d\.]+), ([\d\.]+)\)"
                if re.search(pattern, content):
                    content = re.sub(pattern, adjust_banner_y, content)
                    modified = True
            
            elif modification['type'] == 'font_adjustment':
                # Ajustar tamaños de fuente
                adjustment = modification['adjustment']
                # Modificar los tamaños de fuente en la extracción
                pattern = r"size = span\['size'\]"
                replacement = f"size = span['size'] + {adjustment}"
                if pattern in content:
                    # Primero revertir cualquier ajuste previo
                    content = re.sub(r"size = span\['size'\] [+\-] [\d\.]+", "size = span['size']", content)
                    # Luego aplicar el nuevo
                    content = content.replace("size = span['size']", replacement)
                    modified = True
            
            elif modification['type'] == 'color_adjustment':
                # No implementado por ahora (colores son hex)
                modified = False
            
            elif modification['type'] == 'general_adjustment':
                # Ajuste general: modificar tolerance con valor basado en ciclo
                cycle = modification['cycle']
                new_tolerance = 0.6 + (cycle * 0.03)
                if new_tolerance > 1.2:
                    new_tolerance = 0.6
                
                pattern = r'tolerance = [\d\.]+\s+#.*\n'
                replacement = f'    tolerance = {new_tolerance:.2f}  # Óptimo encontrado\n'
                if re.search(pattern, content):
                    content = re.sub(pattern, replacement, content)
                    modified = True
            
            if modified:
                with open('generate_cv_from_python.py', 'w') as f:
                    f.write(content)
                return True
            
            return False
            
        except Exception as e:
            print(f'   ⚠️  Error en apply_modification: {e}')
            return False
    
    def revert_changes(self):
        """Revierte cambios usando git"""
        subprocess.run(['git', 'checkout', 'generate_cv_from_python.py'], 
                      capture_output=True)
    
    def save_best_version(self):
        """Guarda la mejor versión"""
        subprocess.run(['git', 'add', 'generate_cv_from_python.py'], 
                      capture_output=True)
        subprocess.run(['git', 'commit', '-m', 
                       f'Iteration {self.iteration}: Score {self.current_score:.2f}'],
                      capture_output=True)
    
    def generate_pdf(self):
        """Genera el PDF"""
        result = subprocess.run(['python3', 'generate_cv_from_python.py'],
                              capture_output=True, text=True)
        return result.returncode == 0
    
    def iterate(self):
        """Realiza una iteración completa"""
        
        self.iteration += 1
        print(f'\n{"="*70}')
        print(f'🔄 ITERACIÓN #{self.iteration}/100')
        print(f'{"="*70}')
        print(f'📊 Score actual: {self.current_score:.2f}/100')
        print(f'🏆 Mejor score: {self.best_score:.2f}/100')
        
        # Cargar reporte
        report = self.load_comparison_report()
        if not report:
            print('❌ No se pudo cargar el reporte')
            return False
        
        # Identificar penalty más grande
        penalty_info = self.identify_biggest_penalty(report)
        if not penalty_info:
            print('❌ No se pudo identificar penalty')
            return False
        
        penalty_name, penalty_value = penalty_info
        print(f'🎯 Penalty objetivo: {penalty_name} (-{penalty_value:.2f} pts)')
        
        # Generar modificación
        modifications = self.generate_modification(penalty_name, penalty_value, report)
        if not modifications:
            print('❌ No se pudo generar modificación')
            return False
        
        modification = modifications[0]
        print(f'🔧 Modificación: {modification.get("description", modification["type"])}')
        
        # Aplicar modificación
        if not self.apply_modification(modification):
            print('⚠️  No se pudo aplicar modificación')
            return False
        
        # Generar PDF
        print('📄 Generando PDF...', end=' ', flush=True)
        if not self.generate_pdf():
            print('❌ Error')
            self.revert_changes()
            return False
        print('✅')
        
        # Ejecutar comparación
        print('🔍 Comparando...', end=' ', flush=True)
        new_score = self.run_comparison()
        if new_score is None:
            print('❌ Error')
            self.revert_changes()
            return False
        print(f'✅ {new_score:.2f}/100')
        
        # Evaluar mejora
        improvement = new_score - self.current_score
        
        if new_score > self.current_score:
            print(f'✅ MEJORA: +{improvement:.2f} pts')
            self.current_score = new_score
            if new_score > self.best_score:
                self.best_score = new_score
                print(f'🏆 NUEVO MEJOR SCORE: {self.best_score:.2f}/100')
            self.save_best_version()
            self.no_improvement_count = 0
        else:
            print(f'❌ EMPEORÓ: {improvement:.2f} pts - REVIRTIENDO')
            self.revert_changes()
            self.no_improvement_count += 1
        
        # Guardar historial
        self.history.append({
            'iteration': self.iteration,
            'timestamp': datetime.now().isoformat(),
            'penalty_targeted': penalty_name,
            'penalty_value': penalty_value,
            'modification': modification,
            'score_before': self.current_score if improvement <= 0 else self.current_score - improvement,
            'score_after': new_score,
            'improvement': improvement,
            'kept': improvement > 0
        })
        
        # Guardar historial a archivo
        with open('iteration_history.json', 'w') as f:
            json.dump({
                'current_iteration': self.iteration,
                'current_score': self.current_score,
                'best_score': self.best_score,
                'history': self.history
            }, f, indent=2)
        
        # Verificar condiciones de salida
        if self.current_score >= 99.0:
            print(f'\n🎉 ¡OBJETIVO ALCANZADO! Score: {self.current_score:.2f}/100')
            return 'success'
        
        if self.no_improvement_count >= 15:
            print(f'\n⚠️  Sin mejora en 15 iteraciones. Re-evaluando estrategia...')
            self.no_improvement_count = 0
            # Aquí podrías cambiar de estrategia
        
        return True
    
    def run(self, max_iterations=100):
        """Ejecuta el loop principal de iteraciones"""
        
        print('╔══════════════════════════════════════════════════════════╗')
        print('║        SISTEMA DE ITERACIÓN INTELIGENTE                 ║')
        print('║     Optimización de PDF Guiada por Análisis             ║')
        print('╚══════════════════════════════════════════════════════════╝')
        print(f'\n🎯 Objetivo: Score >= 99.0/100')
        print(f'🔄 Iteraciones máximas: {max_iterations}')
        print(f'📊 Score inicial: {self.current_score:.2f}/100')
        
        for i in range(max_iterations):
            result = self.iterate()
            
            if result == 'success':
                break
            elif result == False:
                continue
        
        # Resumen final
        print(f'\n{"="*70}')
        print(f'📊 RESUMEN FINAL')
        print(f'{"="*70}')
        print(f'🔄 Iteraciones completadas: {self.iteration}')
        print(f'🏆 Mejor score alcanzado: {self.best_score:.2f}/100')
        print(f'📈 Mejora total: +{self.best_score - 71.43:.2f} pts')
        print(f'📁 Historial guardado en: iteration_history.json')
        print(f'✅ Versión final en: generate_cv_from_python.py')
        print(f'📄 PDF final en: generated.pdf')

if __name__ == '__main__':
    iterator = IntelligentIterator()
    iterator.run(100)

