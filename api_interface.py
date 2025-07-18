#!/usr/bin/env python3
"""
API Interface for Software Engineering Team Integration
Provides simple functions for the web team to use the optimization engine
"""

import sys
import os
sys.path.append('src')

import json
import pickle
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
import logging

# Import our modules
from data_loader import load_locations, preprocess_data
from distance_calculator import calculate_distance_matrix
from optimization_model import GeneticAlgorithmTSP
from baseline_model import RandomRouteGenerator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RouteOptimizationAPI:
    """
    Simple API interface for the software engineering team.
    Provides easy-to-use functions for route optimization.
    """
    
    def __init__(self, data_file: str = "data/locations.csv"):
        """
        Initialize the API with location data.
        
        Args:
            data_file (str): Path to the locations CSV file
        """
        self.data_file = data_file
        self.locations_df = None
        self.coordinates = None
        self.location_names = None
        self.distance_matrix = None
        self._load_data()
    
    def _load_data(self):
        """Load and prepare the location data."""
        try:
            # Load and preprocess data
            self.locations_df, self.coordinates, self.location_names = preprocess_data(self.data_file)
            
            # Calculate distance matrix
            self.distance_matrix = calculate_distance_matrix(self.coordinates)
            
            logger.info(f"API initialized with {len(self.location_names)} locations")
            
        except Exception as e:
            logger.error(f"Error initializing API: {e}")
            raise
    
    def get_all_locations(self) -> List[Dict]:
        """
        Get all available locations for the web team.
        
        Returns:
            List[Dict]: List of location dictionaries with id, name, coordinates
        """
        locations = []
        for i, (name, lat, lon) in enumerate(zip(self.location_names, 
                                                 self.coordinates[:, 0], 
                                                 self.coordinates[:, 1])):
            locations.append({
                'id': i,
                'name': name,
                'latitude': float(lat),
                'longitude': float(lon)
            })
        return locations
    
    def optimize_route(self, selected_location_ids: List[int], 
                      population_size: int = 50, 
                      generations: int = 100) -> Dict:
        """
        Optimize a route for selected locations.
        
        Args:
            selected_location_ids (List[int]): List of location IDs to optimize
            population_size (int): GA population size
            generations (int): Number of generations
            
        Returns:
            Dict: Optimization results
        """
        if not selected_location_ids:
            raise ValueError("No locations selected")
        
        if len(selected_location_ids) < 2:
            raise ValueError("Need at least 2 locations for route optimization")
        
        # Filter coordinates and names for selected locations
        selected_coordinates = self.coordinates[selected_location_ids]
        selected_names = [self.location_names[i] for i in selected_location_ids]
        
        # Create distance matrix for selected locations
        selected_distance_matrix = calculate_distance_matrix(selected_coordinates)
        
        # Run optimization
        ga = GeneticAlgorithmTSP(population_size=population_size)
        results = ga.optimize(selected_distance_matrix, generations)
        
        # Convert route indices back to original location IDs
        optimized_route_ids = [selected_location_ids[i] for i in results['best_route']]
        optimized_route_names = [selected_names[i] for i in results['best_route']]
        
        return {
            'optimized_route': {
                'location_ids': optimized_route_ids,
                'location_names': optimized_route_names,
                'total_distance': float(results['best_distance']),
                'execution_time': float(results['execution_time'])
            },
            'algorithm_info': {
                'population_size': population_size,
                'generations': generations,
                'algorithm': 'Genetic Algorithm'
            }
        }
    
    def compare_with_random(self, selected_location_ids: List[int]) -> Dict:
        """
        Compare optimized route with a random route.
        
        Args:
            selected_location_ids (List[int]): List of location IDs
            
        Returns:
            Dict: Comparison results
        """
        if len(selected_location_ids) < 2:
            raise ValueError("Need at least 2 locations")
        
        # Get optimized route
        optimized_result = self.optimize_route(selected_location_ids)
        
        # Generate random route for comparison
        selected_coordinates = self.coordinates[selected_location_ids]
        selected_names = [self.location_names[i] for i in selected_location_ids]
        selected_distance_matrix = calculate_distance_matrix(selected_coordinates)
        
        random_generator = RandomRouteGenerator()
        random_route = random_generator.generate_random_route(len(selected_location_ids))
        
        from distance_calculator import calculate_route_distance
        random_distance = calculate_route_distance(random_route, selected_distance_matrix)
        
        random_route_ids = [selected_location_ids[i] for i in random_route]
        random_route_names = [selected_names[i] for i in random_route]
        
        optimized_distance = optimized_result['optimized_route']['total_distance']
        improvement = ((random_distance - optimized_distance) / random_distance) * 100
        
        return {
            'random_route': {
                'location_ids': random_route_ids,
                'location_names': random_route_names,
                'total_distance': float(random_distance)
            },
            'optimized_route': optimized_result['optimized_route'],
            'comparison': {
                'distance_saved': float(random_distance - optimized_distance),
                'improvement_percentage': float(improvement)
            }
        }
    
    def get_route_visualization_data(self, route_location_ids: List[int]) -> Dict:
        """
        Get data for route visualization (coordinates, names, distances).
        
        Args:
            route_location_ids (List[int]): List of location IDs in route order
            
        Returns:
            Dict: Visualization data
        """
        route_coordinates = self.coordinates[route_location_ids]
        route_names = [self.location_names[i] for i in route_location_ids]
        
        # Calculate distances between consecutive points
        distances = []
        total_distance = 0
        
        for i in range(len(route_coordinates) - 1):
            from distance_calculator import haversine_distance
            lat1, lon1 = route_coordinates[i]
            lat2, lon2 = route_coordinates[i + 1]
            distance = haversine_distance(lat1, lon1, lat2, lon2)
            distances.append(float(distance))
            total_distance += distance
        
        # Add return to start distance
        if len(route_coordinates) > 2:
            lat1, lon1 = route_coordinates[-1]
            lat2, lon2 = route_coordinates[0]
            return_distance = haversine_distance(lat1, lon1, lat2, lon2)
            distances.append(float(return_distance))
            total_distance += return_distance
        
        return {
            'route': {
                'location_ids': route_location_ids,
                'location_names': route_names,
                'coordinates': route_coordinates.tolist(),
                'segment_distances': distances,
                'total_distance': float(total_distance)
            }
        }
    
    def add_custom_location(self, name: str, latitude: float, longitude: float) -> int:
        """
        Add a custom location to the dataset.
        
        Args:
            name (str): Location name
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            
        Returns:
            int: New location ID
        """
        # Validate coordinates
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            raise ValueError("Invalid coordinates")
        
        # Add to existing data
        new_id = len(self.location_names)
        self.location_names.append(name)
        
        # Add coordinates
        new_coord = np.array([[latitude, longitude]])
        self.coordinates = np.vstack([self.coordinates, new_coord])
        
        # Recalculate distance matrix
        self.distance_matrix = calculate_distance_matrix(self.coordinates)
        
        logger.info(f"Added custom location: {name} (ID: {new_id})")
        return new_id
    
    def export_results_to_json(self, results: Dict, filename: str = "optimization_results.json"):
        """
        Export optimization results to JSON for web team.
        
        Args:
            results (Dict): Optimization results
            filename (str): Output filename
        """
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results exported to {filename}")

# Example usage functions for the web team
def create_api_instance():
    """Create and return an API instance."""
    return RouteOptimizationAPI()

def get_sample_optimization():
    """Example function showing how to use the API."""
    api = RouteOptimizationAPI()
    
    # Get all available locations
    locations = api.get_all_locations()
    print(f"Available locations: {len(locations)}")
    
    # Select some locations (first 5)
    selected_ids = [0, 1, 2, 3, 4]
    
    # Optimize route
    result = api.optimize_route(selected_ids)
    print(f"Optimized route: {result['optimized_route']['location_names']}")
    print(f"Total distance: {result['optimized_route']['total_distance']:.2f} km")
    
    # Compare with random
    comparison = api.compare_with_random(selected_ids)
    print(f"Improvement: {comparison['comparison']['improvement_percentage']:.1f}%")
    
    return result

if __name__ == "__main__":
    # Example usage
    result = get_sample_optimization()
    print("\nAPI is ready for web team integration!") 