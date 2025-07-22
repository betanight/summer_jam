# Software Engineer Guide

Welcome to the Route Optimization API team. This guide provides instructions for using the route optimization system.

## Overview

The Route Optimization API helps determine the optimal travel routes between multiple locations in California. The system uses genetic algorithms to find the shortest possible route between selected attractions and points of interest.

## Getting Started

### Step 1: Start the API
Navigate to the backend directory and run:
```bash
cd backend
python3 start_api.py
```

The server will start and display:
```
Starting Route Optimization API Server...
Dependencies are installed
API will be available at: http://localhost:8000
```

### Step 2: Test the API
In a separate terminal window, run:
```bash
python3 test_api.py
```

All tests should pass with green checkmarks.

### Step 3: Access Documentation
Open your web browser and navigate to: `http://localhost:8000/docs`

This provides interactive API documentation for testing endpoints.

## Available Endpoints

### 1. Get All Locations
**Purpose:** Retrieve all available California attractions
**Method:** GET
**URL:** `http://localhost:8000/locations`

### 2. Optimize Route
**Purpose:** Calculate the optimal route between selected locations
**Method:** POST
**URL:** `http://localhost:8000/optimize`

### 3. Compare Routes
**Purpose:** Compare optimized route with random route
**Method:** POST
**URL:** `http://localhost:8000/compare`

### 4. Get Visualization Data
**Purpose:** Retrieve data for route visualization
**Method:** POST
**URL:** `http://localhost:8000/visualization`

### 5. Get Street Routing Data
**Purpose:** Retrieve actual driving directions
**Method:** POST
**URL:** `http://localhost:8000/street-routing`

### 6. Quick Optimization
**Purpose:** Fast route optimization using URL parameters
**Method:** GET
**URL:** `http://localhost:8000/quick-optimize?location_ids=0,1,2,3,4`

### 7. Add Custom Location
**Purpose:** Add new locations to the system
**Method:** POST
**URL:** `http://localhost:8000/locations`

## Available Attractions

The system contains nearly 1000 California attractions including:

**National Parks:**
- Yosemite National Park
- Redwood National and State Parks
- Death Valley National Park
- Joshua Tree National Park
- Sequoia National Park
- Kings Canyon National Park

**Landmarks:**
- Golden Gate Bridge
- Hollywood Sign
- Alcatraz Island

**Amusement Parks:**
- Disneyland
- Universal Studios Hollywood
- Six Flags Magic Mountain

**Beaches:**
- Venice Beach
- Santa Monica Pier
- Malibu Beach
- La Jolla Cove

**Museums:**
- Getty Center
- LACMA
- California Science Center

**Wine Regions:**
- Napa Valley
- Sonoma Valley
- Paso Robles

**Roadside Attractions:**
- Cabazon Dinosaurs
- Salvation Mountain
- World's Largest Thermometer
- The Donut Hole
- Motel Crystal Pier

## API Usage Examples

### JavaScript
```javascript
// Get all locations
fetch('http://localhost:8000/locations')
  .then(response => response.json())
  .then(data => {
    console.log('Locations:', data.data.locations);
  });

// Optimize route
fetch('http://localhost:8000/optimize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ location_ids: [0, 1, 2, 3, 4] })
})
.then(response => response.json())
.then(data => {
  console.log('Optimized route:', data.data.optimized_route);
});

// Compare routes
fetch('http://localhost:8000/compare', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ location_ids: [0, 1, 2, 3, 4] })
})
.then(response => response.json())
.then(data => {
  console.log('Route comparison:', data.data);
});
```

### Python
```python
import requests

# Get all locations
response = requests.get('http://localhost:8000/locations')
locations = response.json()['data']['locations']
print('Locations:', locations)

# Optimize route
response = requests.post('http://localhost:8000/optimize', json={
    'location_ids': [0, 1, 2, 3, 4]
})
optimized_route = response.json()['data']['optimized_route']
print('Optimized route:', optimized_route)

# Compare routes
response = requests.post('http://localhost:8000/compare', json={
    'location_ids': [0, 1, 2, 3, 4]
})
comparison = response.json()['data']
print('Route comparison:', comparison)
```

## Response Formats

### Route Optimization Response
```json
{
  "success": true,
  "data": {
    "optimized_route": {
      "location_ids": [4, 3, 0, 2, 1],
      "location_names": ["Disneyland", "Universal Studios Hollywood", "Yosemite National Park", "Redwood National and State Parks", "Death Valley National Park"],
      "total_distance": 1234.5,
      "execution_time": 0.003
    }
  }
}
```

### Route Comparison Response
```json
{
  "success": true,
  "data": {
    "random_route": {
      "distance": 1500.2,
      "route": [0, 1, 2, 3, 4]
    },
    "optimized_route": {
      "distance": 1234.5,
      "route": [4, 3, 0, 2, 1]
    },
    "improvement_percentage": 17.7,
    "distance_saved": 265.7
  }
}
```

## System Features

### Performance
- Route optimization completes in under 0.01 seconds
- Supports up to 9 locations simultaneously
- Uses genetic algorithms for optimization

### Optimization Quality
- Typically 15-30% improvement over random routes
- Significant distance savings on multi-location routes
- Real coordinate-based distance calculations

### Data Source
- Nearly 1000 California attractions
- Real geographic coordinates
- Diverse attraction categories

### API Design
- RESTful HTTP endpoints
- Language-agnostic interface
- Interactive documentation available
- Comprehensive error handling

## Common Questions

### Adding Custom Locations
Use the POST `/locations` endpoint to add hotels, restaurants, or any custom locations.

### Accuracy
The system uses real geographic coordinates and calculates actual distances between locations.

### Error Handling
Check the `/health` endpoint to verify API status. Error messages provide specific guidance.

### Integration
The API is designed for integration with any programming language through HTTP requests.

### Data Source
The system uses a curated dataset of approximately 1000 California attractions including National Parks, landmarks, museums, beaches, amusement parks, wine regions, historical sites, and roadside attractions.

## Troubleshooting

### Server Startup Issues
- Ensure you are in the `backend` directory
- Use `python3 start_api.py` (not `python`)
- Verify all dependencies are installed

### Connection Errors
- Confirm the server is running
- Verify the URL is `http://localhost:8000`
- Test the health endpoint first: `http://localhost:8000/health`

### API Errors
- Check the interactive documentation at `http://localhost:8000/docs`
- Verify request data format
- Review error message details

### Data Loading Issues
- Ensure the California attractions data file exists
- Verify the data file is in the correct location
- Restart the API server if necessary

## Support Resources

- **Interactive Documentation:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`
- **API Testing:** Run `python3 test_api.py`
- **Detailed Documentation:** See `backend/API_DOCUMENTATION.md`

## Use Cases

The Route Optimization API can be used to build:
- California travel planning applications
- Delivery route optimization systems
- Tour guide applications
- Logistics dashboards
- Interactive mapping applications

The data science team has implemented the optimization algorithms and mathematical models. Software engineers can access this functionality through simple HTTP requests to build applications and services.
