"""
Baseline model for route generation using random selection.
This serves as a comparison point for the optimization algorithms.
"""

import numpy as np
import random
from typing import List, Tuple
import logging
import time

logger = logging.getLogger(__name__)

class RandomRouteGenerator:
    """
    Baseline model that generates random routes for comparison.
    """
    
    def __init__(self, seed: int = 42):
        """
        Initialize the random route generator.
        
        Args:
            seed (int): Random seed for reproducibility
        """
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)
        logger.info(f"RandomRouteGenerator initialized with seed {seed}")
    
    def generate_random_route(self, num_locations: int) -> List[int]:
        """
        Generate a random route visiting all locations exactly once.
        
        Args:
            num_locations (int): Number of locations to visit
            
        Returns:
            List[int]: Random route as list of location indices
        """
        route = list(range(num_locations))
        random.shuffle(route)
        
        logger.info(f"Generated random route: {route}")
        return route
    
    def generate_multiple_routes(self, num_locations: int, num_routes: int = 10) -> List[List[int]]:
        """
        Generate multiple random routes for statistical analysis.
        
        Args:
            num_locations (int): Number of locations
            num_routes (int): Number of random routes to generate
            
        Returns:
            List[List[int]]: List of random routes
        """
        routes = []
        for i in range(num_routes):
            route = self.generate_random_route(num_locations)
            routes.append(route)
        
        logger.info(f"Generated {num_routes} random routes")
        return routes
    
    def evaluate_routes(self, routes: List[List[int]], distance_matrix: np.ndarray) -> dict:
        """
        Evaluate multiple routes and calculate statistics.
        
        Args:
            routes (List[List[int]]): List of routes to evaluate
            distance_matrix (np.ndarray): Distance matrix
            
        Returns:
            dict: Statistics about the routes
        """
        from distance_calculator import calculate_route_distance
        
        distances = []
        for route in routes:
            distance = calculate_route_distance(route, distance_matrix)
            distances.append(distance)
        
        stats = {
            'num_routes': len(routes),
            'distances': distances,
            'mean_distance': np.mean(distances),
            'std_distance': np.std(distances),
            'min_distance': np.min(distances),
            'max_distance': np.max(distances),
            'best_route': routes[np.argmin(distances)],
            'best_distance': np.min(distances)
        }
        
        logger.info(f"Route evaluation complete. Mean distance: {stats['mean_distance']:.2f} km")
        return stats

def run_baseline_experiment(coordinates: np.ndarray, distance_matrix: np.ndarray, 
                           num_routes: int = 10) -> dict:
    """
    Run complete baseline experiment with timing.
    
    Args:
        coordinates (np.ndarray): Location coordinates
        distance_matrix (np.ndarray): Distance matrix
        num_routes (int): Number of random routes to generate
        
    Returns:
        dict: Complete experiment results
    """
    start_time = time.time()
    
    # Initialize generator
    generator = RandomRouteGenerator()
    
    # Generate routes
    routes = generator.generate_multiple_routes(len(coordinates), num_routes)
    
    # Evaluate routes
    stats = generator.evaluate_routes(routes, distance_matrix)
    
    # Calculate timing
    end_time = time.time()
    execution_time = end_time - start_time
    
    results = {
        'execution_time': execution_time,
        'num_locations': len(coordinates),
        'num_routes_generated': num_routes,
        'best_route': stats['best_route'],
        'best_distance': stats['best_distance'],
        'mean_distance': stats['mean_distance'],
        'std_distance': stats['std_distance'],
        'all_routes': routes,
        'all_distances': stats['distances']
    }
    
    logger.info(f"Baseline experiment completed in {execution_time:.3f} seconds")
    logger.info(f"Best random route distance: {results['best_distance']:.2f} km")
    
    return results 