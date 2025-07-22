#!/usr/bin/env python3
"""
Simple Web Route Visualizer
A web-based route visualizer with search bars and interactive map
"""

import folium
import webbrowser
import tempfile
import requests
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time
import os

class WebRouteVisualizer:
    def __init__(self):
        self.api_url = "http://localhost:8000"
        self.port = 8080
        self.map_file = None
        
    def create_html_interface(self):
        """Create the HTML interface"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🗺️ Route Visualizer</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: bold;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        .search-section {
            padding: 30px;
            background: #f8f9fa;
        }
        .search-row {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            align-items: center;
        }
        .search-group {
            flex: 1;
        }
        .search-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #2c3e50;
            font-size: 1.1em;
        }
        .search-group input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
            box-sizing: border-box;
        }
        .search-group input:focus {
            outline: none;
            border-color: #3498db;
        }
        .search-button {
            background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
            margin-top: 25px;
        }
        .search-button:hover {
            transform: translateY(-2px);
        }
        .status {
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
        }
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .status.loading {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .map-container {
            padding: 20px;
            text-align: center;
        }
        .map-frame {
            width: 100%;
            height: 500px;
            border: none;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .instructions {
            background: #e8f5e8;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            border-left: 4px solid #4caf50;
        }
        .instructions h3 {
            margin: 0 0 10px 0;
            color: #2c3e50;
        }
        .instructions ul {
            margin: 0;
            padding-left: 20px;
        }
        .instructions li {
            margin: 5px 0;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗺️ Route Visualizer</h1>
            <p>Enter start and end cities to see the route with attractions</p>
        </div>
        
        <div class="search-section">
            <div class="search-row">
                <div class="search-group">
                    <label for="startCity">Start City:</label>
                    <input type="text" id="startCity" placeholder="e.g., Los Angeles" value="Los Angeles">
                </div>
                <div class="search-group">
                    <label for="endCity">End City:</label>
                    <input type="text" id="endCity" placeholder="e.g., San Francisco" value="San Francisco">
                </div>
            </div>
            
            <button class="search-button" onclick="findRoute()">🔍 Find Route</button>
            
            <div id="status" class="status" style="display: none;"></div>
            
            <div class="instructions">
                <h3>📋 How to Use:</h3>
                <ul>
                    <li>Enter start and end cities in the search bars above</li>
                    <li>Click "Find Route" or press Enter</li>
                    <li>An interactive map will open showing the route</li>
                    <li>Blue marker = Start city, Red marker = End city</li>
                    <li>Green stars = Attractions along the route</li>
                    <li>Click markers to see details and distances</li>
                </ul>
            </div>
        </div>
        
        <div class="map-container">
            <iframe id="mapFrame" class="map-frame" src="about:blank"></iframe>
        </div>
    </div>

    <script>
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + type;
            status.style.display = 'block';
        }
        
        function findRoute() {
            const startCity = document.getElementById('startCity').value.trim();
            const endCity = document.getElementById('endCity').value.trim();
            
            if (!startCity || !endCity) {
                showStatus('Please enter both start and end cities', 'error');
                return;
            }
            
            showStatus('Finding route...', 'loading');
            
            // Make API call to get route data
            fetch(`http://localhost:8000/route-points?fromCity=${encodeURIComponent(startCity)}&toCity=${encodeURIComponent(endCity)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Get attractions
                        return fetch(`http://localhost:8000/places?fromCity=${encodeURIComponent(startCity)}&toCity=${encodeURIComponent(endCity)}&max_attractions=5`);
                    } else {
                        throw new Error(data.message || 'Could not find route');
                    }
                })
                .then(response => response.json())
                .then(attractionData => {
                    // Create map URL
                    const mapUrl = `http://localhost:8080/map.html?start=${encodeURIComponent(startCity)}&end=${encodeURIComponent(endCity)}`;
                    document.getElementById('mapFrame').src = mapUrl;
                    showStatus('✅ Route found! Map loaded below', 'success');
                })
                .catch(error => {
                    showStatus('❌ Error: ' + error.message, 'error');
                });
        }
        
        // Allow Enter key to trigger search
        document.getElementById('startCity').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') findRoute();
        });
        document.getElementById('endCity').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') findRoute();
        });
    </script>
</body>
</html>
        """
        
        # Save HTML interface
        with open('interface.html', 'w') as f:
            f.write(html_content)
    
    def create_map_page(self):
        """Create the map page that will be embedded"""
        map_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Route Map</title>
    <style>
        body { margin: 0; padding: 0; }
        #map { width: 100%; height: 100vh; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        // Get URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        const startCity = urlParams.get('start');
        const endCity = urlParams.get('end');
        
        if (startCity && endCity) {
            // Create map using Leaflet (free alternative to Google Maps)
            const map = L.map('map').setView([37.7749, -122.4194], 8);
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);
            
            // Get route data and create markers
            fetch(`http://localhost:8000/route-points?fromCity=${encodeURIComponent(startCity)}&toCity=${encodeURIComponent(endCity)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const start = data.data.start;
                        const end = data.data.end;
                        
                        // Add markers
                        L.marker([start.lat, start.lng], {color: 'blue'})
                            .addTo(map)
                            .bindPopup(`<b>Start: ${start.city}</b>`);
                            
                        L.marker([end.lat, end.lng], {color: 'red'})
                            .addTo(map)
                            .bindPopup(`<b>End: ${end.city}</b>`);
                            
                        // Add route line
                        L.polyline([[start.lat, start.lng], [end.lat, end.lng]], {
                            color: 'blue',
                            weight: 3,
                            opacity: 0.8
                        }).addTo(map);
                        
                        // Fit map to show both points
                        map.fitBounds([[start.lat, start.lng], [end.lat, end.lng]]);
                    }
                });
        }
    </script>
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
</body>
</html>
        """
        
        with open('map.html', 'w') as f:
            f.write(map_html)
    
    def start_server(self):
        """Start the web server"""
        os.chdir('.')
        server = HTTPServer(('localhost', self.port), SimpleHTTPRequestHandler)
        print(f"🌐 Web server started at http://localhost:{self.port}")
        print(f"📱 Open your browser and go to: http://localhost:{self.port}/interface.html")
        print()
        server.serve_forever()
    
    def run(self):
        """Run the web visualizer"""
        print("🗺️ Starting Web Route Visualizer...")
        print("Make sure your backend API is running at http://localhost:8000")
        print()
        
        # Create HTML files
        self.create_html_interface()
        self.create_map_page()
        
        # Start server
        self.start_server()

def main():
    """Main function"""
    visualizer = WebRouteVisualizer()
    visualizer.run()

if __name__ == "__main__":
    main() 