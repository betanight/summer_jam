# Frontend Integration Guide

## Overview

This backend provides attractions data for the frontend team's route optimization system. The system allows users to:

1. **Search for routes** between two cities
2. **Display start/end markers** on the map (blue for start, green for end)
3. **Discover attractions** along the route (max 9 attractions)
4. **Choose attractions** within 10 miles of their route
5. **Visualize the route** with selected attractions on Google Maps

## API Endpoints

### GET `/route-points`

Returns coordinates for start and end cities to display on the map.

**Parameters:**
- `fromCity` (required): Starting city name
- `toCity` (required): Destination city name

**Example Request:**
```
GET /route-points?fromCity=Los%20Angeles&toCity=San%20Francisco
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "start": {
      "city": "Los Angeles",
      "lat": 34.0536909,
      "lng": -118.242766,
      "color": "blue"
    },
    "end": {
      "city": "San Francisco", 
      "lat": 37.7792588,
      "lng": -122.4193286,
      "color": "green"
    }
  },
  "message": "Found coordinates for route from Los Angeles to San Francisco"
}
```

### GET `/places`

Returns attractions along a route between two cities.

**Parameters:**
- `fromCity` (required): Starting city name
- `toCity` (required): Destination city name  
- `max_attractions` (optional): Maximum attractions to return (default: 9, max: 9)
- `max_distance_miles` (optional): Maximum distance from route in miles (default: 10.0, max: 50.0)

**Example Request:**
```
GET /places?fromCity=Los%20Angeles&toCity=San%20Francisco&max_attractions=5&max_distance_miles=10.0
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "attractions": [
      {
        "key": "attraction_0",
        "name": "Yosemite National Park",
        "town": "Yosemite Valley",
        "rating": 4.5,
        "image": "https://via.placeholder.com/300x200?text=Attraction",
        "location": {
          "lat": 37.8651,
          "lng": -119.5383
        },
        "category": "National Park",
        "distance_from_route": 2.5
      }
    ]
  },
  "message": "Found 5 attractions along route"
}
```

## Frontend Integration

### 1. Search Flow

1. User enters start and destination cities
2. Frontend calls `/route-points` to get coordinates for map markers
3. Frontend displays blue marker (start) and green marker (end) on map
4. Frontend calls `/places` endpoint to get attractions along the route
5. Frontend displays attractions in sidebar for user selection

### 2. Map Display

- **Blue marker**: Starting city location
- **Green marker**: Destination city location
- **Attraction markers**: Red pins for attractions along the route
- **Route line**: Drawn between selected attractions when optimized

### 3. Attraction Selection

- Users can "like" attractions by clicking heart buttons
- Selected attractions are stored in frontend state
- Maximum 9 attractions can be selected

### 4. Route Optimization

- When user clicks "Make Route", frontend sends selected attraction IDs to `/optimize`
- Backend optimizes the route using genetic algorithms
- Returns optimized route with coordinates for Google Maps visualization

### 5. Map Visualization

- Frontend uses Google Maps API to display route
- Start/end markers remain visible throughout the process
- Attractions are shown as markers on the map
- Route is drawn between selected attractions

## Data Sources

### California Attractions

The backend uses a comprehensive dataset of California attractions including:

- **National Parks**: Yosemite, Redwood, Death Valley, etc.
- **Landmarks**: Golden Gate Bridge, Hollywood Sign, Alcatraz
- **Amusement Parks**: Disneyland, Universal Studios, Six Flags
- **Beaches**: Venice Beach, Santa Monica Pier, Malibu
- **Museums**: Getty Center, LACMA, California Science Center
- **Historical Sites**: Mission San Juan Capistrano, Sutter's Fort
- **Roadside Attractions**: Cabazon Dinosaurs, Salvation Mountain
- **Wine Regions**: Napa Valley, Sonoma Valley, Paso Robles

### Distance Calculation

- Uses geodesic distance calculation for accurate route proximity
- Attractions within specified distance (default 10 miles) are included
- Sorted by distance from route for optimal user experience

## Technical Implementation

### Route Finding

1. **Geocoding**: Convert city names to coordinates using Nominatim
2. **Route Generation**: Create route points between start and end cities
3. **Distance Filtering**: Find attractions within specified distance of route
4. **Formatting**: Return data in frontend-compatible format

### Data Format

Each attraction includes:
- `key`: Unique identifier for React rendering
- `name`: Attraction name
- `town`: City/town location
- `rating`: Default rating (4.5 for all attractions)
- `image`: Placeholder or actual image URL
- `location`: Google Maps compatible coordinates
- `category`: Type of attraction
- `distance_from_route`: Distance in miles from route

## Setup Instructions

### Backend Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Start the API server:
```bash
python start_api.py
```

3. Test the integration:
```bash
python test_api.py
```

### Frontend Setup

1. Clone the frontend repository:
```bash
git clone https://github.com/manahilsami/route_optimizer_fe.git
cd route_optimizer_fe
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. The frontend will automatically connect to `http://localhost:8000`

## Testing

### API Testing

Run the comprehensive test suite:
```bash
cd backend
python test_api.py
```

This will test:
- Health check endpoint
- Location management
- Route optimization
- New `/places` endpoint
- New `/route-points` endpoint
- Data formatting for frontend

### Frontend Testing

1. Enter "Los Angeles" as starting city
2. Enter "San Francisco" as destination city
3. Click search to see route markers and attractions
4. Verify blue marker (start) and green marker (end) appear on map
5. Select attractions by clicking heart buttons
6. Click "Make Route" to optimize and visualize

## Error Handling

### Common Issues

1. **City Not Found**: Ensure city names are valid California cities
2. **No Attractions**: Try increasing `max_distance_miles` parameter
3. **API Connection**: Verify backend is running on port 8000
4. **CORS Issues**: Backend includes CORS middleware for frontend access
5. **Map Markers Not Showing**: Check if route-points endpoint is working

### Debugging

- Check browser console for API errors
- Verify network requests in browser dev tools
- Check backend logs for detailed error messages
- Use `/health` endpoint to verify API status

## Future Enhancements

1. **Real Google Maps Directions**: Integrate actual Google Maps Directions API
2. **User Ratings**: Add real user ratings and reviews
3. **Image Enhancement**: Replace placeholder images with real attraction photos
4. **Advanced Filtering**: Add category-based filtering
5. **Route Preferences**: Allow users to specify route preferences (scenic, fastest, etc.)

## Support

For technical issues or questions about the integration, refer to:
- Backend API documentation: `/docs` endpoint
- Frontend repository: https://github.com/manahilsami/route_optimizer_fe.git
- Test files for examples of proper API usage 