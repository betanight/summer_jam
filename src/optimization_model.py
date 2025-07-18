"""
Optimization model using Genetic Algorithm to solve the Traveling Salesman Problem.
"""

import numpy as np
import random
from typing import List, Tuple, Callable
import logging
import time
from copy import deepcopy

logger = logging.getLogger(__name__)

class GeneticAlgorithmTSP:
    """
    Genetic Algorithm implementation for solving the Traveling Salesman Problem.
    """
    
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.01, 
                 crossover_rate: float = 0.8, elite_size: int = 5):
        """
        Initialize the Genetic Algorithm.
        
        Args:
            population_size (int): Size of the population
            mutation_rate (float): Probability of mutation
            crossover_rate (float): Probability of crossover
            elite_size (int): Number of best individuals to preserve
        """
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_size = elite_size
        self.best_route = None
        self.best_distance = float('inf')
        
        logger.info(f"GeneticAlgorithmTSP initialized with population_size={population_size}")
    
    def create_individual(self, num_locations: int) -> List[int]:
        """
        Create a random individual (route).
        
        Args:
            num_locations (int): Number of locations
            
        Returns:
            List[int]: Random route
        """
        return random.sample(range(num_locations), num_locations)
    
    def create_initial_population(self, num_locations: int) -> List[List[int]]:
        """
        Create initial population of routes.
        
        Args:
            num_locations (int): Number of locations
            
        Returns:
            List[List[int]]: Initial population
        """
        population = []
        for _ in range(self.population_size):
            individual = self.create_individual(num_locations)
            population.append(individual)
        
        logger.info(f"Created initial population of {self.population_size} individuals")
        return population
    
    def calculate_fitness(self, route: List[int], distance_matrix: np.ndarray) -> float:
        """
        Calculate fitness (inverse of distance) for a route.
        
        Args:
            route (List[int]): Route to evaluate
            distance_matrix (np.ndarray): Distance matrix
            
        Returns:
            float: Fitness value (higher is better)
        """
        from distance_calculator import calculate_route_distance
        distance = calculate_route_distance(route, distance_matrix)
        return 1.0 / (distance + 1e-10)  # Avoid division by zero
    
    def rank_population(self, population: List[List[int]], distance_matrix: np.ndarray) -> List[Tuple[float, List[int]]]:
        """
        Rank population by fitness.
        
        Args:
            population (List[List[int]]): Population to rank
            distance_matrix (np.ndarray): Distance matrix
            
        Returns:
            List[Tuple[float, List[int]]]: Ranked population (fitness, route)
        """
        fitness_results = {}
        for i, route in enumerate(population):
            fitness = self.calculate_fitness(route, distance_matrix)
            fitness_results[i] = fitness
        
        return sorted(fitness_results.items(), key=lambda x: x[1], reverse=True)
    
    def selection(self, ranked_population: List[Tuple[int, float]]) -> List[List[int]]:
        """
        Select individuals for breeding using tournament selection.
        
        Args:
            ranked_population (List[Tuple[int, float]]): Ranked population
            
        Returns:
            List[List[int]]: Selected individuals
        """
        selection_results = []
        for i in range(self.elite_size):
            selection_results.append(ranked_population[i][0])
        
        # Tournament selection for the rest
        for i in range(self.population_size - self.elite_size):
            tournament_size = 3
            tournament = random.sample(ranked_population, tournament_size)
            winner = max(tournament, key=lambda x: x[1])
            selection_results.append(winner[0])
        
        return selection_results
    
    def crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """
        Perform ordered crossover (OX) between two parents.
        
        Args:
            parent1, parent2 (List[int]): Parent routes
            
        Returns:
            List[int]: Offspring route
        """
        if random.random() > self.crossover_rate:
            return parent1
        
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        
        # Create child with segment from parent1
        child = [-1] * size
        child[start:end] = parent1[start:end]
        
        # Fill remaining positions with elements from parent2
        remaining = [x for x in parent2 if x not in child[start:end]]
        j = 0
        for i in range(size):
            if child[i] == -1:
                child[i] = remaining[j]
                j += 1
        
        return child
    
    def mutate(self, route: List[int]) -> List[int]:
        """
        Perform swap mutation on a route.
        
        Args:
            route (List[int]): Route to mutate
            
        Returns:
            List[int]: Mutated route
        """
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(route)), 2)
            route[i], route[j] = route[j], route[i]
        
        return route
    
    def breed_population(self, mating_pool: List[List[int]]) -> List[List[int]]:
        """
        Breed new population from mating pool.
        
        Args:
            mating_pool (List[List[int]]): Selected individuals
            
        Returns:
            List[List[int]]: New population
        """
        children = []
        
        # Keep elite individuals
        for i in range(self.elite_size):
            children.append(mating_pool[i])
        
        # Breed the rest
        for i in range(self.population_size - self.elite_size):
            parent1 = random.choice(mating_pool)
            parent2 = random.choice(mating_pool)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            children.append(child)
        
        return children
    
    def evolve_population(self, population: List[List[int]], distance_matrix: np.ndarray) -> List[List[int]]:
        """
        Evolve population for one generation.
        
        Args:
            population (List[List[int]]): Current population
            distance_matrix (np.ndarray): Distance matrix
            
        Returns:
            List[List[int]]: Evolved population
        """
        # Rank population
        ranked_population = self.rank_population(population, distance_matrix)
        
        # Selection
        selection_results = self.selection(ranked_population)
        mating_pool = [population[i] for i in selection_results]
        
        # Breeding
        children = self.breed_population(mating_pool)
        
        return children
    
    def optimize(self, distance_matrix: np.ndarray, num_generations: int = 100) -> dict:
        """
        Run the genetic algorithm optimization.
        
        Args:
            distance_matrix (np.ndarray): Distance matrix
            num_generations (int): Number of generations to evolve
            
        Returns:
            dict: Optimization results
        """
        start_time = time.time()
        num_locations = len(distance_matrix)
        
        # Create initial population
        population = self.create_initial_population(num_locations)
        
        # Track progress
        progress = []
        best_distances = []
        
        logger.info(f"Starting optimization with {num_generations} generations")
        
        for generation in range(num_generations):
            # Evolve population
            population = self.evolve_population(population, distance_matrix)
            
            # Track best route
            ranked_population = self.rank_population(population, distance_matrix)
            best_route_idx = ranked_population[0][0]
            best_route = population[best_route_idx]
            
            from distance_calculator import calculate_route_distance
            best_distance = calculate_route_distance(best_route, distance_matrix)
            
            if best_distance < self.best_distance:
                self.best_distance = best_distance
                self.best_route = best_route.copy()
            
            progress.append(generation)
            best_distances.append(best_distance)
            
            if generation % 10 == 0:
                logger.info(f"Generation {generation}: Best distance = {best_distance:.2f} km")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        results = {
            'best_route': self.best_route,
            'best_distance': self.best_distance,
            'execution_time': execution_time,
            'num_generations': num_generations,
            'progress': progress,
            'best_distances': best_distances,
            'final_population': population
        }
        
        logger.info(f"Optimization completed in {execution_time:.3f} seconds")
        logger.info(f"Best route distance: {self.best_distance:.2f} km")
        
        return results

def run_optimization_experiment(coordinates: np.ndarray, distance_matrix: np.ndarray,
                               population_size: int = 50, num_generations: int = 100) -> dict:
    """
    Run complete optimization experiment.
    
    Args:
        coordinates (np.ndarray): Location coordinates
        distance_matrix (np.ndarray): Distance matrix
        population_size (int): GA population size
        num_generations (int): Number of generations
        
    Returns:
        dict: Complete optimization results
    """
    # Initialize GA
    ga = GeneticAlgorithmTSP(population_size=population_size)
    
    # Run optimization
    results = ga.optimize(distance_matrix, num_generations)
    
    return results 