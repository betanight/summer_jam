#!/usr/bin/env python3
"""
API interface for the route optimization system.
Provides a clean interface for web applications to interact with the optimization engine.
"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional
import time
import json

# Import our modules
from src.data_loader import DataLoader
from src.distance_calculator import DistanceCalculator
from src.baseline_model import RandomRouteGenerator
from src.optimization_model import GeneticAlgorithmTSP

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RouteOptimizationAPI:
    """
    Main API class for route optimization functionality.
    Provides methods for loading data, optimizing routes, and comparing results.
    """
    
    def __init__(self, data_file: str = "data/locations.csv"):
        """
        Initialize the API with location data.
        
        Args:
            data_file (str): Path to the CSV file containing location data
        """
        self.data_file = data_file
        self.data_loader = DataLoader(data_file)
        self.distance_calculator = None
        self.baseline_model = None
        self.optimization_model = None
        self.coordinates = None
        self.location_names = []
        self.locations = []
        
        # Initialize the system
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize all components of the optimization system."""
        try:
            # Load and preprocess data
            self.coordinates, self.location_names = self.data_loader.load_data()
            self.data_loader.preprocess_data()
            self.locations = self.data_loader.get_locations()
            
            # Initialize distance calculator
            self.distance_calculator = DistanceCalculator(self.coordinates)
            
            # Initialize models
            self.baseline_model = RandomRouteGenerator()
            self.optimization_model = GeneticAlgorithmTSP(len(self.coordinates))
            
            logger.info(f"API initialized with {len(self.coordinates)} locations")
            
        except Exception as e:
            logger.error(f"Error initializing API: {e}")
            raise
    
    def get_all_locations(self) -> List[Dict[str, Any]]:
        """
        Get all available locations.
        
        Returns:
            List[Dict[str, Any]]: List of location dictionaries
        """
        return self.locations
    
    def add_custom_location(self, name: str, latitude: float, longitude: float) -> int:
        """
        Add a custom location to the system.
        
        Args:
            name (str): Location name
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            
        Returns:
            int: ID of the new location
        """
        try:
            # Add location to data loader
            new_id = self.data_loader.add_location(name, latitude, longitude)
            
            # Update our local references
            self.locations = self.data_loader.get_locations()
            self.coordinates = self.data_loader.coordinates
            self.location_names = self.data_loader.location_names
            
            # Reinitialize distance calculator with new coordinates
            self.distance_calculator = DistanceCalculator(self.coordinates)
            
            # Reinitialize models with new number of locations
            self.baseline_model = RandomRouteGenerator()
            self.optimization_model = GeneticAlgorithmTSP(len(self.coordinates))
            
            logger.info(f"Added custom location: {name} (ID: {new_id})")
            return new_id
            
        except Exception as e:
            logger.error(f"Error adding custom location: {e}")
            raise
    
    def optimize_route(self, location_ids: List[int]) -> Dict[str, Any]:
        """
        Optimize a route for the given location IDs.
        
        Args:
            location_ids (List[int]): List of location IDs to optimize
            
        Returns:
            Dict[str, Any]: Optimization results including route and metrics
        """
        try:
            if len(location_ids) < 2:
                raise ValueError("Need at least 2 locations to optimize")
            
            # Validate location IDs
            valid_ids = [loc['id'] for loc in self.locations]
            for loc_id in location_ids:
                if loc_id not in valid_ids:
                    raise ValueError(f"Invalid location ID: {loc_id}")
            
            # Get coordinates for selected locations
            selected_coords = []
            selected_names = []
            for loc_id in location_ids:
                location = next(loc for loc in self.locations if loc['id'] == loc_id)
                selected_coords.append([location['latitude'], location['longitude']])
                selected_names.append(location['name'])
            
            selected_coords = np.array(selected_coords)
            
            # Create distance calculator for selected locations
            temp_distance_calc = DistanceCalculator(selected_coords)
            
            # Run optimization
            start_time = time.time()
            optimized_route = self.optimization_model.optimize(temp_distance_calc)
            execution_time = time.time() - start_time
            
            # Calculate total distance
            total_distance = temp_distance_calc.calculate_route_distance(optimized_route)
            
            # Get location names in optimized order
            optimized_names = [selected_names[i] for i in optimized_route]
            optimized_ids = [location_ids[i] for i in optimized_route]
            
            result = {
                'optimized_route': {
                    'location_ids': optimized_ids,
                    'location_names': optimized_names,
                    'total_distance': total_distance,
                    'execution_time': execution_time
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error optimizing route: {e}")
            raise
    
    def compare_with_random(self, location_ids: List[int]) -> Dict[str, Any]:
        """
        Compare optimized route with a random route.
        
        Args:
            location_ids (List[int]): List of location IDs to compare
            
        Returns:
            Dict[str, Any]: Comparison results
        """
        try:
            if len(location_ids) < 2:
                raise ValueError("Need at least 2 locations to compare")
            
            # Get optimized route
            optimized_result = self.optimize_route(location_ids)
            optimized_distance = optimized_result['optimized_route']['total_distance']
            
            # Get coordinates for selected locations
            selected_coords = []
            for loc_id in location_ids:
                location = next(loc for loc in self.locations if loc['id'] == loc_id)
                selected_coords.append([location['latitude'], location['longitude']])
            
            selected_coords = np.array(selected_coords)
            temp_distance_calc = DistanceCalculator(selected_coords)
            
            # Generate random route
            random_route = self.baseline_model.generate_random_route(len(selected_coords))
            random_distance = temp_distance_calc.calculate_route_distance(random_route)
            
            # Calculate improvement
            improvement = ((random_distance - optimized_distance) / random_distance) * 100
            
            comparison = {
                'random_route': {
                    'distance': random_distance,
                    'route': random_route
                },
                'optimized_route': {
                    'distance': optimized_distance,
                    'route': optimized_result['optimized_route']['location_ids']
                },
                'improvement_percentage': improvement,
                'distance_saved': random_distance - optimized_distance
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing routes: {e}")
            raise
    
    def get_route_visualization_data(self, route_ids: List[int]) -> Dict[str, Any]:
        """
        Get visualization data for a route (simplified for web deployment).
        
        Args:
            route_ids (List[int]): List of location IDs in route order
            
        Returns:
            Dict[str, Any]: Visualization data
        """
        try:
            # Get coordinates and names for the route
            route_coordinates = []
            route_names = []
            
            for loc_id in route_ids:
                location = next(loc for loc in self.locations if loc['id'] == loc_id)
                route_coordinates.append([location['latitude'], location['longitude']])
                route_names.append(location['name'])
            
            # Calculate total distance
            coords_array = np.array(route_coordinates)
            temp_distance_calc = DistanceCalculator(coords_array)
            total_distance = temp_distance_calc.calculate_route_distance(list(range(len(route_coordinates))))
            
            visualization_data = {
                'route_coordinates': route_coordinates,
                'route_names': route_names,
                'total_distance': total_distance,
                'num_locations': len(route_ids)
            }
            
            return visualization_data
            
        except Exception as e:
            logger.error(f"Error getting visualization data: {e}")
            raise
    
    def get_street_routing_data(self, route_ids: List[int]) -> Dict[str, Any]:
        """
        Get street routing data using OSRM API for actual road paths.
        
        Args:
            route_ids (List[int]): List of location IDs in route order
            
        Returns:
            Dict[str, Any]: Street routing data with actual road coordinates
        """
        try:
            import requests
            
            # Get coordinates for the route
            route_coordinates = []
            route_names = []
            
            for loc_id in route_ids:
                location = next(loc for loc in self.locations if loc['id'] == loc_id)
                route_coordinates.append([location['longitude'], location['latitude']])  # OSRM uses lon,lat
                route_names.append(location['name'])
            
            # Build OSRM API URL
            coordinates_str = ';'.join([f"{coord[0]},{coord[1]}" for coord in route_coordinates])
            osrm_url = f"http://router.project-osrm.org/route/v1/driving/{coordinates_str}?overview=full&geometries=geojson"
            
            # Get street routing data
            response = requests.get(osrm_url, timeout=10)
            response.raise_for_status()
            
            route_data = response.json()
            
            if route_data.get('code') == 'Ok' and route_data.get('routes'):
                route = route_data['routes'][0]
                street_coordinates = route['geometry']['coordinates']
                
                # Convert back to lat,lon for frontend
                street_coordinates = [[coord[1], coord[0]] for coord in street_coordinates]
                
                return {
                    'street_coordinates': street_coordinates,
                    'route_names': route_names,
                    'total_distance_km': route['distance'] / 1000,  # Convert meters to km
                    'total_time_hours': route['duration'] / 3600,   # Convert seconds to hours
                    'num_locations': len(route_ids),
                    'routing_success': True
                }
            else:
                # Fallback to straight-line coordinates
                return {
                    'street_coordinates': route_coordinates,
                    'route_names': route_names,
                    'total_distance_km': 0,  # Will be calculated by frontend
                    'total_time_hours': 0,
                    'num_locations': len(route_ids),
                    'routing_success': False,
                    'error': 'OSRM routing failed, using straight-line coordinates'
                }
                
        except Exception as e:
            logger.error(f"Error getting street routing data: {e}")
            # Fallback to straight-line coordinates
            route_coordinates = []
            route_names = []
            
            for loc_id in route_ids:
                location = next(loc for loc in self.locations if loc['id'] == loc_id)
                route_coordinates.append([location['latitude'], location['longitude']])
                route_names.append(location['name'])
            
            return {
                'street_coordinates': route_coordinates,
                'route_names': route_names,
                'total_distance_km': 0,
                'total_time_hours': 0,
                'num_locations': len(route_ids),
                'routing_success': False,
                'error': f'Street routing unavailable: {str(e)}'
            } 