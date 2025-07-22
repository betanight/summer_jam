# 🚀 Route Optimization API - Software Engineer Integration Guide

## Overview

This backend provides attractions data for the frontend team's route optimization system. The system allows users to:

1. **Search for routes** between two cities
2. **Display start/end markers** on the map (blue for start, green for end)
3. **Discover attractions** along the route (max 9 attractions)
4. **Choose attractions** within 10 miles of their route
5. **Visualize the route** with selected attractions on Google Maps

## 🎯 Working California Cities

### ✅ Confirmed Working Cities (49 total)

These cities have been tested and work with the route API. Users can use any combination as start/end points:

| # | City | # | City | # | City | # | City |
|---|------|---|------|---|------|---|------|
| 1 | Apple Valley | 14 | Hayward | 27 | Newport Beach | 40 | Santa Ana |
| 2 | Brea | 15 | Huntington Beach | 28 | Ontario | 41 | Santa Barbara |
| 3 | Chico | 16 | La Mesa | 29 | Redwood City | 42 | Santa Clara |
| 4 | Chino | 17 | La Puente | 30 | San Bernardino | 43 | Santa Monica |
| 5 | Concord | 18 | Lake Forest | 31 | San Bruno | 44 | Santa Rosa |
| 6 | Corona | 19 | Lakewood | 32 | San Diego | 45 | South Gate |
| 7 | Costa Mesa | 20 | Long Beach | 33 | San Francisco | 46 | Temple City |
| 8 | Cypress | 21 | Los Angeles | 34 | San Jacinto | 47 | Tulare |
| 9 | Davis | 22 | Madera | 35 | San Leandro | 48 | Union City |
| 10 | Fairfield | 23 | Merced | 36 | San Mateo | 49 | Yorba Linda |
| 11 | Fontana | 24 | Mission Viejo | 37 | San Rafael | | |
| 12 | Garden Grove | 25 | Modesto | 38 | San Ramon | | |
| 13 | Hayward | 26 | Mountain View | 39 | Santa Ana | | |

### 🎯 Best Testing Combinations

For demo and testing purposes, use these proven city pairs:

1. **Los Angeles → San Francisco** (Major coastal route)
2. **San Diego → Sacramento** (North-South route)  
3. **Fresno → Oakland** (Central to Bay Area)
4. **San Jose → Riverside** (Bay Area to Inland Empire)
5. **Stockton → San Bernardino** (Central Valley to Inland Empire)

### ⚠️ Important Notes

- **Exact Names**: Use city names exactly as listed above
- **Geocoding**: Uses free Nominatim service (may occasionally timeout)
- **Fallback**: If a city fails, try nearby major cities from the list
- **Testing**: Always test with known working combinations first

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

### 2. API Usage Examples

```javascript
// Get route points (start/end markers)
const getRoutePoints = async (fromCity, toCity) => {
  const response = await fetch(
    `/route-points?fromCity=${encodeURIComponent(fromCity)}&toCity=${encodeURIComponent(toCity)}`
  );
  const data = await response.json();
  return data.success ? data.data : null;
};

// Get attractions along route
const getAttractions = async (fromCity, toCity, maxAttractions = 9) => {
  const response = await fetch(
    `/places?fromCity=${encodeURIComponent(fromCity)}&toCity=${encodeURIComponent(toCity)}&max_attractions=${maxAttractions}`
  );
  const data = await response.json();
  return data.success ? data.data.attractions : [];
};
```

### 3. Expected Data Format

**Route Points Response:**
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
  }
}
```

**Attractions Response:**
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
  }
}
```

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

## Working Cities

### ✅ Confirmed Working California Cities

The following **50 California cities** have been tested and confirmed to work with the route API. Users can use any combination of these cities as start/end points:

1. **Apple Valley**
2. **Brea**
3. **Chico**
4. **Chino**
5. **Davis**
6. **Elk Grove**
7. **Fresno**
8. **Hayward**
9. **Indio**
10. **Irvine**
11. **La Habra**
12. **La Mesa**
13. **Lake Forest**
14. **Livermore**
15. **Lodi**
16. **Los Angeles**
17. **Madera**
18. **Merced**
19. **Modesto**
20. **Moreno Valley**
21. **Mountain View**
22. **Napa**
23. **Newport Beach**
24. **Oakland**
25. **Oceanside**
26. **Ontario**
27. **Palo Alto**
28. **Pasadena**
29. **Pittsburg**
30. **Pomona**
31. **Redding**
32. **Redwood City**
33. **Riverside**
34. **Roseville**
35. **Sacramento**
36. **Salinas**
37. **San Bernardino**
38. **San Diego**
39. **San Francisco**
40. **San Jose**
41. **San Leandro**
42. **San Mateo**
43. **San Ramon**
44. **Santa Ana**
45. **Santa Barbara**
46. **Santa Clara**
47. **Stockton**
48. **Tracy**
49. **Turlock**
50. **Union City**

### 🎯 Recommended Testing Combinations

For initial testing and demonstration, use these proven city pairs:

- **Los Angeles → San Francisco** (Major coastal route)
- **San Diego → Sacramento** (North-South route)
- **Fresno → Oakland** (Central to Bay Area)
- **San Jose → Riverside** (Bay Area to Inland Empire)
- **Stockton → San Bernardino** (Central Valley to Inland Empire)

### ⚠️ Important Notes

- **City Names**: Use exact city names as listed above
- **Geocoding**: The system uses free Nominatim geocoding service
- **Timeouts**: Some cities may occasionally timeout due to geocoding service limits
- **Fallback**: If a city fails, try nearby major cities from the list above

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

## Error Handling & Troubleshooting

### Common Issues

1. **City Not Found**: Ensure city names are from the working list above
2. **No Attractions**: Try increasing `max_distance_miles` parameter
3. **API Connection**: Verify backend is running on port 8000
4. **CORS Issues**: Backend includes CORS middleware for frontend access
5. **Map Markers Not Showing**: Check if route-points endpoint is working
6. **Geocoding Timeout**: Try a different city combination from the working list

### Debugging Steps

1. **Check API Health**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test Route Points**:
   ```bash
   curl "http://localhost:8000/route-points?fromCity=Los%20Angeles&toCity=San%20Francisco"
   ```

3. **Test Attractions**:
   ```bash
   curl "http://localhost:8000/places?fromCity=Los%20Angeles&toCity=San%20Francisco"
   ```

4. **Browser Console**: Check for API errors in browser dev tools
5. **Backend Logs**: Check terminal for detailed error messages

### 🔧 Quick Fixes

- **City not working**: Try a different city from the working list above
- **No attractions found**: Increase `max_distance_miles` to 15 or 20
- **API not responding**: Restart the backend server
- **CORS errors**: Verify backend CORS settings are enabled
- **Map not loading**: Check if frontend is connecting to correct API URL

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