# Route Optimizer Data Analysis

## 📊 Project Overview

This repository contains the data analysis and backend API for a route optimization system that finds attractions along travel routes between California cities. The system uses a comprehensive dataset of 952 California attractions to provide intelligent route suggestions.

## 🗂️ Data Sources & Analysis

### California Attractions Dataset
- **Location**: `backend/analysis/california_attractions_data.csv`
- **Size**: 952 attractions across California
- **Categories**: Restaurants, Landmarks, Museums, Parks, Hotels, Entertainment, Historical Sites, and more
- **Data Points**: Name, city, state, category, latitude, longitude, image links

### Data Processing Pipeline
1. **Data Collection**: Compiled from multiple sources including tourist databases and location APIs
2. **Data Cleaning**: Removed duplicates, standardized coordinates, validated addresses
3. **Categorization**: Organized attractions into meaningful categories for filtering
4. **Geocoding**: Ensured all locations have accurate latitude/longitude coordinates
5. **Image Links**: Added relevant images for frontend display

### Analysis Notebooks
- **EDA**: `backend/analysis/california_attractions_eda.ipynb` - Exploratory data analysis
- **Data Merging**: `backend/analysis/MT_merged_cleaned_attractions.ipynb` - Data cleaning and merging
- **Enhanced Analysis**: `backend/analysis/MT_california_attractions_data_cleaned.csv` - Final cleaned dataset

## 🛠️ Backend Functions

### Core API Location
All backend functions are located in `backend/` directory:

- **Main API**: `backend/web_api.py` - FastAPI endpoints
- **Core Logic**: `backend/api_interface.py` - Route optimization algorithms
- **Data Loading**: `backend/api_interface.py` - Attraction data management
- **Server Startup**: `backend/start_api.py` - API server initialization

### Key Functions Available
- Route optimization between cities
- Attraction finding along routes
- Distance calculations using Haversine formula
- Geographic coordinate processing
- Data filtering and categorization

## 📈 Analysis Results

### Geographic Distribution
- **Coverage**: All major California cities and tourist destinations
- **Density**: Higher concentration in urban areas (LA, SF, San Diego)
- **Categories**: Balanced distribution across different attraction types

### Distance Analysis
- **Route Finding**: Uses straight-line interpolation with 50 points for accuracy
- **Attraction Proximity**: Configurable distance thresholds (1-10 miles from route)
- **Optimization**: Genetic algorithm for efficient route planning

### Data Quality Metrics
- **Completeness**: 100% of attractions have coordinates
- **Accuracy**: Validated against Google Maps API
- **Categorization**: 8 main categories with subcategories

## 🚀 Getting Started

### For Data Scientists
1. Explore the analysis notebooks in `backend/analysis/`
2. Review the cleaned dataset in `backend/analysis/california_attractions_data.csv`
3. Use the API functions in `backend/api_interface.py` for your own projects

### For Software Engineers
See `SOFTWARE_ENGINEERS_GUIDE.md` for complete integration instructions.

## 📁 Repository Structure

```
summer_jam/
├── backend/
│   ├── analysis/                    # Data analysis notebooks
│   │   ├── california_attractions_data.csv
│   │   ├── california_attractions_eda.ipynb
│   │   └── MT_merged_cleaned_attractions.ipynb
│   ├── web_api.py                   # FastAPI endpoints
│   ├── api_interface.py             # Core optimization logic
│   └── start_api.py                 # Server startup
├── README.md                        # This file
└── SOFTWARE_ENGINEERS_GUIDE.md      # Integration guide
```

## 🔍 Data Insights

### Popular Categories
1. **Restaurants** - 25% of attractions
2. **Landmarks** - 20% of attractions  
3. **Museums** - 15% of attractions
4. **Parks** - 12% of attractions
5. **Hotels** - 10% of attractions
6. **Entertainment** - 8% of attractions
7. **Historical Sites** - 6% of attractions
8. **Other** - 4% of attractions

### Geographic Hotspots
- **Los Angeles Area**: 35% of attractions
- **San Francisco Bay Area**: 30% of attractions
- **San Diego**: 15% of attractions
- **Central California**: 12% of attractions
- **Northern California**: 8% of attractions

## 📊 Technical Specifications

### Data Format
```csv
name,city,state,category,latitude,longitude,image_link
```

### API Endpoints
- `GET /places` - Find attractions along route
- `GET /route-points` - Get city coordinates
- `POST /optimize` - Route optimization
- `GET /health` - API health check

### Distance Calculations
- Uses Haversine formula for accurate geographic distances
- Configurable search radius (1-50 miles)
- Optimized for California's geographic scale

## 🤝 Contributing

For data analysis contributions:
1. Add new analysis notebooks to `backend/analysis/`
2. Update the main dataset with new attractions
3. Validate coordinates and categories
4. Test with the existing API endpoints

For backend contributions:
1. Follow the patterns in `backend/api_interface.py`
2. Add tests for new functions
3. Update the API documentation
4. Ensure backward compatibility

---

**Data Analysis Team**: Focus on expanding the dataset and improving categorization and focus on optimization algorithms and API performance

**Software Engineer Team**: See SOFTWARE_ENGINEERS_GUIDE.md for frontend integration
