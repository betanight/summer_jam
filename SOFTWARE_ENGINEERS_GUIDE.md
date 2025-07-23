# Software Engineers Integration Guide

## 🚀 Quick API Integration

This guide shows software engineers how to easily integrate our route optimization API into their own projects.

## 📡 API Endpoints Overview

### Core Endpoints
- `GET /health` - API health check
- `GET /places` - Find attractions along route
- `GET /route-points` - Get city coordinates  
- `POST /optimize` - Basic route optimization
- `POST /optimize-with-directions` - Complete route optimization with street directions

## 🔗 Easy Integration Methods

### Method 1: Direct API Calls
```javascript
// Find attractions between cities
const response = await fetch('http://localhost:8000/places?fromCity=Los%20Angeles&toCity=San%20Francisco');
const data = await response.json();
const attractions = data.data.attractions;

// Optimize route with selected attractions
const optimizationResponse = await fetch('http://localhost:8000/optimize-with-directions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(selectedAttractions)
});
```

### Method 2: Copy Core Functions
You can copy these functions directly into your project:

#### Route Optimization Function
```python
def optimize_route(location_ids):
    # Copy from backend/api_interface.py - optimize_route method
    # Returns optimized route with distance calculations
```

#### Attraction Finding Function  
```python
def get_attractions_along_route(from_city, to_city, max_attractions=9):
    # Copy from backend/api_interface.py - get_attractions_along_route method
    # Returns attractions formatted for frontend
```

#### Street Directions Function
```python
def get_street_directions(optimized_route):
    # Copy from backend/api_interface.py - get_street_directions method
    # Returns route coordinates for map display
```

## 🛠️ Backend Functions Location

### Core Functions in `backend/api_interface.py`:
- `optimize_route()` - Main optimization algorithm
- `get_attractions_along_route()` - Find attractions near route
- `get_street_directions()` - Get route coordinates
- `get_route_points_coordinates()` - Get city coordinates
- `_find_attractions_near_route()` - Distance-based attraction filtering

### API Endpoints in `backend/web_api.py`:
- All FastAPI endpoints for HTTP requests
- Request/response models
- Error handling and validation

### Data Loading in `backend/api_interface.py`:
- `_load_california_attractions()` - Load attraction data
- `_initialize_system()` - Setup API with data

## 📊 Data Integration

### Attraction Dataset
- **File**: `backend/analysis/california_attractions_data.csv`
- **Format**: CSV with name, city, state, category, latitude, longitude, image_link
- **Size**: 952 California attractions

### Data Structure
```json
{
  "key": "attraction_0",
  "name": "Hollywood Sign",
  "town": "Los Angeles", 
  "rating": 4.5,
  "image": "image_url",
  "location": {"lat": 34.1341, "lng": -118.3215},
  "category": "Landmark",
  "distance_from_route": 0.5
}
```

## 🔧 Integration Examples

### React Frontend Integration
```javascript
// Constants
const API_BASE_URL = 'http://localhost:8000';

// API Functions
const api = {
  async getAttractions(fromCity, toCity) {
    const response = await fetch(
      `${API_BASE_URL}/places?fromCity=${encodeURIComponent(fromCity)}&toCity=${encodeURIComponent(toCity)}`
    );
    return response.json();
  },

  async optimizeRoute(selectedAttractions) {
    const response = await fetch(`${API_BASE_URL}/optimize-with-directions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(selectedAttractions)
    });
    return response.json();
  },

  async getRoutePoints(fromCity, toCity) {
    const response = await fetch(
      `${API_BASE_URL}/route-points?fromCity=${encodeURIComponent(fromCity)}&toCity=${encodeURIComponent(toCity)}`
    );
    return response.json();
  }
};
```

### Python Backend Integration
```python
# Copy these functions directly into your project
from api_interface import RouteOptimizationAPI

class YourRouteOptimizer:
    def __init__(self):
        self.api = RouteOptimizationAPI()
    
    def find_attractions(self, from_city, to_city):
        return self.api.get_attractions_along_route(from_city, to_city)
    
    def optimize_route(self, attractions):
        return self.api.optimize_route(attractions)
    
    def get_directions(self, optimized_route):
        return self.api.get_street_directions(optimized_route)
```

## 🚀 Quick Start for Your Project

### Step 1: Clone the Repository
```bash
git clone https://github.com/betanight/summer_jam.git
cd summer_jam/backend
```

### Step 2: Copy Core Functions
Copy these files to your project:
- `api_interface.py` - Core optimization logic
- `analysis/california_attractions_data.csv` - Attraction dataset

### Step 3: Install Dependencies
```bash
pip install fastapi uvicorn pandas numpy geopy
```

### Step 4: Use the Functions
```python
from api_interface import RouteOptimizationAPI

api = RouteOptimizationAPI()

# Find attractions
attractions = api.get_attractions_along_route("Los Angeles", "San Francisco")

# Optimize route
optimized = api.optimize_route([0, 1, 2, 3])

# Get directions
directions = api.get_street_directions(optimized_route)
```

## 📡 API Response Formats

### Attractions Response
```json
{
  "success": true,
  "data": {
    "attractions": [
      {
        "key": "attraction_0",
        "name": "Hollywood Sign",
        "town": "Los Angeles",
        "rating": 4.5,
        "image": "image_url",
        "location": {"lat": 34.1341, "lng": -118.3215},
        "category": "Landmark",
        "distance_from_route": 0.5
      }
    ]
  },
  "message": "Found 9 attractions along route"
}
```

### Route Optimization Response
```json
{
  "success": true,
  "data": {
    "optimized_route": [
      {
        "key": "attraction_0",
        "location": {"lat": 34.1341, "lng": -118.3215}
      }
    ],
    "directions": {
      "origin": {"lat": 34.1341, "lng": -118.3215, "name": "attraction_0"},
      "destination": {"lat": 37.7648, "lng": -122.4269, "name": "attraction_1"},
      "waypoints": [],
      "total_locations": 2,
      "route_coordinates": [...]
    }
  },
  "message": "Route optimized with street directions"
}
```

## 🗺️ Map Integration

### Google Maps Integration
```javascript
// Use the optimized route data with Google Maps
const route = optimizedResponse.data.optimized_route;
const directions = optimizedResponse.data.directions;

// Create waypoints for Google Maps DirectionsService
const waypoints = route.slice(1, -1).map(point => ({
  location: point.location,
  stopover: true
}));

// Use with Google Maps API
directionsService.route({
  origin: route[0].location,
  destination: route[route.length - 1].location,
  waypoints: waypoints,
  travelMode: google.maps.TravelMode.DRIVING
}, (result, status) => {
  if (status === 'OK') {
    directionsRenderer.setDirections(result);
  }
});
```

## 🔧 Customization Options

### Distance Configuration
```python
# Modify search radius in api_interface.py
max_distance_miles = 10.0  # Default: 10 miles
max_attractions = 9        # Default: 9 attractions
```

### Category Filtering
```python
# Add category filtering in get_attractions_along_route()
categories = ['Restaurant', 'Landmark', 'Museum']  # Filter by categories
```

### Route Optimization Algorithm
```python
# Modify optimization in _simple_optimize_route()
# Currently uses nearest neighbor algorithm
# Can be replaced with genetic algorithm or other methods
```

## 🐛 Troubleshooting

### Common Issues
1. **API not starting**: Check port 8000 availability
2. **No attractions found**: Try different California cities
3. **CORS errors**: Add CORS middleware to your frontend
4. **Data loading errors**: Verify CSV file path

### Debug Endpoints
- `GET /health` - Check API status
- `GET /stats` - View API statistics
- `GET /locations` - List all attractions

## 📞 Support

For integration help:
1. Check the API documentation at `http://localhost:8000/docs`
2. Review the core functions in `backend/api_interface.py`
3. Test with the provided examples above
4. Use the health check endpoint to verify API status

---

**Ready to integrate!** 🚀 Copy the functions you need and start building your route optimization features.
