"""
Distance calculation utilities for route optimization.
Uses Haversine formula for accurate geographic distance calculations.
"""

import numpy as np
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on Earth.
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
        
    Returns:
        float: Distance in kilometers
    """
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Earth's radius in kilometers
    r = 6371
    
    return c * r

class DistanceCalculator:
    """
    Distance calculator class for route optimization.
    """
    
    def __init__(self, coordinates: np.ndarray):
        """
        Initialize with coordinates.
        
        Args:
            coordinates (np.ndarray): Array of coordinates [lat, lon]
        """
        self.coordinates = coordinates
        self.distance_matrix = self._calculate_distance_matrix()
    
    def _calculate_distance_matrix(self) -> np.ndarray:
        """
        Calculate distance matrix between all pairs of locations.
        
        Returns:
            np.ndarray: Distance matrix where [i][j] is distance from i to j
        """
        n = len(self.coordinates)
        distance_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    distance_matrix[i][j] = haversine_distance(
                        self.coordinates[i][0], self.coordinates[i][1],
                        self.coordinates[j][0], self.coordinates[j][1]
                    )
        
        logger.info(f"Distance matrix calculated for {n} locations")
        return distance_matrix
    
    def calculate_route_distance(self, route: List[int]) -> float:
        """
        Calculate total distance for a given route.
        
        Args:
            route (List[int]): List of location indices representing the route
            
        Returns:
            float: Total route distance in kilometers
        """
        total_distance = 0
        
        for i in range(len(route) - 1):
            current = route[i]
            next_city = route[i + 1]
            total_distance += self.distance_matrix[current][next_city]
        
        return total_distance
    
    def get_distance_matrix(self) -> np.ndarray:
        """
        Get the pre-calculated distance matrix.
        
        Returns:
            np.ndarray: Distance matrix
        """
        return self.distance_matrix

def calculate_distance_matrix(coordinates: np.ndarray) -> np.ndarray:
    """
    Calculate distance matrix between all pairs of locations.
    
    Args:
        coordinates (np.ndarray): Array of coordinates [lat, lon]
        
    Returns:
        np.ndarray: Distance matrix where [i][j] is distance from i to j
    """
    n = len(coordinates)
    distance_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                distance_matrix[i][j] = haversine_distance(
                    coordinates[i][0], coordinates[i][1],
                    coordinates[j][0], coordinates[j][1]
                )
    
    logger.info(f"Distance matrix calculated for {n} locations")
    return distance_matrix

def calculate_route_distance(route: List[int], distance_matrix: np.ndarray) -> float:
    """
    Calculate total distance for a given route.
    
    Args:
        route (List[int]): List of location indices representing the route
        distance_matrix (np.ndarray): Pre-calculated distance matrix
        
    Returns:
        float: Total route distance in kilometers
    """
    total_distance = 0
    
    for i in range(len(route) - 1):
        current = route[i]
        next_city = route[i + 1]
        total_distance += distance_matrix[current][next_city]
    
    # Add distance from last city back to first (optional, for closed loop)
    # total_distance += distance_matrix[route[-1]][route[0]]
    
    return total_distance

def get_route_coordinates(route: List[int], coordinates: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extract coordinates for a route in order.
    
    Args:
        route (List[int]): List of location indices
        coordinates (np.ndarray): Array of all coordinates
        
    Returns:
        Tuple[np.ndarray, np.ndarray]: Arrays of latitudes and longitudes for the route
    """
    route_coords = coordinates[route]
    lats = route_coords[:, 0]
    lons = route_coords[:, 1]
    
    return lats, lons

def calculate_route_statistics(route: List[int], distance_matrix: np.ndarray) -> dict:
    """
    Calculate comprehensive statistics for a route.
    
    Args:
        route (List[int]): List of location indices
        distance_matrix (np.ndarray): Distance matrix
        
    Returns:
        dict: Dictionary containing route statistics
    """
    total_distance = calculate_route_distance(route, distance_matrix)
    
    # Calculate segment distances
    segment_distances = []
    for i in range(len(route) - 1):
        segment_distances.append(distance_matrix[route[i]][route[i + 1]])
    
    stats = {
        'total_distance': total_distance,
        'num_locations': len(route),
        'avg_segment_distance': np.mean(segment_distances),
        'max_segment_distance': np.max(segment_distances),
        'min_segment_distance': np.min(segment_distances),
        'segment_distances': segment_distances
    }
    
    return stats 