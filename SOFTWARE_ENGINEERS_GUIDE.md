# Software Engineers Integration Guide

## 📁 File Structure & Purpose

### Core Files

#### `api_interface.py` - Main API for React Integration
**Purpose**: The primary interface that React will call to get route optimization data.

**Key Functions for React Team**:
- `get_all_locations()` - Returns all available locations (9 European landmarks + any custom ones)
- `add_custom_location(name, latitude, longitude)` - Adds new location (hotels, restaurants, etc.)
- `optimize_route(location_ids)` - Finds optimal route order for selected locations
- `compare_with_random(location_ids)` - Compares optimized vs random route performance
- `get_route_visualization_data(route_ids)` - Gets coordinates for map visualization
- `get_street_routing_data(route_ids)` - Gets actual road routing data

#### `main.py` - Demo/Testing File
**Purpose**: Shows how to use the API. You can run this to test functionality.

#### `requirements.txt` - Dependencies
**Purpose**: Lists all Python packages needed. Install with `pip install -r requirements.txt`

### Data Science Modules (src/ folder)

#### `src/data_loader.py` - Data Management
**Purpose**: Handles loading and validating location data.
**What it does**: 
- Loads CSV file with 9 European landmarks
- Validates coordinates are within reasonable ranges
- Adds new custom locations
- Provides clean data to other modules

#### `src/distance_calculator.py` - Distance Calculations
**Purpose**: Calculates distances between locations using Haversine formula.
**What it does**:
- Creates distance matrix between all locations
- Calculates total route distance
- Handles coordinate validation

#### `src/baseline_model.py` - Random Route Generator
**Purpose**: Creates random routes for comparison with optimized routes.
**What it does**:
- Generates random route orders
- Provides baseline performance metrics
- Used to show improvement of optimization

#### `src/optimization_model.py` - Genetic Algorithm TSP Solver
**Purpose**: Finds the optimal route using genetic algorithms.
**What it does**:
- Implements Traveling Salesman Problem solver
- Uses evolutionary computation to find best route
- Provides significant improvement over random routes

#### `src/visualization.py` - Visualization Utilities
**Purpose**: Provides data for creating charts and visualizations.
**What it does**:
- Generates performance comparison charts
- Creates route visualization data
- Prepares data for frontend display

### Data Files

#### `data/locations.csv` - Location Dataset
**Purpose**: Contains the 9 European landmarks with coordinates.
**Format**: CSV with columns: id, name, latitude, longitude, city

## 🎯 Functions for React Dashboard

### 1. Getting All Locations
**Function**: `api.get_all_locations()`
**Returns**: List of location dictionaries with id, name, latitude, longitude
**Use Case**: Populate location selector in React dashboard

### 2. Adding Custom Locations
**Function**: `api.add_custom_location(name, latitude, longitude)`
**Returns**: ID of the new location
**Use Case**: Let users add their hotels, restaurants, or personal landmarks

### 3. Optimizing Routes
**Function**: `api.optimize_route(location_ids)`
**Returns**: Optimized route with location order, total distance, execution time
**Use Case**: Find the best route order for selected locations

### 4. Getting Street Routing Data
**Function**: `api.get_street_routing_data(route_ids)`
**Returns**: Actual road coordinates, driving distance, estimated time
**Use Case**: Display realistic driving routes on maps

### 5. Comparing Performance
**Function**: `api.compare_with_random(location_ids)`
**Returns**: Comparison between optimized and random routes
**Use Case**: Show users how much the optimization improves their route

### 6. Getting Visualization Data
**Function**: `api.get_route_visualization_data(route_ids)`
**Returns**: Coordinates and metadata for map display
**Use Case**: Draw routes on interactive maps

## 🛣️ Route Types Available

### 1. Optimization Routes (Straight-line)
- **Purpose**: Fast TSP optimization
- **Distance**: Direct point-to-point using Haversine formula
- **Speed**: ~0.005 seconds for 9 locations
- **Use**: Finding optimal location order

### 2. Street Routing (Actual Roads)
- **Purpose**: Realistic driving paths
- **Distance**: Actual road network distances
- **API**: Uses OSRM (Open Source Routing Machine)
- **Use**: Displaying realistic routes on maps

## 📊 Sample Data Formats

### Location Data
```json
{
  "id": 0,
  "name": "Sagrada Familia Barcelona",
  "latitude": 41.4036,
  "longitude": 2.1744,
  "city": "Barcelona"
}
```

### Optimization Result
```json
{
  "optimized_route": {
    "location_ids": [2, 0, 3, 1, 4],
    "location_names": ["Colosseum", "Sagrada Familia", "Eiffel Tower", "Anne Frank House", "Oia"],
    "total_distance": 3381.2,
    "execution_time": 0.004
  }
}
```

### Street Routing Data
```json
{
  "street_coordinates": [[lat1, lon1], [lat2, lon2], ...],
  "route_names": ["Colosseum", "Sagrada Familia", ...],
  "total_distance_km": 3456.7,
  "total_time_hours": 42.3,
  "routing_success": true
}
```

## 🔧 Integration Steps for React Team

### Step 1: Set up Python Backend
1. Install dependencies: `pip install -r requirements.txt`
2. Create Flask/FastAPI server that imports `api_interface.py`
3. Create REST endpoints that call the API functions

### Step 2: Create React Components
1. Location selector component (uses `get_all_locations()`)
2. Route optimizer component (uses `optimize_route()`)
3. Map visualization component (uses `get_street_routing_data()`)
4. Performance comparison component (uses `compare_with_random()`)

### Step 3: Connect Frontend to Backend
1. Make API calls from React to your Python backend
2. Handle the JSON responses in React state
3. Display results in your dashboard

## ✅ Verification Checklist

- [x] **Easy Location Addition**: `add_custom_location()` works seamlessly
- [x] **React Integration Ready**: All functions return clean JSON
- [x] **Both Route Types**: Straight-line optimization + actual road routing
- [x] **Performance Metrics**: Compare optimized vs random routes
- [x] **Error Handling**: All functions have proper error handling
- [x] **Documentation**: Complete function descriptions and examples

## 🚀 Ready for React Dashboard

The data science team has provided:
- **Fast optimization** (~0.005 seconds)
- **Real street routing** (actual roads, distances, times)
- **Easy location management** (add/remove locations)
- **Performance comparisons** (optimized vs random)
- **Clean API interface** (ready for REST endpoints)

**Your React team can now build an amazing interactive dashboard!** 🎯 