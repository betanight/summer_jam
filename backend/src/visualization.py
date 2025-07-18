"""
Visualization utilities for route optimization results.
Simplified for web deployment without heavy dependencies.
"""

import numpy as np
from typing import List, Dict, Tuple
import logging
import requests
import json
import time

logger = logging.getLogger(__name__)

class RouteVisualizer:
    """
    Simplified visualization class for route optimization results.
    """
    
    def __init__(self):
        """Initialize the visualizer."""
        self.colors = {
            'baseline': '#FF6B6B',
            'optimized': '#4ECDC4',
            'locations': '#45B7D1',
            'route_line': '#2C3E50'
        }
        # OpenRouteService API key (free tier available)
        self.routing_api_key = None  # Will be set if available
        self.routing_base_url = "https://api.openrouteservice.org/v2/directions/driving-car"
    
    def get_road_route(self, start_coords: Tuple[float, float], 
                       end_coords: Tuple[float, float]) -> List[Tuple[float, float]]:
        """
        Get actual road route between two points using OpenRouteService API.
        
        Args:
            start_coords (Tuple[float, float]): Start coordinates (lat, lon)
            end_coords (Tuple[float, float]): End coordinates (lat, lon)
            
        Returns:
            List[Tuple[float, float]]: List of coordinates along the road route
        """
        try:
            # For now, return straight line if no API key
            # In production, you would use a real routing service
            return [start_coords, end_coords]
            
            # Uncomment below when you have an API key
            # headers = {
            #     'Authorization': f'Bearer {self.routing_api_key}',
            #     'Content-Type': 'application/json'
            # }
            # 
            # payload = {
            #     "coordinates": [
            #         [start_coords[1], start_coords[0]],  # [lon, lat]
            #         [end_coords[1], end_coords[0]]       # [lon, lat]
            #     ],
            #     "format": "geojson"
            # }
            # 
            # response = requests.post(self.routing_base_url, 
            #                          headers=headers, 
            #                          json=payload)
            # 
            # if response.status_code == 200:
            #     data = response.json()
            #     coordinates = data['features'][0]['geometry']['coordinates']
            #     # Convert [lon, lat] to [lat, lon]
            #     return [(coord[1], coord[0]) for coord in coordinates]
            # else:
            #     logger.warning(f"Routing API failed: {response.status_code}")
            #     return [start_coords, end_coords]
                
        except Exception as e:
            logger.warning(f"Error getting road route: {e}")
            return [start_coords, end_coords]
    
    def get_route_path(self, route_indices: List[int], coordinates: np.ndarray) -> List[Tuple[float, float]]:
        """
        Get the complete road path for a route.
        
        Args:
            route_indices (List[int]): Route location indices
            coordinates (np.ndarray): All location coordinates
            
        Returns:
            List[Tuple[float, float]]: Complete road path coordinates
        """
        path = []
        
        for i in range(len(route_indices) - 1):
            start_idx = route_indices[i]
            end_idx = route_indices[i + 1]
            
            start_coords = (coordinates[start_idx, 0], coordinates[start_idx, 1])
            end_coords = (coordinates[end_idx, 0], coordinates[end_idx, 1])
            
            # Get road route between these points
            segment_path = self.get_road_route(start_coords, end_coords)
            path.extend(segment_path)
            
            # Add small delay to avoid API rate limits
            time.sleep(0.1)
        
        return path
    
    def create_route_summary(self, coordinates: np.ndarray, location_names: List[str],
                           baseline_route: List[int], optimized_route: List[int],
                           baseline_distance: float, optimized_distance: float) -> Dict:
        """
        Create a summary of route comparison (for web API).
        
        Args:
            coordinates (np.ndarray): Location coordinates
            location_names (List[str]): Names of locations
            baseline_route (List[int]): Baseline route indices
            optimized_route (List[int]): Optimized route indices
            baseline_distance (float): Baseline route distance
            optimized_distance (float): Optimized route distance
            
        Returns:
            Dict: Route comparison summary
        """
        # Get road paths for routes
        baseline_path = self.get_route_path(baseline_route, coordinates)
        optimized_path = self.get_route_path(optimized_route, coordinates)
        
        # Convert paths to separate lat/lon arrays
        baseline_lats = [coord[0] for coord in baseline_path]
        baseline_lons = [coord[1] for coord in baseline_path]
        optimized_lats = [coord[0] for coord in optimized_path]
        optimized_lons = [coord[1] for coord in optimized_path]
        
        summary = {
            'baseline_route': {
                'location_names': [location_names[i] for i in baseline_route],
                'coordinates': {
                    'latitudes': baseline_lats,
                    'longitudes': baseline_lons
                },
                'distance': baseline_distance
            },
            'optimized_route': {
                'location_names': [location_names[i] for i in optimized_route],
                'coordinates': {
                    'latitudes': optimized_lats,
                    'longitudes': optimized_lons
                },
                'distance': optimized_distance
            },
            'improvement': {
                'distance_saved': baseline_distance - optimized_distance,
                'improvement_percentage': ((baseline_distance - optimized_distance) / baseline_distance) * 100
            }
        }
        
        return summary 