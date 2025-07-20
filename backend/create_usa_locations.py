#!/usr/bin/env python3
"""
Convert roadside attractions data to locations.csv format for the API.
"""

import pandas as pd
import random

def create_usa_locations():
    """Create a locations.csv file with USA roadside attractions."""
    
    # Read the roadside attractions data
    df = pd.read_csv("heatmap/processed_roadside_attractions.csv")
    
    # Select a diverse set of interesting attractions
    # Let's pick some from different categories and states
    selected_attractions = [
        # Gas Stations
        {"title": "Teapot Dome gas station, Zillah, Washington", "state": "WA", "category": "Gas Station"},
        {"title": "Hat n' Boots gas station, Seattle, Washington", "state": "WA", "category": "Gas Station"},
        {"title": "World's Largest Redwood Tree Service Station, Ukiah, California", "state": "CA", "category": "Gas Station"},
        
        # Restaurants
        {"title": "Mickey's Diner, St. Paul, Minnesota", "state": "MN", "category": "Restaurant"},
        {"title": "The Donut Hole, La Puente, California", "state": "CA", "category": "Restaurant"},
        {"title": "Bob's Java Jive, Tacoma, Washington", "state": "WA", "category": "Restaurant"},
        
        # Entertainment
        {"title": "Dog Bark Park, Cottonwood, Idaho", "state": "ID", "category": "Entertainment"},
        {"title": "The Barrel, Devils Lake, North Dakota", "state": "ND", "category": "Entertainment"},
        
        # Lodging
        {"title": "Wigwam Village #6, Holbrook, Arizona", "state": "AZ", "category": "Lodging"},
        {"title": "Motel Inn (first motel), San Luis Obispo, California", "state": "CA", "category": "Lodging"}
    ]
    
    # Create a new dataframe with selected attractions
    usa_locations = []
    
    for i, attraction in enumerate(selected_attractions):
        # Find matching rows in the original data
        matching_rows = df[
            (df['title'].str.contains(attraction['title'].split(',')[0], case=False)) &
            (df['state'] == attraction['state'])
        ]
        
        if not matching_rows.empty:
            row = matching_rows.iloc[0]
            usa_locations.append({
                'location_name': row['title'],
                'latitude': 0,  # We'll need to add real coordinates
                'longitude': 0,  # We'll need to add real coordinates
                'activity_type': row['category'].lower().replace(' ', '_'),
                'state': row['state']  # Keep the state info
            })
    
    # Add some approximate coordinates for these locations
    # These are rough estimates based on the locations mentioned
    coordinates = [
        (46.4232, -120.2644),  # Zillah, WA
        (47.6062, -122.3321),  # Seattle, WA
        (39.1502, -123.2078),  # Ukiah, CA
        (44.9537, -93.0900),   # St. Paul, MN
        (34.0200, -117.9495),  # La Puente, CA
        (47.2529, -122.4443),  # Tacoma, WA
        (46.0511, -116.8963),  # Cottonwood, ID
        (48.1128, -98.8654),   # Devils Lake, ND
        (34.9022, -110.1587),  # Holbrook, AZ
        (35.2828, -120.6596)   # San Luis Obispo, CA
    ]
    
    # Create the final locations data
    final_locations = []
    for i, location in enumerate(usa_locations):
        if i < len(coordinates):
            location['latitude'] = coordinates[i][0]
            location['longitude'] = coordinates[i][1]
            final_locations.append(location)
    
    # Write to locations.csv (without the state column for API compatibility)
    df_out = pd.DataFrame(final_locations)
    df_out = df_out[['location_name', 'latitude', 'longitude', 'activity_type']]
    df_out.to_csv("data/locations.csv", index=False)
    
    print(f"Created locations.csv with {len(final_locations)} USA roadside attractions:")
    for location in final_locations:
        print(f"  • {location['location_name']} ({location['state']})")

if __name__ == "__main__":
    create_usa_locations() 