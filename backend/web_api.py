#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uvicorn
import logging
import pandas as pd

from api_interface import RouteOptimizationAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Route Optimization API",
    description="API for optimizing travel routes between multiple locations using genetic algorithms",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    api = RouteOptimizationAPI()
    logger.info("Route Optimization API initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize API: {e}")
    api = None

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

@app.get("/health", response_model=APIResponse)
async def health_check():
    return APIResponse(
        success=True,
        data={"status": "healthy", "api_ready": api is not None},
        message="API is running"
    )

@app.get("/locations", response_model=APIResponse)
async def get_locations():
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

@app.post("/locations", response_model=APIResponse)
async def add_location(location: LocationRequest):
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

@app.post("/optimize", response_model=APIResponse)
async def optimize_route(request: List[LocationDataRequest]):
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        if len(request) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 locations to optimize")
        
        coordinates = []
        location_data_for_frontend = []
        
        for location_data in request:
            lat = location_data.location.get('lat')
            lng = location_data.location.get('lng')
            if lat is None or lng is None:
                raise HTTPException(status_code=400, detail=f"Invalid coordinates for location {location_data.key}")
            
            coordinates.append([lat, lng])
            location_data_for_frontend.append({
                "key": location_data.key,
                "location": location_data.location
            })
        
        temp_location_ids = list(range(len(coordinates)))
        optimized_result = api.optimize_route(temp_location_ids)
        
        optimized_route = []
        for optimized_id in optimized_result['optimized_route']['location_ids']:
            if optimized_id < len(location_data_for_frontend):
                optimized_route.append(location_data_for_frontend[optimized_id])
        
        return APIResponse(
            success=True,
            data={"optimized_route": optimized_route},
            message="Route optimized successfully"
        )
    except Exception as e:
        logger.error(f"Error optimizing route: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare", response_model=APIResponse)
async def compare_routes(request: RouteOptimizationRequest):
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

@app.post("/visualization", response_model=APIResponse)
async def get_visualization_data(request: RouteVisualizationRequest):
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

@app.post("/street-routing", response_model=APIResponse)
async def get_street_routing_data(request: RouteVisualizationRequest):
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

@app.post("/quick-optimize")
async def quick_optimize(
    location_ids: List[str] = Body(..., embed=True, description="List of location IDs to optimize")
):
    print("location_ids:", location_ids)
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        try:
            result = []
            df = pd.read_csv("analysis/california_attractions_data.csv")
            for location in location_ids:
                record = df[df["name"] == location]
                if record.empty:
                    pass
                loc = {"key": record["name"].values[0]
                        , "location": {"lat": record["latitude"].values[0], "lng": record["longitude"].values[0]}}
                result.append(loc)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid location IDs format")
        
        return result
    except Exception as e:
        logger.error(f"Error in quick optimize: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats", response_model=APIResponse)
async def get_api_stats():
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

@app.get("/places", response_model=APIResponse)
async def get_places_along_route(
    fromCity: str = Query(..., description="Starting city"),
    toCity: str = Query(..., description="Destination city"),
    max_attractions: int = Query(9, ge=1, le=9, description="Maximum number of attractions to suggest"),
    max_distance_miles: float = Query(10.0, ge=1.0, le=50.0, description="Maximum distance from route in miles")
):
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
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

@app.get("/route-points", response_model=APIResponse)
async def get_route_points(
    fromCity: str = Query(..., description="Starting city name"),
    toCity: str = Query(..., description="Destination city name")
):
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        route_points = api.get_route_points_coordinates(from_city=fromCity, to_city=toCity)
        
        return APIResponse(
            success=True,
            data=route_points,
            message=f"Found coordinates for route from {fromCity} to {toCity}"
        )
    except Exception as e:
        logger.error(f"Error getting route points: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize-with-directions", response_model=APIResponse)
async def optimize_with_directions(request: List[LocationDataRequest]):
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        if len(request) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 locations to optimize")
        
        coordinates = []
        location_data_for_frontend = []
        
        for location_data in request:
            lat = location_data.location.get('lat')
            lng = location_data.location.get('lng')
            if lat is None or lng is None:
                raise HTTPException(status_code=400, detail=f"Invalid coordinates for location {location_data.key}")
            
            coordinates.append([lat, lng])
            location_data_for_frontend.append({
                "key": location_data.key,
                "location": location_data.location
            })
        
        temp_location_ids = list(range(len(coordinates)))
        optimized_result = api.optimize_route(temp_location_ids)
        
        optimized_route = []
        for optimized_id in optimized_result['optimized_route']['location_ids']:
            if optimized_id < len(location_data_for_frontend):
                optimized_route.append(location_data_for_frontend[optimized_id])
        
        directions_data = api.get_street_directions(optimized_route)
        
        return APIResponse(
            success=True,
            data={
                "optimized_route": optimized_route,
                "directions": directions_data
            },
            message="Route optimized with street directions"
        )
    except Exception as e:
        logger.error(f"Error optimizing route with directions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/optimize-with-routing", response_model=APIResponse)
async def optimize_route_with_routing(request: List[LocationDataRequest]):
    try:
        if not api:
            raise HTTPException(status_code=503, detail="API not initialized")
        
        if len(request) < 2:
            raise HTTPException(status_code=400, detail="Need at least 2 locations to optimize")
        
        coordinates = []
        location_data_for_frontend = []
        
        for location_data in request:
            lat = location_data.location.get('lat')
            lng = location_data.location.get('lng')
            if lat is None or lng is None:
                raise HTTPException(status_code=400, detail=f"Invalid coordinates for location {location_data.key}")
            
            coordinates.append([lat, lng])
            location_data_for_frontend.append({
                "key": location_data.key,
                "location": location_data.location
            })
        
        temp_location_ids = list(range(len(coordinates)))
        optimized_result = api.optimize_route(temp_location_ids)
        
        optimized_route = []
        for optimized_id in optimized_result['optimized_route']['location_ids']:
            if optimized_id < len(location_data_for_frontend):
                optimized_route.append(location_data_for_frontend[optimized_id])
        
        optimized_ids = optimized_result['optimized_route']['location_ids']
        routing_data = api.get_street_routing_data(optimized_ids)
        
        result = {
            "optimized_route": optimized_route,
            "routing_data": routing_data,
            "total_distance": optimized_result['optimized_route']['total_distance']
        }
        
        return APIResponse(
            success=True,
            data=result,
            message="Route optimized with street routing data"
        )
    except Exception as e:
        logger.error(f"Error optimizing route with routing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "web_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 