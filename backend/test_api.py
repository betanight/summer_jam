#!/usr/bin/env python3
"""
Test script for the Route Optimization API.
Run this to verify all endpoints are working correctly.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['message']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_get_locations():
    """Test getting all locations"""
    print("\n🔍 Testing get locations...")
    try:
        response = requests.get(f"{BASE_URL}/locations")
        if response.status_code == 200:
            data = response.json()
            locations = data['data']['locations']
            print(f"✅ Retrieved {len(locations)} locations")
            for loc in locations[:3]:  # Show first 3
                print(f"   - {loc['name']}")
            return locations
        else:
            print(f"❌ Get locations failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Get locations error: {e}")
        return None

def test_optimize_route(location_ids):
    """Test route optimization"""
    print(f"\n🔍 Testing route optimization for locations {location_ids}...")
    try:
        response = requests.post(f"{BASE_URL}/optimize", json={
            "location_ids": location_ids
        })
        if response.status_code == 200:
            data = response.json()
            route = data['data']['optimized_route']
            print(f"✅ Route optimized successfully")
            print(f"   - Total distance: {route['total_distance']:.1f} km")
            print(f"   - Execution time: {route['execution_time']:.3f} seconds")
            print(f"   - Route: {' → '.join(route['location_names'])}")
            return route
        else:
            print(f"❌ Route optimization failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Route optimization error: {e}")
        return None

def test_compare_routes(location_ids):
    """Test route comparison"""
    print(f"\n🔍 Testing route comparison for locations {location_ids}...")
    try:
        response = requests.post(f"{BASE_URL}/compare", json={
            "location_ids": location_ids
        })
        if response.status_code == 200:
            data = response.json()
            comparison = data['data']
            print(f"✅ Route comparison completed")
            print(f"   - Random route: {comparison['random_route']['distance']:.1f} km")
            print(f"   - Optimized route: {comparison['optimized_route']['distance']:.1f} km")
            print(f"   - Improvement: {comparison['improvement_percentage']:.1f}%")
            print(f"   - Distance saved: {comparison['distance_saved']:.1f} km")
            return comparison
        else:
            print(f"❌ Route comparison failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Route comparison error: {e}")
        return None

def test_visualization(location_ids):
    """Test visualization data"""
    print(f"\n🔍 Testing visualization data for locations {location_ids}...")
    try:
        response = requests.post(f"{BASE_URL}/visualization", json={
            "route_ids": location_ids
        })
        if response.status_code == 200:
            data = response.json()
            viz_data = data['data']
            print(f"✅ Visualization data retrieved")
            print(f"   - Coordinates: {len(viz_data['route_coordinates'])} points")
            print(f"   - Total distance: {viz_data['total_distance']:.1f} km")
            print(f"   - Locations: {viz_data['num_locations']}")
            return viz_data
        else:
            print(f"❌ Visualization failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Visualization error: {e}")
        return None

def test_street_routing(location_ids):
    """Test street routing data"""
    print(f"\n🔍 Testing street routing for locations {location_ids}...")
    try:
        response = requests.post(f"{BASE_URL}/street-routing", json={
            "route_ids": location_ids
        })
        if response.status_code == 200:
            data = response.json()
            routing_data = data['data']
            print(f"✅ Street routing data retrieved")
            print(f"   - Routing success: {routing_data['routing_success']}")
            if routing_data['routing_success']:
                print(f"   - Street distance: {routing_data['total_distance_km']:.1f} km")
                print(f"   - Travel time: {routing_data['total_time_hours']:.1f} hours")
            else:
                print(f"   - Error: {routing_data.get('error', 'Unknown error')}")
            return routing_data
        else:
            print(f"❌ Street routing failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Street routing error: {e}")
        return None

def test_quick_optimize(location_ids):
    """Test quick optimization endpoint"""
    print(f"\n🔍 Testing quick optimization for locations {location_ids}...")
    try:
        location_str = ",".join(map(str, location_ids))
        response = requests.get(f"{BASE_URL}/quick-optimize?location_ids={location_str}")
        if response.status_code == 200:
            data = response.json()
            route = data['data']['optimized_route']
            print(f"✅ Quick optimization successful")
            print(f"   - Total distance: {route['total_distance']:.1f} km")
            print(f"   - Route: {' → '.join(route['location_names'])}")
            return route
        else:
            print(f"❌ Quick optimization failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Quick optimization error: {e}")
        return None

def test_add_location():
    """Test adding a custom location"""
    print(f"\n🔍 Testing add custom location...")
    try:
        location_data = {
            "name": "Test Location",
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        response = requests.post(f"{BASE_URL}/locations", json=location_data)
        if response.status_code == 200:
            data = response.json()
            location_id = data['data']['location_id']
            print(f"✅ Custom location added successfully")
            print(f"   - Location ID: {location_id}")
            print(f"   - Name: {location_data['name']}")
            return location_id
        else:
            print(f"❌ Add location failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Add location error: {e}")
        return None

def test_get_stats():
    """Test getting API statistics"""
    print(f"\n🔍 Testing API statistics...")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            data = response.json()
            stats = data['data']
            print(f"✅ API statistics retrieved")
            print(f"   - Total locations: {stats['total_locations']}")
            print(f"   - Algorithm: {stats['algorithm']}")
            print(f"   - Distance formula: {stats['distance_formula']}")
            print(f"   - Sample locations: {', '.join(stats['sample_locations'][:3])}")
            return stats
        else:
            print(f"❌ Get stats failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Get stats error: {e}")
        return None

def main():
    """Run all tests"""
    print("🧪 Route Optimization API Test Suite")
    print("=" * 50)
    
    # Check if API is running
    if not test_health():
        print("\n❌ API is not running. Please start the API server first:")
        print("   cd backend")
        print("   python start_api.py")
        return
    
    # Test all endpoints
    locations = test_get_locations()
    if not locations:
        return
    
    # Use first 5 locations for testing
    test_location_ids = [loc['id'] for loc in locations[:5]]
    
    test_optimize_route(test_location_ids)
    test_compare_routes(test_location_ids)
    test_visualization(test_location_ids)
    test_street_routing(test_location_ids)
    test_quick_optimize(test_location_ids)
    test_add_location()
    test_get_stats()
    
    print("\n🎉 All tests completed!")
    print("\n📖 For more information:")
    print("   - Interactive docs: http://localhost:8000/docs")
    print("   - API documentation: backend/API_DOCUMENTATION.md")

if __name__ == "__main__":
    main() 