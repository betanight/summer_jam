# Route Optimization API Documentation

This document provides comprehensive documentation for the Route Optimization API, designed for the software engineering team to integrate with the data science functionality.

## Quick Start

### 1. Start the API Server

```bash
cd backend
python start_api.py
```

The API will be available at `http://localhost:8000`

### 2. Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation with Swagger UI.

## API Endpoints

### Health Check
**GET** `/health`

Check if the API is running and ready.

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "api_ready": true
  },
  "message": "API is running"
}
```

### Get All Locations
**GET** `/locations`

Retrieve all available locations in the system.

**Response:**
```json
{
  "success": true,
  "data": {
    "locations": [
      {
        "id": 0,
        "name": "Sagrada Familia",
        "latitude": 41.4036,
        "longitude": 2.1744,
        "city": "Barcelona"
      }
    ],
    "count": 9
  },
  "message": "Retrieved 9 locations"
}
```

### Add Custom Location
**POST** `/locations`

Add a new custom location to the system.

**Request Body:**
```json
{
  "name": "Custom Location",
  "latitude": 40.7128,
  "longitude": -74.0060
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "location_id": 10,
    "location": {
      "name": "Custom Location",
      "latitude": 40.7128,
      "longitude": -74.0060
    }
  },
  "message": "Location 'Custom Location' added successfully"
}
```

### Optimize Route
**POST** `/optimize`

Optimize a route for the given location IDs using genetic algorithms.

**Request Body:**
```json
{
  "location_ids": [0, 1, 2, 3, 4]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "optimized_route": {
      "location_ids": [0, 2, 1, 4, 3],
      "location_names": ["Sagrada Familia", "Anne Frank House", "Eiffel Tower", "Colosseum", "Big Ben"],
      "total_distance": 2847.3,
      "execution_time": 0.045
    }
  },
  "message": "Route optimized successfully"
}
```

### Compare Routes
**POST** `/compare`

Compare an optimized route with a random baseline route.

**Request Body:**
```json
{
  "location_ids": [0, 1, 2, 3, 4]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "random_route": {
      "distance": 4100.2,
      "route": [0, 3, 1, 4, 2]
    },
    "optimized_route": {
      "distance": 2847.3,
      "route": [0, 2, 1, 4, 3]
    },
    "improvement_percentage": 30.9,
    "distance_saved": 1252.9
  },
  "message": "Route comparison completed"
}
```

### Get Visualization Data
**POST** `/visualization`

Get data for visualizing a route on a map.

**Request Body:**
```json
{
  "route_ids": [0, 1, 2, 3, 4]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "route_coordinates": [
      [41.4036, 2.1744],
      [52.3676, 4.9041],
      [48.8584, 2.2945]
    ],
    "route_names": ["Sagrada Familia", "Anne Frank House", "Eiffel Tower"],
    "total_distance": 2847.3,
    "num_locations": 5
  },
  "message": "Visualization data retrieved"
}
```

### Get Street Routing Data
**POST** `/street-routing`

Get actual street routing data using OSRM (Open Source Routing Machine).

**Request Body:**
```json
{
  "route_ids": [0, 1, 2, 3, 4]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "street_coordinates": [
      [41.4036, 2.1744],
      [52.3676, 4.9041]
    ],
    "route_names": ["Sagrada Familia", "Anne Frank House"],
    "total_distance_km": 1250.5,
    "total_time_hours": 12.5,
    "num_locations": 5,
    "routing_success": true
  },
  "message": "Street routing data retrieved"
}
```

### Quick Optimization
**GET** `/quick-optimize?location_ids=0,1,2,3,4`

Quick route optimization using query parameters.

**Response:**
```json
{
  "success": true,
  "data": {
    "optimized_route": {
      "location_ids": [0, 2, 1, 4, 3],
      "location_names": ["Sagrada Familia", "Anne Frank House", "Eiffel Tower", "Colosseum", "Big Ben"],
      "total_distance": 2847.3,
      "execution_time": 0.045
    }
  },
  "message": "Route optimized successfully"
}
```

### Get API Statistics
**GET** `/stats`

Get API statistics and system information.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_locations": 9,
    "api_version": "1.0.0",
    "algorithm": "Genetic Algorithm TSP",
    "distance_formula": "Haversine",
    "sample_locations": ["Sagrada Familia", "Anne Frank House", "Eiffel Tower", "Colosseum", "Big Ben"]
  },
  "message": "API statistics retrieved"
}
```

## Integration Examples

### JavaScript/Node.js

```javascript
// Get all locations
const response = await fetch('http://localhost:8000/locations');
const data = await response.json();
console.log(data.data.locations);

// Optimize a route
const optimizeResponse = await fetch('http://localhost:8000/optimize', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    location_ids: [0, 1, 2, 3, 4]
  })
});
const result = await optimizeResponse.json();
console.log(result.data.optimized_route);
```

### Python

```python
import requests

# Get all locations
response = requests.get('http://localhost:8000/locations')
data = response.json()
print(data['data']['locations'])

# Optimize a route
response = requests.post('http://localhost:8000/optimize', json={
    'location_ids': [0, 1, 2, 3, 4]
})
result = response.json()
print(result['data']['optimized_route'])
```

### cURL

```bash
# Get all locations
curl http://localhost:8000/locations

# Optimize a route
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{"location_ids": [0, 1, 2, 3, 4]}'

# Quick optimization
curl "http://localhost:8000/quick-optimize?location_ids=0,1,2,3,4"
```

## Error Handling

All endpoints return consistent error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request (invalid input)
- `500` - Internal Server Error
- `503` - Service Unavailable (API not initialized)

## Data Science Features

### Algorithm Details
- **Optimization Algorithm**: Genetic Algorithm for Traveling Salesman Problem (TSP)
- **Distance Calculation**: Haversine formula for accurate geographic distances
- **Performance**: Typically 30% improvement over random routes
- **Execution Time**: Sub-second optimization for up to 9 locations

### Available Locations
The system comes pre-loaded with 9 European landmarks:
1. Sagrada Familia (Barcelona)
2. Anne Frank House (Amsterdam)
3. Eiffel Tower (Paris)
4. Colosseum (Rome)
5. Big Ben (London)
6. Brandenburg Gate (Berlin)
7. Charles Bridge (Prague)
8. St. Stephen's Cathedral (Vienna)
9. Fisherman's Bastion (Budapest)

## Production Considerations

1. **CORS Configuration**: Update CORS settings for production domains
2. **Authentication**: Add authentication if needed
3. **Rate Limiting**: Implement rate limiting for production use
4. **Error Logging**: Configure proper error logging
5. **Environment Variables**: Use environment variables for configuration

## Support

For questions or issues, refer to:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health` 