#!/usr/bin/env python3
"""
iterate_master.py
Orquestador maestro de iteración automática
Ejecuta hasta 10,000 ciclos para lograr convergencia perfecta
"""
import subprocess
import json
import time
import os
from datetime import datetime

class CVIterator:
    def __init__(self, max_iterations=10000, target_score=0.999):
        self.max_iterations = max_iterations
        self.target_score = target_score
        self.config = {
            'x_offset': 0.0,
            'y_offset': 0.0,
            'scale': 1.0
        }
        self.history = []
        self.best_score = 0.0
        self.best_config = None
        
    def save_config(self):
        """Guarda configuración actual para el generador"""
        with open('../generation_config.json', 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def run_generation(self):
        """Ejecuta el generador de CV"""
        result = subprocess.run(
            ['python3', '3_generate_cv_precise.py'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    def run_comparison(self, cycle):
        """Genera comparación visual"""
        output_path = f'../outputs/comparison_cycle_{cycle}.png'
        result = subprocess.run(
            ['python3', '1_deploy_side_by_side.py',
             '../outputs/Nicolas_Fredes_CV.pdf',
             '../Objetivo_No_editar.pdf',
             output_path],
            capture_output=True,
            text=True
        )
        return result.returncode == 0, output_path
    
    def run_analysis(self):
        """Ejecuta análisis de diferencias"""
        result = subprocess.run(
            ['python3', '2_analyze_differences_deep.py'],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"⚠️  Error en análisis: {result.stderr}")
            return None
        
        # Leer reporte
        try:
            with open('../analysis_report.json', 'r') as f:
                report = json.load(f)
            return report
        except Exception as e:
            print(f"⚠️  Error leyendo reporte: {e}")
            return None
    
    def calculate_corrections(self, report):
        """
        Calcula correcciones inteligentes basadas en el reporte
        Usa un enfoque de descenso de gradiente adaptativo
        """
        if not report or 'section_deltas' not in report:
            return {'x_offset': 0.0, 'y_offset': 0.0, 'scale': 0.0}
        
        deltas = report['section_deltas']
        
        if not deltas:
            return {'x_offset': 0.0, 'y_offset': 0.0, 'scale': 0.0}
        
        # Calcular promedio ponderado de deltas
        total_dx = 0
        total_dy = 0
        count = 0
        
        for section, delta_dict in deltas.items():
            dx = delta_dict.get('dx', 0.0)
            dy = delta_dict.get('dy', 0.0)
            total_dx += dx
            total_dy += dy
            count += 1
        
        if count == 0:
            return {'x_offset': 0.0, 'y_offset': 0.0, 'scale': 0.0}
        
        avg_dx = total_dx / count
        avg_dy = total_dy / count
        
        # Learning rate adaptativo ultra-preciso
        score = report.get('global_score', 0.0)
        
        if score > 0.99:
            # Muy cerca: correcciones mínimas
            learning_rate = 0.005
        elif score > 0.95:
            # Cerca del objetivo: correcciones muy pequeñas
            learning_rate = 0.02
        elif score > 0.90:
            # Bastante cerca: ajuste fino
            learning_rate = 0.05
        elif score > 0.85:
            # Moderadamente cerca: correcciones medias
            learning_rate = 0.15
        else:
            # Lejos: correcciones grandes
            learning_rate = 0.3
        
        # Calcular correcciones (invertir signos para corregir)
        correction_x = -avg_dx * learning_rate
        correction_y = -avg_dy * learning_rate
        
        # Clamp dinámico basado en score
        if score > 0.95:
            max_correction = 0.5  # Muy conservador cerca del objetivo
        elif score > 0.90:
            max_correction = 1.0
        else:
            max_correction = 3.0
            
        correction_x = max(min(correction_x, max_correction), -max_correction)
        correction_y = max(min(correction_y, max_correction), -max_correction)
        
        return {
            'x_offset': correction_x,
            'y_offset': correction_y,
            'scale': 0.0  # Por ahora no ajustamos escala
        }
    
    def apply_corrections(self, corrections):
        """Aplica correcciones a la configuración"""
        self.config['x_offset'] += corrections['x_offset']
        self.config['y_offset'] += corrections['y_offset']
        self.config['scale'] += corrections['scale']
    
    def run_cycle(self, cycle):
        """Ejecuta un ciclo completo de iteración"""
        print(f"\n{'='*100}")
        print(f"CICLO {cycle:05d} / {self.max_iterations}")
        print(f"{'='*100}")
        print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. Guardar configuración
        self.save_config()
        
        # 2. Generar CV
        print(f"\n[1/3] Generando CV...")
        if not self.run_generation():
            print("❌ Error en generación")
            return None
        
        # 3. Analizar diferencias
        print(f"\n[2/3] Analizando diferencias...")
        report = self.run_analysis()
        
        if not report:
            print("❌ Error en análisis")
            return None
        
        score = report.get('global_score', 0.0)
        
        # 4. Generar comparación visual (cada 10 ciclos o al final)
        if cycle % 10 == 0 or score > self.target_score:
            print(f"\n[3/3] Generando comparación visual...")
            success, comp_path = self.run_comparison(cycle)
            if success:
                print(f"   📸 Comparación: {comp_path}")
        
        # 5. Calcular y aplicar correcciones
        corrections = self.calculate_corrections(report)
        
        print(f"\n{'─'*100}")
        print(f"RESULTADOS CICLO {cycle}")
        print(f"{'─'*100}")
        print(f"   🎯 Score Global:  {score*100:.4f}%")
        print(f"   🔧 Corrección X:  {corrections['x_offset']:+.4f}pts")
        print(f"   🔧 Corrección Y:  {corrections['y_offset']:+.4f}pts")
        print(f"   📊 Config actual: X={self.config['x_offset']:+.2f}, Y={self.config['y_offset']:+.2f}")
        
        # Actualizar mejor score
        if score > self.best_score:
            self.best_score = score
            self.best_config = self.config.copy()
            print(f"   🌟 ¡NUEVO MEJOR SCORE! {score*100:.4f}%")
        
        print(f"{'─'*100}")
        
        # Detectar divergencia: si el score cae más de 20% respecto al mejor
        if self.best_score > 0.7 and score < (self.best_score - 0.20):
            print(f"   ⚠️  DIVERGENCIA DETECTADA! Score cayó de {self.best_score*100:.2f}% a {score*100:.2f}%")
            print(f"   🔄 Reseteando a mejor configuración...")
            self.config = self.best_config.copy()
            # No aplicar correcciones este ciclo
        elif score < self.target_score:
            # Aplicar correcciones para siguiente ciclo
            self.apply_corrections(corrections)
        
        # Guardar historial
        self.history.append({
            'cycle': cycle,
            'score': score,
            'config': self.config.copy(),
            'corrections': corrections
        })
        
        return report
    
    def save_history(self):
        """Guarda historial de iteraciones"""
        with open('../iteration_history.json', 'w') as f:
            json.dump({
                'iterations': self.history,
                'best_score': self.best_score,
                'best_config': self.best_config
            }, f, indent=2)
        print(f"✅ Historial guardado: iteration_history.json")
    
    def run(self):
        """Ejecuta el loop principal de iteración"""
        print(f"\n{'#'*100}")
        print(f"CV PIXEL-PERFECT ITERATOR")
        print(f"{'#'*100}")
        print(f"Objetivo: Score ≥ {self.target_score*100:.2f}%")
        print(f"Máximo de iteraciones: {self.max_iterations:,}")
        print(f"{'#'*100}\n")
        
        start_time = time.time()
        
        for cycle in range(1, self.max_iterations + 1):
            report = self.run_cycle(cycle)
            
            if not report:
                print(f"\n⚠️  Error en ciclo {cycle}, continuando...")
                time.sleep(0.5)
                continue
            
            score = report.get('global_score', 0.0)
            
            # Verificar convergencia
            if score >= self.target_score:
                elapsed = time.time() - start_time
                print(f"\n{'#'*100}")
                print(f"🎉 ¡CONVERGENCIA ALCANZADA!")
                print(f"{'#'*100}")
                print(f"   Ciclo: {cycle}")
                print(f"   Score: {score*100:.6f}%")
                print(f"   Tiempo: {elapsed/60:.2f} minutos")
                print(f"   Configuración final:")
                print(f"     - X Offset: {self.config['x_offset']:+.4f}pts")
                print(f"     - Y Offset: {self.config['y_offset']:+.4f}pts")
                print(f"{'#'*100}\n")
                break
            
            # Guardar progreso cada 100 iteraciones
            if cycle % 100 == 0:
                self.save_history()
                elapsed = time.time() - start_time
                rate = cycle / elapsed
                eta = (self.max_iterations - cycle) / rate
                print(f"\n📊 Progreso: {cycle}/{self.max_iterations} ({cycle/self.max_iterations*100:.1f}%)")
                print(f"   Mejor score: {self.best_score*100:.4f}%")
                print(f"   Velocidad: {rate:.2f} iter/s")
                print(f"   ETA: {eta/60:.1f} min\n")
            
            # Pausa mínima
            time.sleep(0.05)
        
        # Guardar historial final
        self.save_history()
        
        # Resumen final
        elapsed = time.time() - start_time
        print(f"\n{'#'*100}")
        print(f"ITERACIÓN COMPLETADA")
        print(f"{'#'*100}")
        print(f"   Total de ciclos: {len(self.history)}")
        print(f"   Mejor score: {self.best_score*100:.6f}%")
        print(f"   Tiempo total: {elapsed/60:.2f} minutos")
        print(f"   Velocidad promedio: {len(self.history)/elapsed:.2f} iter/s")
        
        if self.best_config:
            print(f"\n   Mejor configuración:")
            print(f"     - X Offset: {self.best_config['x_offset']:+.4f}pts")
            print(f"     - Y Offset: {self.best_config['y_offset']:+.4f}pts")
        
        print(f"{'#'*100}\n")

if __name__ == "__main__":
    import sys
    
    max_iter = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    target = float(sys.argv[2]) if len(sys.argv) > 2 else 0.999
    
    iterator = CVIterator(max_iterations=max_iter, target_score=target)
    iterator.run()
