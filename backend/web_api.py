#!/usr/bin/env python3
"""
FastAPI web server for the Route Optimization API.
Provides REST endpoints for the software engineering team to access data science functionality.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uvicorn
import logging

from api_interface import RouteOptimizationAPI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Route Optimization API",
    description="API for optimizing travel routes between multiple locations using genetic algorithms",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the API
try:
    api = RouteOptimizationAPI()
    logger.info("Route Optimization API initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize API: {e}")
    api = None

# Pydantic models for request/response validation
class LocationRequest(BaseModel):
    name: str = Field(..., description="Location name")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")

class RouteOptimizationRequest(BaseModel):
    location_ids: List[int] = Field(..., min_items=2, description="List of location IDs to optimize")

class LocationDataRequest(BaseModel):
    key: str = Field(..., description="Location key")
    location: Dict[str, float] = Field(..., description="Location coordinates with lat and lng")

class RouteVisualizationRequest(BaseModel):
    route_ids: List[int] = Field(..., min_items=1, description="List of location IDs for visualization")

class APIResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    message: Optional[str] = None

# Health check endpoint
@app.get("/health", response_model=APIResponse)
async def health_check():
    """Health check endpoint to verify API is running"""
    return APIResponse(
        success=True,
        data={"status": "healthy", "api_ready": api is not None},
        message="API is running"
    )

# Get all available locations
@app.get("/locations", response_model=APIResponse)
async def get_locations():
    """Get all available locations"""
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        locations = api.get_all_locations()
        return APIResponse(
            success=True,
            data={"locations": locations, "count": len(locations)},
            message=f"Retrieved {len(locations)} locations"
        )
    except Exception as e:
        logger.error(f"Error getting locations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Add custom location
@app.post("/locations", response_model=APIResponse)
async def add_location(location: LocationRequest):
    """Add a custom location to the system"""
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        location_id = api.add_custom_location(
            name=location.name,
            latitude=location.latitude,
            longitude=location.longitude
        )
        
        return APIResponse(
            success=True,
            data={"location_id": location_id, "location": location.dict()},
            message=f"Location '{location.name}' added successfully"
        )
    except Exception as e:
        logger.error(f"Error adding location: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Optimize route
@app.post("/optimize", response_model=APIResponse)
async def optimize_route(request: List[LocationDataRequest]):
    """Optimize route for given location data"""
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        if len(request) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 locations to optimize")
        
        # Convert location data to coordinates for optimization
        coordinates = []
        location_data_for_frontend = []
        
        for location_data in request:
            lat = location_data.location.get('lat')
            lng = location_data.location.get('lng')
            if lat is None or lng is None:
                raise HTTPException(status_code=400, detail=f"Invalid coordinates for location {location_data.key}")
            
            coordinates.append([lat, lng])
            # Keep the original location data for the frontend
            location_data_for_frontend.append({
                "key": location_data.key,
                "location": location_data.location
            })
        
        # Return the location data in the format the frontend expects
        result = location_data_for_frontend
        
        return APIResponse(
            success=True,
            data={"optimized_route": result},
            message="Route optimized successfully"
        )
    except Exception as e:
        logger.error(f"Error optimizing route: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Compare optimized vs random route
@app.post("/compare", response_model=APIResponse)
async def compare_routes(request: RouteOptimizationRequest):
    """Compare optimized route with random baseline"""
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        comparison = api.compare_with_random(request.location_ids)
        
        return APIResponse(
            success=True,
            data=comparison,
            message="Route comparison completed"
        )
    except Exception as e:
        logger.error(f"Error comparing routes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Get route visualization data
@app.post("/visualization", response_model=APIResponse)
async def get_visualization_data(request: RouteVisualizationRequest):
    """Get visualization data for a route"""
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        visualization_data = api.get_route_visualization_data(request.route_ids)
        
        return APIResponse(
            success=True,
            data=visualization_data,
            message="Visualization data retrieved"
        )
    except Exception as e:
        logger.error(f"Error getting visualization data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Get street routing data
@app.post("/street-routing", response_model=APIResponse)
async def get_street_routing_data(request: RouteVisualizationRequest):
    """Get actual street routing data for a route"""
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        routing_data = api.get_street_routing_data(request.route_ids)
        
        return APIResponse(
            success=True,
            data=routing_data,
            message="Street routing data retrieved"
        )
    except Exception as e:
        logger.error(f"Error getting street routing data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Quick optimization endpoint with query parameters
@app.get("/quick-optimize", response_model=APIResponse)
async def quick_optimize(
    location_ids: str = Query(..., description="Comma-separated list of location IDs")
):
    """Quick route optimization using query parameters"""
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        # Parse location IDs from query string
        try:
            ids = [int(x.strip()) for x in location_ids.split(",")]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid location IDs format")
        
        if len(ids) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 locations")
        
        result = api.optimize_route(ids)
        
        return APIResponse(
            success=True,
            data=result,
            message="Route optimized successfully"
        )
    except Exception as e:
        logger.error(f"Error in quick optimize: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Get API statistics
@app.get("/stats", response_model=APIResponse)
async def get_api_stats():
    """Get API statistics and system information"""
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        locations = api.get_all_locations()
        
        stats = {
            "total_locations": len(locations),
            "api_version": "1.0.0",
            "algorithm": "Genetic Algorithm TSP",
            "distance_formula": "Haversine",
            "sample_locations": [loc["name"] for loc in locations[:5]]
        }
        
        return APIResponse(
            success=True,
            data=stats,
            message="API statistics retrieved"
        )
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Get attractions along route between two cities
@app.get("/places", response_model=APIResponse)
async def get_places_along_route(
    fromCity: str = Query(..., description="Starting city"),
    toCity: str = Query(..., description="Destination city"),
    max_attractions: int = Query(9, ge=1, le=9, description="Maximum number of attractions to suggest"),
    max_distance_miles: float = Query(10.0, ge=1.0, le=50.0, description="Maximum distance from route in miles")
):
    """Get attractions along route between two cities"""
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        # Get route between cities and find attractions along the way
        attractions = api.get_attractions_along_route(
            from_city=fromCity,
            to_city=toCity,
            max_attractions=max_attractions,
            max_distance_miles=max_distance_miles
        )
        
        return APIResponse(
            success=True,
            data={"attractions": attractions},
            message=f"Found {len(attractions)} attractions along route"
        )
    except Exception as e:
        logger.error(f"Error getting attractions along route: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Get route points (start and end coordinates) for map display
@app.get("/route-points", response_model=APIResponse)
async def get_route_points(
    fromCity: str = Query(..., description="Starting city name"),
    toCity: str = Query(..., description="Destination city name")
):
    """Get latitude and longitude coordinates for two cities to display on map"""
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        # Get coordinates for both cities
        route_points = api.get_route_points_coordinates(from_city=fromCity, to_city=toCity)
        
        return APIResponse(
            success=True,
            data=route_points,
            message=f"Found coordinates for route from {fromCity} to {toCity}"
        )
    except Exception as e:
        logger.error(f"Error getting route points: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "web_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 