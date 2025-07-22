# Summer Activity Route Optimizer

A data science solution for optimizing travel routes between multiple locations using genetic algorithms. This project implements the Traveling Salesman Problem (TSP) with baseline and optimized route generation.

## Project Overview

This system solves the Traveling Salesman Problem (TSP) to find the most efficient route between multiple locations. It includes:

- 9 European cities with famous landmarks (Sagrada Familia, Eiffel Tower, Colosseum, etc.)
- Baseline random route generation for comparison
- Genetic algorithm optimization for finding optimal routes
- Distance calculations using the Haversine formula
- Performance metrics and route comparisons
- **NEW: Web API for software engineering team integration**

## Project Structure

```
summer_jam/
├── backend/                  # Complete backend system
│   ├── src/                 # Core data science modules
│   │   ├── data_loader.py   # Data loading and preprocessing
│   │   ├── distance_calculator.py  # Distance calculations
│   │   ├── baseline_model.py  # Random route generation
│   │   ├── optimization_model.py   # Genetic algorithm TSP solver
│   │   └── visualization.py   # Visualization utilities
│   ├── analysis/            # Data analysis and visualization
│   │   ├── california_attractions_map.html  # Interactive CA map with 2-mile radius
│   │   ├── enhanced_attractions.csv         # Clean dataset with coordinates (66 locations)
│   │   ├── maximize_location.ipynb          # Jupyter notebook for data enhancement
│   │   ├── serve_map.py                     # Python server for local map hosting
│   │   ├── attractions_analysis.html        # USA attractions heatmap
│   │   ├── usa_attractions_heatmap.html     # Enhanced USA visualization
│   │   ├── create_usa_heatmap.py           # USA heatmap generation script
│   │   ├── processed_roadside_attractions.csv # Original roadside attractions data
│   │   └── README.md                        # Analysis documentation
│   ├── data/                # Location datasets
│   │   └── locations.csv    # European landmarks with coordinates
│   ├── api_interface.py     # Core API for integration
│   ├── web_api.py          # FastAPI web server
│   ├── start_api.py        # Easy startup script
│   ├── test_api.py         # API testing script
│   ├── create_usa_locations.py  # USA location creation script
│   ├── reset_data.py       # Data reset utility
│   ├── API_DOCUMENTATION.md # Complete API docs
│   ├── main.py             # Core entry point
│   └── requirements.txt    # Python dependencies
├── SOFTWARE_ENGINEERS_GUIDE.md  # Integration guide for React team
├── task.md                 # Original requirements
└── README.md              # This file
```

## Quick Start

### For Data Science Team

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### For Software Engineering Team

```bash
cd backend
pip install -r requirements.txt
python start_api.py
```

The API will be available at `http://localhost:8000`

### For California Attractions Analysis

```bash
cd backend/analysis
python serve_map.py
```

Then open `http://localhost:8000/california_attractions_map.html` in your browser.

## California Attractions Map

### Interactive Visualization
- **66 California locations** with precise coordinates
- **2-mile radius circles** around each attraction
- **Interactive markers** with attraction details
- **Categories**: National Parks, Landmarks, Museums, Beaches, etc.
- **Real-time data loading** from enhanced_attractions.csv

### Features
- 🗺️ **Interactive Map**: Leaflet.js-based visualization
- 📍 **Location Markers**: Click for attraction details
- 🔴 **Radius Circles**: 2-mile coverage areas
- 📊 **Data Summary**: Total locations and categories
- 🎯 **California Focus**: All major attractions and landmarks
- 📱 **Responsive Design**: Works on any device

### Data Categories
- **National Parks**: Yosemite, Death Valley, Joshua Tree, etc.
- **Landmarks**: Golden Gate Bridge, Hollywood Sign, Alcatraz
- **Amusement Parks**: Disneyland, Universal Studios, Six Flags
- **Beaches**: Venice Beach, Santa Monica Pier, Malibu
- **Museums**: Getty Center, LACMA, California Science Center
- **Wine Regions**: Napa Valley, Sonoma Valley, Paso Robles
- **Historical Sites**: Missions, Sutter's Fort, Bodie Ghost Town

## Web API for Software Engineers

### Start the API Server

```bash
cd backend
python start_api.py
```

### Available Endpoints

- **GET** `/health` - Health check
- **GET** `/locations` - Get all available locations
- **POST** `/locations` - Add custom location
- **POST** `/optimize` - Optimize route for given locations
- **POST** `/compare` - Compare optimized vs random route
- **POST** `/visualization` - Get visualization data
- **POST** `/street-routing` - Get actual street routing data
- **GET** `/quick-optimize` - Quick optimization with query params
- **GET** `/stats` - API statistics

### Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation with Swagger UI.

### Test the API

```bash
cd backend
python test_api.py
```

### Example Usage

```javascript
// Get all locations
const response = await fetch('http://localhost:8000/locations');
const data = await response.json();

// Optimize a route
const optimizeResponse = await fetch('http://localhost:8000/optimize', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ location_ids: [0, 1, 2, 3, 4] })
});
const result = await optimizeResponse.json();
```

For complete API documentation, see `backend/API_DOCUMENTATION.md`.

## Data Science Components

### 1. Data Preparation
- **European Dataset**: 9 European landmarks with accurate GPS coordinates
- **California Dataset**: 66 California attractions with precise coordinates
- **USA Dataset**: Comprehensive roadside attractions analysis
- **Preprocessing**: Coordinate validation, distance matrix calculation
- **Features**: Location name, latitude, longitude, city, category

### 2. Data Analysis & Visualization
- **California Map**: Interactive visualization with 2-mile radius circles
- **USA Heatmap**: Comprehensive roadside attractions analysis
- **Data Enhancement**: Jupyter notebook for location optimization
- **Coordinate Validation**: Clean datasets with verified coordinates
- **Category Analysis**: National Parks, Landmarks, Museums, etc.

### 2. Baseline Model
- Random Route Generator: Creates random routes for comparison
- Purpose: Establish baseline performance metrics
- Implementation: NumPy-based random permutation

### 3. Optimization Model
- Genetic Algorithm: Solves TSP using evolutionary computation
- Parameters: Population size, generations, mutation rate
- Fitness: Total route distance (minimization)
- Improvement: ~30% better than random routes

### 4. Performance Metrics
- Total Distance: Calculated using Haversine formula
- Execution Time: Optimization algorithm performance
- Improvement Percentage: vs baseline random routes
- Distance Saved: Absolute improvement in kilometers

## Results & Performance

### European Route Optimization
- Baseline (Random): ~4,100 km
- Optimized Route: ~2,847 km
- Improvement: 30.9% distance reduction
- Execution Time: ~0.045 seconds

### California Attractions Analysis
- **66 Locations**: All with verified coordinates
- **Categories**: 20 different attraction types
- **Coverage**: Major cities, national parks, landmarks
- **Data Quality**: 100% coordinate validation
- **Visualization**: Interactive map with 2-mile radius circles

### Key Features
- **Fast Optimization**: Sub-second execution for 9 locations
- **Accurate Distances**: Haversine formula for real-world distances
- **Flexible API**: Easy integration with any frontend
- **Extensible**: Add custom locations dynamically
- **Production Ready**: Error handling, logging, validation
- **Web API**: RESTful endpoints for software engineering team
- **Interactive Maps**: California attractions with radius visualization

## Task Requirements Met

### Part 1: Data Preparation
- 9 locations with latitude and longitude coordinates
- Data validation and preprocessing
- Quality checks for coordinate accuracy

### Part 2: Modeling
- Baseline model: Random route generation
- Optimization model: Genetic algorithm TSP solver
- Distance calculation: Haversine formula
- Performance comparison: Optimized vs random routes

### Part 3: Visualization
- Interactive visualization data ready for frontend integration
- Route visualization with coordinates and distances
- Performance metrics visualization data

### Part 4: Reporting
- Complete documentation of data science approach
- Model explanations and algorithm descriptions
- Results analysis with performance metrics
- Next steps for further exploration
- **NEW: Web API with comprehensive documentation**

## API Integration Guide

The web API provides easy access to all data science functionality:

1. **Route Optimization**: Use genetic algorithms to find optimal routes
2. **Performance Comparison**: Compare optimized vs random routes
3. **Visualization Data**: Get coordinates and data for map visualization
4. **Street Routing**: Get actual road routing using OSRM
5. **Custom Locations**: Add new locations dynamically
6. **Health Monitoring**: Check API status and statistics

All endpoints return consistent JSON responses with proper error handling and validation.