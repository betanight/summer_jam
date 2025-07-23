#!/usr/bin/env python3

import logging
import numpy as np
from typing import List, Dict, Any, Optional
import time
import json
import pandas as pd
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RouteOptimizationAPI:
    
    def __init__(self, data_file: str = "analysis/california_attractions_data.csv"):
        self.data_file = data_file
        self.attractions = []
        self.coordinates = None
        self.attraction_names = []
        
        self._initialize_system()
    
    def _initialize_system(self):
        try:
            self.attractions = self._load_california_attractions()
            self.attraction_names = [attraction['name'] for attraction in self.attractions]
            self.coordinates = np.array([[attraction['latitude'], attraction['longitude']] for attraction in self.attractions])
            
            logger.info(f"API initialized with {len(self.attractions)} attractions")
            
        except Exception as e:
            logger.error(f"Error initializing API: {e}")
            raise
    
    def get_all_locations(self) -> List[Dict[str, Any]]:
        return self.attractions
    
    def add_custom_location(self, name: str, latitude: float, longitude: float) -> int:
        try:
            new_id = len(self.attractions)
            new_attraction = {
                'id': new_id,
                'name': name,
                'city': 'Custom Location',
                'state': 'CA',
                'category': 'Custom',
                'latitude': latitude,
                'longitude': longitude,
                'image_link': 'https://via.placeholder.com/300x200?text=Custom'
            }
            
            self.attractions.append(new_attraction)
            self.attraction_names.append(name)
            self.coordinates = np.array([[attraction['latitude'], attraction['longitude']] for attraction in self.attractions])
            
            logger.info(f"Added custom location: {name} (ID: {new_id})")
            return new_id
            
        except Exception as e:
            logger.error(f"Error adding custom location: {e}")
            raise
    
    def optimize_route(self, location_ids: List[int]) -> Dict[str, Any]:
        try:
            if len(location_ids) < 2:
                raise ValueError("Need at least 2 locations to optimize")
            
            valid_ids = [attraction['id'] for attraction in self.attractions]
            for loc_id in location_ids:
                if loc_id not in valid_ids:
                    raise ValueError(f"Invalid location ID: {loc_id}")
            
            selected_coords = []
            selected_names = []
            for loc_id in location_ids:
                attraction = next(attraction for attraction in self.attractions if attraction['id'] == loc_id)
                selected_coords.append([attraction['latitude'], attraction['longitude']])
                selected_names.append(attraction['name'])
            
            selected_coords = np.array(selected_coords)
            
            optimized_route = self._simple_optimize_route(selected_coords)
            
            total_distance = self._calculate_route_distance(selected_coords, optimized_route)
            optimized_names = [selected_names[i] for i in optimized_route]
            optimized_ids = [location_ids[i] for i in optimized_route]
            
            result = {
                'optimized_route': {
                    'location_ids': optimized_ids,
                    'location_names': optimized_names,
                    'total_distance': total_distance,
                    'execution_time': 0.1
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error optimizing route: {e}")
            raise
    
    def _simple_optimize_route(self, coordinates: np.ndarray) -> List[int]:
        n = len(coordinates)
        if n <= 1:
            return list(range(n))
        
        route = [0]
        unvisited = set(range(1, n))
        
        while unvisited:
            current = route[-1]
            nearest = min(unvisited, key=lambda x: np.linalg.norm(coordinates[current] - coordinates[x]))
            route.append(nearest)
            unvisited.remove(nearest)
        
        return route
    
    def _calculate_route_distance(self, coordinates: np.ndarray, route: List[int]) -> float:
        total_distance = 0.0
        for i in range(len(route) - 1):
            point1 = coordinates[route[i]]
            point2 = coordinates[route[i + 1]]
            distance = np.linalg.norm(point1 - point2)
            total_distance += distance
        return total_distance
    
    def compare_with_random(self, location_ids: List[int]) -> Dict[str, Any]:
        try:
            if len(location_ids) < 2:
                raise ValueError("Need at least 2 locations to compare")
            
            optimized_result = self.optimize_route(location_ids)
            optimized_distance = optimized_result['optimized_route']['total_distance']
            
            selected_coords = []
            for loc_id in location_ids:
                attraction = next(attraction for attraction in self.attractions if attraction['id'] == loc_id)
                selected_coords.append([attraction['latitude'], attraction['longitude']])
            
            selected_coords = np.array(selected_coords)
            
            import random
            random_route = list(range(len(selected_coords)))
            random.shuffle(random_route)
            random_distance = self._calculate_route_distance(selected_coords, random_route)
            
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
                attraction = next(attraction for attraction in self.attractions if attraction['id'] == loc_id)
                route_coordinates.append([attraction['latitude'], attraction['longitude']])
                route_names.append(attraction['name'])
            
            coords_array = np.array(route_coordinates)
            total_distance = self._calculate_route_distance(coords_array, list(range(len(route_coordinates))))
            
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
            route_coordinates = []
            route_names = []
            
            for loc_id in route_ids:
                attraction = next(attraction for attraction in self.attractions if attraction['id'] == loc_id)
                route_coordinates.append([attraction['latitude'], attraction['longitude']])
                route_names.append(attraction['name'])
            
            coords_array = np.array(route_coordinates)
            total_distance = self._calculate_route_distance(coords_array, list(range(len(route_coordinates))))
            
            routing_data = {
                'route_coordinates': route_coordinates,
                'route_names': route_names,
                'total_distance': total_distance,
                'num_locations': len(route_ids)
            }
            
            return routing_data
            
        except Exception as e:
            logger.error(f"Error getting street routing data: {e}")
            raise

    def get_street_directions(self, optimized_route: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            if len(optimized_route) < 2:
                return {"error": "Need at least 2 locations for directions"}
            
            coordinates = []
            for location in optimized_route:
                if 'location' in location and 'lat' in location['location'] and 'lng' in location['location']:
                    coordinates.append({
                        'lat': location['location']['lat'],
                        'lng': location['location']['lng'],
                        'name': location.get('key', 'Unknown')
                    })
            
            if len(coordinates) < 2:
                return {"error": "Invalid coordinates in route"}
            
            waypoints = []
            if len(coordinates) > 2:
                waypoints = coordinates[1:-1]
            
            directions_data = {
                'origin': coordinates[0],
                'destination': coordinates[-1],
                'waypoints': waypoints,
                'total_locations': len(coordinates),
                'route_coordinates': coordinates
            }
            
            return directions_data
            
        except Exception as e:
            logger.error(f"Error getting street directions: {e}")
            raise

    def get_attractions_along_route(self, from_city: str, to_city: str, max_attractions: int = 9, max_distance_miles: float = 25.0) -> List[Dict[str, Any]]:
        try:
            from geopy.geocoders import Nominatim
            from geopy.distance import geodesic
            
            geolocator = Nominatim(user_agent="route_optimizer")
            
            start_location = geolocator.geocode(f"{from_city}, CA, USA")
            end_location = geolocator.geocode(f"{to_city}, CA, USA")
            
            if not start_location or not end_location:
                raise ValueError(f"Could not find coordinates for {from_city} or {to_city}")
            
            start_coords = (start_location.latitude, start_location.longitude)
            end_coords = (end_location.latitude, end_location.longitude)
            
            logger.info(f"Route from {from_city} ({start_coords}) to {to_city} ({end_coords})")
            
            route_points = self._get_route_points(start_coords, end_coords)
            
            nearby_attractions = self._find_attractions_near_route(
                self.attractions, route_points, max_distance_miles, max_attractions
            )
            
            logger.info(f"Found {len(nearby_attractions)} attractions near route")
            
            formatted_attractions = []
            for i, attraction in enumerate(nearby_attractions):
                formatted_attraction = {
                    'key': f"attraction_{i}",
                    'name': attraction['name'],
                    'town': attraction['city'],
                    'rating': 4.5,
                    'image': attraction.get('image_link', 'https://via.placeholder.com/300x200?text=Attraction'),
                    'location': {
                        'lat': attraction['latitude'],
                        'lng': attraction['longitude']
                    },
                    'category': attraction['category'],
                    'distance_from_route': attraction.get('distance_from_route', 0)
                }
                formatted_attractions.append(formatted_attraction)
            
            logger.info(f"Formatted {len(formatted_attractions)} attractions for frontend")
            return formatted_attractions
            
        except Exception as e:
            logger.error(f"Error getting attractions along route: {e}")
            raise

    def get_route_points_coordinates(self, from_city: str, to_city: str) -> Dict[str, Any]:
        try:
            from geopy.geocoders import Nominatim
            
            geolocator = Nominatim(user_agent="route_optimizer")
            
            start_location = geolocator.geocode(f"{from_city}, CA, USA")
            if not start_location:
                start_location = geolocator.geocode(f"{from_city}, USA")
            
            end_location = geolocator.geocode(f"{to_city}, CA, USA")
            if not end_location:
                end_location = geolocator.geocode(f"{to_city}, USA")
            
            if not start_location or not end_location:
                raise ValueError(f"Could not find coordinates for {from_city} or {to_city}")
            
            route_points = {
                'start': {
                    'city': from_city,
                    'lat': start_location.latitude,
                    'lng': start_location.longitude,
                    'color': 'blue'
                },
                'end': {
                    'city': to_city,
                    'lat': end_location.latitude,
                    'lng': end_location.longitude,
                    'color': 'green'
                }
            }
            
            return route_points
            
        except Exception as e:
            logger.error(f"Error getting route points coordinates: {e}")
            raise

    def _get_route_points(self, start_coords: tuple, end_coords: tuple) -> List[tuple]:
        try:
            import numpy as np
            
            num_points = 50
            lat_points = np.linspace(start_coords[0], end_coords[0], num_points)
            lng_points = np.linspace(start_coords[1], end_coords[1], num_points)
            
            route_points = list(zip(lat_points, lng_points))
            return route_points
            
        except Exception as e:
            logger.error(f"Error getting route points: {e}")
            return [start_coords, end_coords]

    def _load_california_attractions(self) -> List[Dict[str, Any]]:
        try:
            if not os.path.exists(self.data_file):
                raise FileNotFoundError(f"Attractions file not found: {self.data_file}")
            
            df = pd.read_csv(self.data_file)
            attractions = []
            
            for i, (_, row) in enumerate(df.iterrows()):
                attraction = {
                    'id': i,
                    'name': row['name'],
                    'city': row['city'],
                    'state': row['state'],
                    'category': row['category'],
                    'latitude': float(row['latitude']),
                    'longitude': float(row['longitude']),
                    'image_link': row['image_link']
                }
                attractions.append(attraction)
            
            return attractions
            
        except Exception as e:
            logger.error(f"Error loading attractions: {e}")
            raise

    def _find_attractions_near_route(self, attractions: List[Dict], route_points: List[tuple], max_distance_miles: float, max_attractions: int) -> List[Dict]:
        try:
            from geopy.distance import geodesic
            
            logger.info(f"Searching {len(attractions)} attractions near {len(route_points)} route points")
            logger.info(f"Max distance: {max_distance_miles} miles, max attractions: {max_attractions}")
            
            nearby_attractions = []
            
            for attraction in attractions:
                attraction_coords = (attraction['latitude'], attraction['longitude'])
                min_distance = float('inf')
                
                for route_point in route_points:
                    distance = geodesic(attraction_coords, route_point).miles
                    if distance < min_distance:
                        min_distance = distance
                
                max_allowed_distance = max_distance_miles
                
                if min_distance <= max_allowed_distance:
                    attraction['distance_from_route'] = min_distance
                    nearby_attractions.append(attraction)
            
            logger.info(f"Found {len(nearby_attractions)} attractions within {max_distance_miles} miles")
            
            nearby_attractions.sort(key=lambda x: x['distance_from_route'])
            
            unique_attractions = []
            seen_names = set()
            seen_coordinates = set()
            
            for attraction in nearby_attractions:
                name = attraction['name'].lower()
                coords = (attraction['latitude'], attraction['longitude'])
                
                is_duplicate_name = any(
                    name in seen_name or seen_name in name 
                    for seen_name in seen_names
                )
                is_duplicate_coords = coords in seen_coordinates
                
                if not is_duplicate_name and not is_duplicate_coords:
                    unique_attractions.append(attraction)
                    seen_names.add(name)
                    seen_coordinates.add(coords)
                
                if len(unique_attractions) >= max_attractions:
                    break
            
            logger.info(f"Returning {len(unique_attractions)} unique attractions")
            return unique_attractions[:max_attractions]
            
        except Exception as e:
            logger.error(f"Error finding attractions near route: {e}")
            raise 