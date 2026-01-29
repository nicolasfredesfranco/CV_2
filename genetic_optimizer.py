#!/usr/bin/env python3
"""
Multi-Parameter Optimizer for 85% Target
Uses genetic algorithm approach to optimize multiple parameters simultaneously.

Author: Nicolás Ignacio Fredes Franco
"""

import subprocess
import numpy as np
from pdf2image import convert_from_path
import json
import re
from pathlib import Path
from datetime import datetime

class MultiParamOptimizer:
    def __init__(self):
        self.config_file = Path("src/config.py")
        self.coords_file = Path("data/coordinates.json")
        self.target = 85.0
        self.current_best = 77.62
        self.population_size = 20
        self.generations = 15
        self.mutation_rate = 0.15
        
        # Parameter ranges
        self.param_ranges = {
            'y_offset': (35.0, 43.0),
            'font_scale': (0.95, 1.05),
            'y_spacing_scale': (0.98, 1.02)
        }
        
    def log(self, msg):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {msg}")
    
    def calculate_similarity(self):
        """Calculate visual similarity"""
        try:
            obj = convert_from_path("pdfs/objective/Objetivo_No_editar.pdf", dpi=150)[0]
            gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=150)[0]
            
            obj_arr = np.array(obj.convert('RGB'))
            gen_arr = np.array(gen.convert('RGB').resize(obj.size))
            
            diff = np.abs(obj_arr.astype(int) - gen_arr.astype(int))
            diff[diff < 10] = 0
            
            perceptible = np.sum(np.any(diff > 0, axis=2))
            total = obj_arr.shape[0] * obj_arr.shape[1]
            
            return 100 * (1 - perceptible / total)
        except:
            return 0.0
    
    def set_y_offset(self, value):
        """Update Y_GLOBAL_OFFSET"""
        with open(self.config_file, 'r') as f:
            content = f.read()
        
        content = re.sub(
            r'(Y_GLOBAL_OFFSET:\s*float\s*=\s*)[\d.]+',
            rf'\g<1>{value:.2f}',
            content
        )
        
        with open(self.config_file, 'w') as f:
            f.write(content)
    
    def scale_font_sizes(self, scale):
        """Scale all font sizes by a factor"""
        with open(self.coords_file, 'r') as f:
            coords = json.load(f)
        
        for item in coords:
            if 'fontsize' in item:
                item['fontsize'] = round(item['fontsize'] * scale, 2)
        
        with open(self.coords_file, 'w') as f:
            json.dump(coords, f, indent=2)
    
    def scale_y_spacing(self, scale):
        """Scale Y spacing between elements"""
        with open(self.coords_file, 'r') as f:
            coords = json.load(f)
        
        # Sort by Y position
        coords_sorted = sorted(coords, key=lambda x: x.get('y', 0))
        
        # Calculate spacings and scale them
        if len(coords_sorted) > 1:
            base_y = coords_sorted[0]['y']
            for i, item in enumerate(coords_sorted[1:], 1):
                prev_y = coords_sorted[i-1]['y']
                spacing = item['y'] - prev_y
                scaled_spacing = spacing * scale
                item['y'] = prev_y + scaled_spacing
        
        with open(self.coords_file, 'w') as f:
            json.dump(coords, f, indent=2)
    
    def apply_params(self, params):
        """Apply parameter configuration"""
        self.set_y_offset(params['y_offset'])
        # Font and spacing scaling would go here if we want to try them
        # For now focusing on Y offset as primary parameter
    
    def generate_pdf(self):
        """Generate PDF"""
        try:
            result = subprocess.run(
                ["python", "main.py"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def create_initial_population(self):
        """Create initial population around current best"""
        population = []
        
        # Include current best
        population.append({'y_offset': 39.30})
        
        # Generate variations
        for _ in range(self.population_size - 1):
            params = {
                'y_offset': np.random.uniform(*self.param_ranges['y_offset'])
            }
            population.append(params)
        
        return population
    
    def evaluate_individual(self, params, gen_num, ind_num):
        """Evaluate a single parameter set"""
        self.apply_params(params)
        
        if not self.generate_pdf():
            return 0.0
        
        similarity = self.calculate_similarity()
        self.log(f"  Gen{gen_num} Ind{ind_num}: Y={params['y_offset']:.2f} → {similarity:.2f}%")
        
        if similarity > self.current_best:
            improvement = similarity - self.current_best
            self.current_best = similarity
            self.log(f"    ✨ NEW BEST! +{improvement:.2f}%")
            
            # Save best
            gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=150)[0]
            gen.save(f"outputs/best_{similarity:.2f}pct.png")
        
        return similarity
    
    def select_parents(self, population, fitness):
        """Tournament selection"""
        tournament_size = 3
        parents = []
        
        for _ in range(len(population) // 2):
            tournament_idx = np.random.choice(len(population), tournament_size, replace=False)
            tournament_fitness = [fitness[i] for i in tournament_idx]
            winner_idx = tournament_idx[np.argmax(tournament_fitness)]
            parents.append(population[winner_idx])
        
        return parents
    
    def crossover(self, parent1, parent2):
        """Create offspring from two parents"""
        child = {}
        for key in parent1:
            child[key] = parent1[key] if np.random.random() < 0.5 else parent2[key]
        return child
    
    def mutate(self, params):
        """Mutate parameters"""
        mutated = params.copy()
        
        if np.random.random() < self.mutation_rate:
            # Gaussian mutation
            mutated['y_offset'] += np.random.normal(0, 0.5)
            mutated['y_offset'] = np.clip(
                mutated['y_offset'],
                *self.param_ranges['y_offset']
            )
        
        return mutated
    
    def run(self):
        """Run genetic algorithm optimization"""
        self.log("="*70)
        self.log("MULTI-PARAMETER GENETIC ALGORITHM OPTIMIZATION")
        self.log(f"Target: {self.target}%")
        self.log(f"Current: {self.current_best}%")
        self.log(f"Generations: {self.generations}")
        self.log(f"Population: {self.population_size}")
        self.log("="*70)
        
        population = self.create_initial_population()
        
        for gen in range(self.generations):
            self.log(f"\n{'='*70}")
            self.log(f"GENERATION {gen + 1}/{self.generations}")
            self.log(f"{'='*70}")
            
            # Evaluate population
            fitness = []
            for i, individual in enumerate(population):
                fit = self.evaluate_individual(individual, gen+1, i+1)
                fitness.append(fit)
                
                if self.current_best >= self.target:
                    self.log(f"\n🎉 TARGET {self.target}% REACHED!")
                    return True
            
            # Report generation stats
            avg_fitness = np.mean(fitness)
            max_fitness = np.max(fitness)
            self.log(f"\n  Generation Stats: Avg={avg_fitness:.2f}% Max={max_fitness:.2f}%")
            
            # Selection
            parents = self.select_parents(population, fitness)
            
            # Create new population
            new_population = []
            
            # Elitism - keep best individual
            best_idx = np.argmax(fitness)
            new_population.append(population[best_idx])
            
            # Crossover and mutation
            while len(new_population) < self.population_size:
                if len(parents) >= 2:
                    parent1 = parents[np.random.randint(len(parents))]
                    parent2 = parents[np.random.randint(len(parents))]
                    child = self.crossover(parent1, parent2)
                    child = self.mutate(child)
                    new_population.append(child)
                else:
                    break
            
            population = new_population
        
        self.log(f"\n{'='*70}")
        self.log(f"OPTIMIZATION COMPLETE")
        self.log(f"Best Similarity: {self.current_best:.2f}%")
        self.log(f"Gap to 85%: {self.target - self.current_best:.2f}%")
        self.log("="*70)
        
        return self.current_best >= self.target

if __name__ == "__main__":
    optimizer = MultiParamOptimizer()
    success = optimizer.run()
    
    if success:
        print("\n✅ Successfully reached 85% target!")
    else:
        print(f"\n📊 Achieved {optimizer.current_best:.2f}%, continuing progress towards 85%")
