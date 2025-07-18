# Software Engineering Integration Guide

## 🚀 Quick Integration for React Team

This guide shows how to integrate the route optimization API into your React application.

## 🏗️ Architecture Overview

**Python Backend + React Frontend**
- **Backend**: Python Flask/FastAPI with our optimization API
- **Frontend**: React with mapping library (Leaflet/Google Maps/Mapbox)
- **Communication**: REST API calls between React and Python
- **Optimization**: Python handles the genetic algorithm TSP solving
- **Visualization**: React handles the interactive map display

## 📋 Available API Methods

### 1. Get All Locations
```javascript
// Get all available locations (9 European landmarks)
const locations = await fetch('/api/locations').then(r => r.json());
// Returns: [{id: 0, name: "Sagrada Familia", latitude: 41.4036, longitude: 2.1744}, ...]
```

### 2. Optimize Route (Python Backend)
```javascript
// Optimize route for selected location IDs
const optimizeRoute = async (locationIds) => {
  const response = await fetch('/api/optimize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location_ids: locationIds })
  });
  return response.json();
};

// Usage
const result = await optimizeRoute([0, 1, 2, 3, 4]);
// Returns: {
//   optimized_route: {
//     location_ids: [2, 0, 3, 1, 4],
//     location_names: ["Colosseum", "Sagrada Familia", "Eiffel Tower", "Anne Frank House", "Oia"],
//     total_distance: 3381.2,
//     execution_time: 0.003
//   }
// }
```

### 3. Get Street Routing Data (Actual Roads)
```javascript
// Get actual street routing for visualization
const getStreetRouting = async (routeIds) => {
  const response = await fetch('/api/street-routing', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ route_ids: routeIds })
  });
  return response.json();
};

// Usage
const streetData = await getStreetRouting([2, 0, 3, 1, 4]);
// Returns: {
//   street_coordinates: [[lat1, lon1], [lat2, lon2], ...], // Actual road path
//   route_names: ["Colosseum", "Sagrada Familia", ...],
//   total_distance_km: 3456.7, // Real driving distance
//   total_time_hours: 42.3,    // Estimated driving time
//   routing_success: true
// }
```

### 4. Compare with Random Route
```javascript
// Compare optimized vs random route
const compareRoutes = async (locationIds) => {
  const response = await fetch('/api/compare', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ location_ids: locationIds })
  });
  return response.json();
};

// Usage
const comparison = await compareRoutes([0, 1, 2, 3, 4]);
// Returns: {
//   random_route: { distance: 6588.8, route: [3, 1, 4, 0, 2] },
//   optimized_route: { distance: 3381.2, route: [2, 0, 3, 1, 4] },
//   improvement_percentage: 48.7,
//   distance_saved: 3207.5
// }
```

### 5. Add Custom Location
```javascript
// Add a new location
const addLocation = async (name, latitude, longitude) => {
  const response = await fetch('/api/locations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, latitude, longitude })
  });
  return response.json();
};

// Usage
const newLocation = await addLocation("My Hotel", 40.7128, -74.0060);
// Returns: { id: 9, name: "My Hotel", latitude: 40.7128, longitude: -74.0060 }
```

## 🛣️ Route Types Explained

### 1. Optimization Route (Straight-line distances)
- **Purpose**: Fast TSP optimization using genetic algorithms
- **Distance**: Haversine formula (direct point-to-point)
- **Use**: Finding the optimal order of locations
- **Speed**: ~0.005 seconds for 9 locations

### 2. Street Routing (Actual roads)
- **Purpose**: Real driving paths for visualization
- **Distance**: Actual road network distances
- **Use**: Displaying realistic routes on maps
- **API**: OSRM (Open Source Routing Machine)

## 🗺️ Map Integration Examples

### Leaflet.js Integration with Street Routing
```javascript
import L from 'leaflet';

// Initialize map
const map = L.map('map').setView([48.8584, 2.2945], 4);

// Add markers for all locations
locations.forEach(location => {
  L.marker([location.latitude, location.longitude])
    .bindPopup(location.name)
    .addTo(map);
});

// Draw optimized route with street routing
const drawOptimizedRoute = async (routeIds) => {
  // Get optimized order from Python backend
  const optimizationResult = await optimizeRoute(routeIds);
  const optimizedOrder = optimizationResult.optimized_route.location_ids;
  
  // Get street routing data
  const streetData = await getStreetRouting(optimizedOrder);
  
  if (streetData.routing_success) {
    // Draw actual road path
    L.polyline(streetData.street_coordinates, {
      color: 'red', 
      weight: 3,
      opacity: 0.8
    }).addTo(map);
    
    console.log(`Real driving distance: ${streetData.total_distance_km.toFixed(1)} km`);
    console.log(`Estimated driving time: ${streetData.total_time_hours.toFixed(1)} hours`);
  } else {
    // Fallback to straight-line path
    const coordinates = optimizedOrder.map(id => {
      const location = locations.find(loc => loc.id === id);
      return [location.latitude, location.longitude];
    });
    
    L.polyline(coordinates, {color: 'blue', weight: 2, dashArray: '5, 5'})
      .addTo(map);
  }
};
```

### Google Maps Integration
```javascript
// Initialize map
const map = new google.maps.Map(document.getElementById('map'), {
  center: { lat: 48.8584, lng: 2.2945 },
  zoom: 4
});

// Draw optimized route with street routing
const drawOptimizedRoute = async (routeIds) => {
  // Get optimized order
  const optimizationResult = await optimizeRoute(routeIds);
  const optimizedOrder = optimizationResult.optimized_route.location_ids;
  
  // Get street routing data
  const streetData = await getStreetRouting(optimizedOrder);
  
  if (streetData.routing_success) {
    // Draw actual road path
    const path = streetData.street_coordinates.map(coord => ({
      lat: coord[0], 
      lng: coord[1]
    }));
    
    new google.maps.Polyline({
      path: path,
      geodesic: true,
      strokeColor: '#FF0000',
      strokeOpacity: 1.0,
      strokeWeight: 3,
      map: map
    });
  } else {
    // Fallback to straight-line path
    const path = optimizedOrder.map(id => {
      const location = locations.find(loc => loc.id === id);
      return { lat: location.latitude, lng: location.longitude };
    });
    
    new google.maps.Polyline({
      path: path,
      geodesic: true,
      strokeColor: '#0000FF',
      strokeOpacity: 0.7,
      strokeWeight: 2,
      map: map
    });
  }
};
```

## 🎨 React Component Examples

### Complete Route Optimizer Component
```jsx
import React, { useState, useEffect } from 'react';

const RouteOptimizer = ({ selectedLocationIds }) => {
  const [optimizedRoute, setOptimizedRoute] = useState(null);
  const [streetData, setStreetData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [comparison, setComparison] = useState(null);

  const optimizeAndVisualize = async () => {
    if (selectedLocationIds.length < 2) return;
    
    setLoading(true);
    try {
      // Step 1: Get optimized route order from Python backend
      const optimizationResult = await fetch('/api/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ location_ids: selectedLocationIds })
      }).then(r => r.json());
      
      setOptimizedRoute(optimizationResult.optimized_route);
      
      // Step 2: Get street routing data for visualization
      const streetRoutingResult = await fetch('/api/street-routing', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ route_ids: optimizationResult.optimized_route.location_ids })
      }).then(r => r.json());
      
      setStreetData(streetRoutingResult);
      
      // Step 3: Get comparison data
      const comparisonData = await fetch('/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ location_ids: selectedLocationIds })
      }).then(r => r.json());
      
      setComparison(comparisonData);
    } catch (error) {
      console.error('Optimization failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="route-optimizer">
      <button 
        onClick={optimizeAndVisualize} 
        disabled={selectedLocationIds.length < 2 || loading}
      >
        {loading ? 'Optimizing...' : 'Optimize Route'}
      </button>
      
      {optimizedRoute && (
        <div className="results">
          <h3>Optimized Route</h3>
          <ol>
            {optimizedRoute.location_names.map((name, index) => (
              <li key={index}>{name}</li>
            ))}
          </ol>
          
          {streetData && (
            <div className="street-routing">
              <h4>Real Driving Information</h4>
              {streetData.routing_success ? (
                <>
                  <p>Driving Distance: {streetData.total_distance_km.toFixed(1)} km</p>
                  <p>Estimated Time: {streetData.total_time_hours.toFixed(1)} hours</p>
                  <p>Route Type: Actual roads</p>
                </>
              ) : (
                <>
                  <p>Optimization Distance: {optimizedRoute.total_distance.toFixed(1)} km</p>
                  <p>Route Type: Straight-line approximation</p>
                  <p className="warning">Street routing unavailable</p>
                </>
              )}
            </div>
          )}
        </div>
      )}
      
      {comparison && (
        <div className="comparison">
          <h3>Performance Comparison</h3>
          <p>Random Route: {comparison.random_route.distance.toFixed(1)} km</p>
          <p>Optimized Route: {comparison.optimized_route.distance.toFixed(1)} km</p>
          <p>Distance Saved: {comparison.distance_saved.toFixed(1)} km</p>
          <p>Improvement: {comparison.improvement_percentage.toFixed(1)}%</p>
        </div>
      )}
    </div>
  );
};
```

## 🔧 Backend Setup (Flask Example)

```python
from flask import Flask, request, jsonify
from api_interface import RouteOptimizationAPI

app = Flask(__name__)
api = RouteOptimizationAPI()

@app.route('/api/locations', methods=['GET'])
def get_locations():
    return jsonify(api.get_all_locations())

@app.route('/api/locations', methods=['POST'])
def add_location():
    data = request.json
    new_id = api.add_custom_location(
        data['name'], 
        data['latitude'], 
        data['longitude']
    )
    return jsonify({'id': new_id, **data})

@app.route('/api/optimize', methods=['POST'])
def optimize_route():
    data = request.json
    result = api.optimize_route(data['location_ids'])
    return jsonify(result)

@app.route('/api/street-routing', methods=['POST'])
def get_street_routing():
    data = request.json
    result = api.get_street_routing_data(data['route_ids'])
    return jsonify(result)

@app.route('/api/compare', methods=['POST'])
def compare_routes():
    data = request.json
    result = api.compare_with_random(data['location_ids'])
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## 📊 Performance Expectations

- **Optimization Time**: ~0.005 seconds for 5-9 locations
- **Street Routing Time**: ~1-3 seconds (OSRM API call)
- **Distance Improvement**: 30-50% better than random routes
- **API Response Time**: <100ms for optimization, <3s for street routing
- **Memory Usage**: ~10MB total

## 🎯 Key Features for React Integration

1. **Real-time Optimization**: Instant route calculation from Python backend
2. **Street Routing**: Actual road paths for realistic visualization
3. **Interactive Maps**: Easy integration with any mapping library
4. **Dynamic Location Management**: Add/remove locations on the fly
5. **Performance Metrics**: Compare optimized vs random routes
6. **Flexible Data Format**: JSON responses ready for React state

## 🚀 Ready to Integrate!

The API is production-ready and optimized for web applications. The Python backend handles the complex optimization, while React handles the beautiful interactive interface.

**Architecture Summary:**
- **Python Backend**: Genetic algorithm optimization + street routing
- **React Frontend**: Interactive maps + user interface
- **Communication**: REST API calls between frontend and backend
- **Result**: Fast optimization + realistic route visualization

**Next Steps:**
1. Set up the Flask backend with our API
2. Create React components for location selection
3. Integrate with your preferred mapping library
4. Add real-time optimization triggers
5. Style and polish the UI

The data science team has provided a robust, fast, and accurate route optimization system ready for your React frontend! 🎉 