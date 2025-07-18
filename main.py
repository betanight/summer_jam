#!/usr/bin/env python3
"""
Main entry point for the Summer Activity Route Optimizer API.
Provides core optimization functionality without web interface.
"""

from api_interface import RouteOptimizationAPI
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating the API usage."""
    try:
        # Initialize the API
        api = RouteOptimizationAPI()
        
        # Get all locations
        locations = api.get_all_locations()
        print(f"✅ Loaded {len(locations)} locations:")
        for loc in locations:
            print(f"  - {loc['name']} ({loc['latitude']}, {loc['longitude']})")
        
        # Example: Optimize route for first 5 locations
        location_ids = [0, 1, 2, 3, 4]
        print(f"\n🎯 Optimizing route for locations: {location_ids}")
        
        result = api.optimize_route(location_ids)
        optimized_route = result['optimized_route']
        
        print(f"✅ Optimized route:")
        for i, name in enumerate(optimized_route['location_names']):
            print(f"  {i+1}. {name}")
        print(f"📏 Total distance: {optimized_route['total_distance']:.1f} km")
        print(f"⏱️  Optimization time: {optimized_route['execution_time']:.3f} seconds")
        
        # Compare with random route
        comparison = api.compare_with_random(location_ids)
        improvement = comparison['improvement_percentage']
        distance_saved = comparison['distance_saved']
        
        print(f"\n📊 Performance comparison:")
        print(f"  - Random route: {comparison['random_route']['distance']:.1f} km")
        print(f"  - Optimized route: {comparison['optimized_route']['distance']:.1f} km")
        print(f"  - Distance saved: {distance_saved:.1f} km")
        print(f"  - Improvement: {improvement:.1f}%")
        
        print(f"\n🚀 API is ready for integration!")
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    main() 