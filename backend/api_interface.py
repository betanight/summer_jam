#!/usr/bin/env python3
"""
API interface for the route optimization system.
"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional
import time
import json

from src.data_loader import DataLoader
from src.distance_calculator import DistanceCalculator
from src.baseline_model import RandomRouteGenerator
from src.optimization_model import GeneticAlgorithmTSP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RouteOptimizationAPI:
    
    def __init__(self, data_file: str = "data/locations.csv"):
        self.data_file = data_file
        self.data_loader = DataLoader(data_file)
        self.distance_calculator = None
        self.baseline_model = None
        self.optimization_model = None
        self.coordinates = None
        self.location_names = []
        self.locations = []
        
        self._initialize_system()
    
    def _initialize_system(self):
        try:
            self.coordinates, self.location_names = self.data_loader.load_data()
            self.data_loader.preprocess_data()
            self.locations = self.data_loader.get_locations()
            
            self.distance_calculator = DistanceCalculator(self.coordinates)
            self.baseline_model = RandomRouteGenerator()
            self.optimization_model = GeneticAlgorithmTSP(len(self.coordinates))
            
            logger.info(f"API initialized with {len(self.coordinates)} locations")
            
        except Exception as e:
            logger.error(f"Error initializing API: {e}")
            raise
    
    def get_all_locations(self) -> List[Dict[str, Any]]:
        return self.locations
    
    def add_custom_location(self, name: str, latitude: float, longitude: float) -> int:
        try:
            new_id = self.data_loader.add_location(name, latitude, longitude)
            
            self.locations = self.data_loader.get_locations()
            self.coordinates = self.data_loader.coordinates
            self.location_names = self.data_loader.location_names
            
            self.distance_calculator = DistanceCalculator(self.coordinates)
            self.baseline_model = RandomRouteGenerator()
            self.optimization_model = GeneticAlgorithmTSP(len(self.coordinates))
            
            logger.info(f"Added custom location: {name} (ID: {new_id})")
            return new_id
            
        except Exception as e:
            logger.error(f"Error adding custom location: {e}")
            raise
    
    def optimize_route(self, location_ids: List[int]) -> Dict[str, Any]:
        try:
            if len(location_ids) < 2:
                raise ValueError("Need at least 2 locations to optimize")
            
            valid_ids = [loc['id'] for loc in self.locations]
            for loc_id in location_ids:
                if loc_id not in valid_ids:
                    raise ValueError(f"Invalid location ID: {loc_id}")
            
            selected_coords = []
            selected_names = []
            for loc_id in location_ids:
                location = next(loc for loc in self.locations if loc['id'] == loc_id)
                selected_coords.append([location['latitude'], location['longitude']])
                selected_names.append(location['name'])
            
            selected_coords = np.array(selected_coords)
            temp_distance_calc = DistanceCalculator(selected_coords)
            
            start_time = time.time()
            optimized_route = self.optimization_model.optimize(temp_distance_calc)
            execution_time = time.time() - start_time
            
            total_distance = temp_distance_calc.calculate_route_distance(optimized_route)
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
        try:
            if len(location_ids) < 2:
                raise ValueError("Need at least 2 locations to compare")
            
            optimized_result = self.optimize_route(location_ids)
            optimized_distance = optimized_result['optimized_route']['total_distance']
            
            selected_coords = []
            for loc_id in location_ids:
                location = next(loc for loc in self.locations if loc['id'] == loc_id)
                selected_coords.append([location['latitude'], location['longitude']])
            
            selected_coords = np.array(selected_coords)
            temp_distance_calc = DistanceCalculator(selected_coords)
            
            random_route = self.baseline_model.generate_random_route(len(selected_coords))
            random_distance = temp_distance_calc.calculate_route_distance(random_route)
            
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
        try:
            route_coordinates = []
            route_names = []
            
            for loc_id in route_ids:
                location = next(loc for loc in self.locations if loc['id'] == loc_id)
                route_coordinates.append([location['latitude'], location['longitude']])
                route_names.append(location['name'])
            
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
        try:
            import requests
            
            route_coordinates = []
            route_names = []
            
            for loc_id in route_ids:
                location = next(loc for loc in self.locations if loc['id'] == loc_id)
                route_coordinates.append([location['longitude'], location['latitude']])
                route_names.append(location['name'])
            
            coordinates_str = ';'.join([f"{coord[0]},{coord[1]}" for coord in route_coordinates])
            osrm_url = f"http://router.project-osrm.org/route/v1/driving/{coordinates_str}?overview=full&geometries=geojson"
            
            response = requests.get(osrm_url, timeout=10)
            response.raise_for_status()
            
            route_data = response.json()
            
            if route_data.get('code') == 'Ok' and route_data.get('routes'):
                route = route_data['routes'][0]
                street_coordinates = route['geometry']['coordinates']
                street_coordinates = [[coord[1], coord[0]] for coord in street_coordinates]
                
                return {
                    'street_coordinates': street_coordinates,
                    'route_names': route_names,
                    'total_distance_km': route['distance'] / 1000,
                    'total_time_hours': route['duration'] / 3600,
                    'num_locations': len(route_ids),
                    'routing_success': True
                }
            else:
                return {
                    'street_coordinates': route_coordinates,
                    'route_names': route_names,
                    'total_distance_km': 0,
                    'total_time_hours': 0,
                    'num_locations': len(route_ids),
                    'routing_success': False,
                    'error': 'OSRM routing failed, using straight-line coordinates'
                }
                
        except Exception as e:
            logger.error(f"Error getting street routing data: {e}")
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