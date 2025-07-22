# Route Optimizer with Attractions

## 🎯 Project Overview

This project integrates a data science backend with a React frontend to create a route optimization system that suggests attractions along travel routes.

## 🚀 Quick Start

### 1. Start the Backend
```bash
cd backend
pip install -r requirements.txt
python3 start_api.py
```

### 2. Start the Frontend
```bash
cd route_optimizer_fe
npm install
npm run dev
```

### 3. Test the Integration
1. Open the frontend in your browser
2. Enter "Los Angeles" as starting city
3. Enter "San Francisco" as destination city
4. Click search to see attractions along the route
5. Select attractions by clicking heart buttons
6. Click "Make Route" to optimize and visualize

## 🔗 Key Features

- **Route Search**: Find attractions along routes between California cities
- **Smart Filtering**: Different distance rules for different attraction categories
- **Route Optimization**: Genetic algorithm optimization for selected attractions
- **Google Maps Integration**: Visualize optimized routes on interactive maps
- **952 California Attractions**: Comprehensive dataset of tourist destinations

## 📊 Distance Rules

- **"Other" category**: Must be within 1 mile of the road
- **All other categories**: Can be up to 10 miles from the path
- **Maximum attractions**: 9 per route

## 🎮 User Flow

1. User enters start and destination cities
2. System finds attractions along the route
3. User selects attractions by clicking heart buttons
4. System optimizes the route using genetic algorithms
5. Optimized route is displayed on Google Maps

## 📚 Documentation

- **Setup Guide**: [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed integration instructions
- **API Documentation**: http://localhost:8000/docs - Interactive API docs
- **Frontend Integration**: [route_optimizer_fe/README.md](route_optimizer_fe/README.md)

## 🛠️ Technical Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Pandas**: Data processing for attractions
- **Geopy**: Geographic calculations
- **NumPy**: Numerical computations

### Frontend
- **React**: User interface
- **Google Maps API**: Route visualization
- **Vite**: Build tool and dev server

## 📁 Project Structure

```
summer_jam/
├── backend/                    # Data science backend
│   ├── start_api.py           # API server
│   ├── web_api.py             # FastAPI endpoints
│   ├── api_interface.py       # Core logic
│   └── analysis/california_attractions_data.csv
├── route_optimizer_fe/        # React frontend
│   └── src/components/utils/constants.js
├── SETUP_GUIDE.md            # Detailed setup instructions
└── README.md                 # This file
```

## 🧪 Testing

### API Testing
```bash
cd backend
python3 test_api.py
```

### Manual Testing
1. Start both servers
2. Test route search functionality
3. Verify attraction selection
4. Check route optimization
5. Confirm Google Maps visualization

## 🐛 Troubleshooting

### Common Issues
- **API not starting**: Check if port 8000 is available
- **Frontend connection**: Verify backend is running
- **No attractions**: Try different California cities
- **CORS errors**: Backend includes CORS middleware

### Debug Endpoints
- Health: `GET /health`
- All locations: `GET /locations`
- API stats: `GET /stats`

## 🎉 Success Criteria

The integration is working when:
- ✅ Backend API is running on port 8000
- ✅ Frontend can connect to backend
- ✅ Route search returns attractions
- ✅ Attraction selection works
- ✅ Route optimization functions
- ✅ Google Maps visualization displays

## 📞 Support

For technical issues:
1. Check the [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
2. Review API documentation at http://localhost:8000/docs
3. Test individual components using the test scripts
4. Check browser console and backend logs for errors

---

**Ready to use!** 🚀 The software engineers can now integrate their frontend with your data science backend for route optimization with attractions.