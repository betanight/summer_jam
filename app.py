#!/usr/bin/env python3
"""
Interactive Route Optimization Dashboard
Flask web app with map interface for testing the optimization system
"""

from flask import Flask, render_template, request, jsonify
from api_interface import RouteOptimizationAPI
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the optimization API
api = RouteOptimizationAPI()

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('dashboard.html')

@app.route('/api/locations')
def get_locations():
    """Get all available locations."""
    try:
        locations = api.get_all_locations()
        return jsonify({
            'success': True,
            'locations': locations
        })
    except Exception as e:
        logger.error(f"Error getting locations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/add-location', methods=['POST'])
def add_location():
    """Add a custom location."""
    try:
        data = request.get_json()
        name = data.get('name')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not all([name, latitude, longitude]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        location_id = api.add_custom_location(name, latitude, longitude)
        
        return jsonify({
            'success': True,
            'location_id': location_id,
            'message': f'Added {name} successfully'
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error adding location: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/optimize-route', methods=['POST'])
def optimize_route():
    """Optimize a route for selected locations."""
    try:
        data = request.get_json()
        location_ids = data.get('location_ids', [])
        
        if len(location_ids) < 2:
            return jsonify({'error': 'Need at least 2 locations'}), 400
        
        result = api.optimize_route(location_ids)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error optimizing route: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare-routes', methods=['POST'])
def compare_routes():
    """Compare optimized route with random route."""
    try:
        data = request.get_json()
        location_ids = data.get('location_ids', [])
        
        if len(location_ids) < 2:
            return jsonify({'error': 'Need at least 2 locations'}), 400
        
        comparison = api.compare_with_random(location_ids)
        
        return jsonify({
            'success': True,
            'comparison': comparison
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Error comparing routes: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/route-visualization', methods=['POST'])
def get_route_visualization():
    """Get visualization data for a route."""
    try:
        data = request.get_json()
        route_ids = data.get('route_ids', [])
        
        if not route_ids:
            return jsonify({'error': 'No route provided'}), 400
        
        viz_data = api.get_route_visualization_data(route_ids)
        
        return jsonify({
            'success': True,
            'visualization': viz_data
        })
    except Exception as e:
        logger.error(f"Error getting visualization data: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Interactive Route Optimization Dashboard")
    print("📍 Open http://localhost:5001 in your browser")
    print("🗺️  Click on the map to add locations")
    print("🎯 Click 'Optimize Route' to see the best path")
    app.run(debug=True, host='0.0.0.0', port=5001) 