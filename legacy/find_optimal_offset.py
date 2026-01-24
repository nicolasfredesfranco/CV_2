#!/usr/bin/env python3
"""
Búsqueda exhaustiva del offset Y óptimo
Basado en el análisis que muestra delta consistente de +1.5 a +2.0pts
"""
import subprocess
import json
import os

def test_offset(y_offset):
    """Prueba un offset específico y retorna el score"""
    # Guardar configuración
    config = {'x_offset': 0.0, 'y_offset': y_offset, 'scale': 1.0}
    with open('../generation_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    # Generar CV
    result = subprocess.run(['python3', '3_generate_cv_precise.py'],
                          capture_output=True, text=True, cwd='.')
    if result.returncode != 0:
        return None
    
    # Analizar
    result = subprocess.run(['python3', '2_analyze_differences_deep.py'],
                          capture_output=True, text=True, cwd='.')
    if result.returncode != 0:
        return None
    
    # Leer score
    try:
        with open('../analysis_report.json', 'r') as f:
            report = json.load(f)
        return report['global_score']
    except:
        return None

def main():
    print("="*100)
    print("BÚSQUEDA EXHAUSTIVA DE OFFSET Y ÓPTIMO")
    print("="*100)
    print("\nRango actual: Y=-1.5 (compensar delta de +1.5pts detectado)")
    print("Probando valores alrededor del punto óptimo conocido...\n")
    
    # Basado en el delta promedio observado (+1.5 a +2.0), 
    # y sabiendo que el óptimo conocido es Y=+10.9,
    # necesitamos RESTAR el delta, así que probamos Y = 10.9 - 1.7 ≈ 9.2
    # Pero el actual tiene delta positivo, así que necesitamos AUMENTAR Y
    
    # Valor actual en config
    try:
        with open('../generation_config.json', 'r') as f:
            current_config = json.load(f)
        current_y = current_config.get('y_offset', 0.0)
    except:
        current_y = 0.0
    
    print(f"Configuración actual: Y = {current_y:+.2f}")
    print(f"Delta promedio detectado: +1.7pts (CV generado está ARRIBA)")
    print(f"Corrección necesaria: RESTAR 1.7pts del offset Y")
    print(f"Nuevo offset estimado: Y = {current_y - 1.7:+.2f}\n")
    
    # Búsqueda fina alrededor del valor corregido
    base = current_y - 1.7
    test_range = [base + offset for offset in [-0.5, -0.3, -0.1, 0.0, 0.1, 0.3, 0.5]]
    
    results = []
    
    for i, y_val in enumerate(test_range, 1):
        print(f"\n[{i}/{len(test_range)}] Probando Y = {y_val:+.2f}pts...")
        score = test_offset(y_val)
        
        if score is not None:
            results.append((y_val, score))
            print(f"    ✅ Score: {score*100:.4f}%")
        else:
            print(f"    ❌ Error")
    
    # Encontrar mejor
    if results:
        best_y, best_score = max(results, key=lambda x: x[1])
        
        print("\n" + "="*100)
        print("RESULTADO DE LA BÚSQUEDA")
        print("="*100)
        print(f"\nMejor configuración encontrada:")
        print(f"  Y Offset: {best_y:+.4f}pts")
        print(f"  Score: {best_score*100:.6f}%")
        
        # Guardar mejor configuración
        best_config = {'x_offset': 0.0, 'y_offset': best_y, 'scale': 1.0}
        with open('../generation_config_best.json', 'w') as f:
            json.dump(best_config, f, indent=2)
        with open('../generation_config.json', 'w') as f:
            json.dump(best_config, f, indent=2)
        
        print(f"\n✅ Configuración guardada en generation_config.json")
        print("="*100)
        
        # Generar CV final con mejor configuración
        print("\nGenerando CV final...")
        subprocess.run(['python3', '3_generate_cv_precise.py'], cwd='.')
        
        return best_score
    else:
        print("\n❌ No se pudo completar la búsqueda")
        return None

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
