#!/usr/bin/env python3
"""
Simple Route Visualizer
A quick Python app with search bars and interactive map visualization
"""

import tkinter as tk
from tkinter import ttk, messagebox
import folium
import webbrowser
import tempfile
import os
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
import json

class RouteVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Route Visualizer")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')
        
        # API URL
        self.api_url = "http://localhost:8000"
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="🗺️ Route Visualizer", 
            font=("Arial", 20, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Enter start and end cities to see the route",
            font=("Arial", 12),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        subtitle_label.pack(pady=5)
        
        # Search frame
        search_frame = tk.Frame(self.root, bg='#f0f0f0')
        search_frame.pack(pady=30)
        
        # Start city
        start_label = tk.Label(
            search_frame,
            text="Start City:",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        start_label.grid(row=0, column=0, padx=(0, 10), pady=10)
        
        self.start_entry = tk.Entry(
            search_frame,
            font=("Arial", 12),
            width=20,
            relief="solid",
            bd=1
        )
        self.start_entry.grid(row=0, column=1, padx=(0, 20), pady=10)
        self.start_entry.bind('<Return>', self.on_enter)
        
        # End city
        end_label = tk.Label(
            search_frame,
            text="End City:",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        end_label.grid(row=0, column=2, padx=(0, 10), pady=10)
        
        self.end_entry = tk.Entry(
            search_frame,
            font=("Arial", 12),
            width=20,
            relief="solid",
            bd=1
        )
        self.end_entry.grid(row=0, column=3, padx=(0, 0), pady=10)
        self.end_entry.bind('<Return>', self.on_enter)
        
        # Search button
        search_button = tk.Button(
            self.root,
            text="🔍 Find Route",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            relief="flat",
            padx=20,
            pady=10,
            command=self.find_route
        )
        search_button.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready to search...",
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.status_label.pack(pady=10)
        
        # Results frame
        self.results_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.results_frame.pack(pady=10, fill='both', expand=True)
        
    def on_enter(self, event):
        """Handle Enter key press"""
        self.find_route()
        
    def find_route(self):
        """Find route between cities"""
        start_city = self.start_entry.get().strip()
        end_city = self.end_entry.get().strip()
        
        if not start_city or not end_city:
            messagebox.showerror("Error", "Please enter both start and end cities")
            return
            
        self.status_label.config(text="Finding route...")
        self.root.update()
        
        try:
            # Get route points from API
            route_data = self.get_route_points(start_city, end_city)
            if route_data:
                # Get attractions along route
                attractions = self.get_attractions(start_city, end_city)
                
                # Create map
                self.create_map(route_data, attractions)
                
                self.status_label.config(text=f"✅ Route found! Map opened in browser")
            else:
                self.status_label.config(text="❌ Could not find route")
                
        except Exception as e:
            self.status_label.config(text=f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Could not find route: {str(e)}")
    
    def get_route_points(self, start_city, end_city):
        """Get route points from API"""
        try:
            url = f"{self.api_url}/route-points"
            params = {
                'fromCity': start_city,
                'toCity': end_city
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('success'):
                return data['data']
            else:
                raise Exception(data.get('message', 'Unknown error'))
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"API connection failed: {str(e)}")
    
    def get_attractions(self, start_city, end_city):
        """Get attractions along route"""
        try:
            url = f"{self.api_url}/places"
            params = {
                'fromCity': start_city,
                'toCity': end_city,
                'max_attractions': 5
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get('success'):
                return data['data']['attractions']
            else:
                return []
                
        except:
            return []
    
    def create_map(self, route_data, attractions):
        """Create interactive map with route and attractions"""
        try:
            # Get coordinates
            start_lat = route_data['start']['lat']
            start_lng = route_data['start']['lng']
            end_lat = route_data['end']['lat']
            end_lng = route_data['end']['lng']
            
            # Calculate center
            center_lat = (start_lat + end_lat) / 2
            center_lng = (start_lng + end_lng) / 2
            
            # Create map
            m = folium.Map(
                location=[center_lat, center_lng],
                zoom_start=8,
                tiles='OpenStreetMap'
            )
            
            # Add start marker
            folium.Marker(
                [start_lat, start_lng],
                popup=f"<b>Start: {route_data['start']['city']}</b>",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
            
            # Add end marker
            folium.Marker(
                [end_lat, end_lng],
                popup=f"<b>End: {route_data['end']['city']}</b>",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
            
            # Add route line
            folium.PolyLine(
                locations=[[start_lat, start_lng], [end_lat, end_lng]],
                color='blue',
                weight=3,
                opacity=0.8,
                popup=f"Route: {route_data['start']['city']} → {route_data['end']['city']}"
            ).add_to(m)
            
            # Add attractions
            for i, attraction in enumerate(attractions[:5]):  # Show first 5 attractions
                lat = attraction['location']['lat']
                lng = attraction['location']['lng']
                name = attraction['name']
                category = attraction.get('category', 'Unknown')
                distance = attraction.get('distance_from_route', 0)
                
                popup_html = f"""
                <b>{name}</b><br>
                Category: {category}<br>
                Distance: {distance:.2f} miles
                """
                
                folium.Marker(
                    [lat, lng],
                    popup=popup_html,
                    icon=folium.Icon(color='green', icon='star')
                ).add_to(m)
            
            # Save map to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w') as f:
                m.save(f.name)
                temp_file = f.name
            
            # Open in browser
            webbrowser.open(f'file://{temp_file}')
            
        except Exception as e:
            raise Exception(f"Map creation failed: {str(e)}")
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function"""
    print("🗺️ Starting Route Visualizer...")
    print("Make sure your backend API is running at http://localhost:8000")
    print()
    
    app = RouteVisualizer()
    app.run()

if __name__ == "__main__":
    main() 