#!/usr/bin/env python3

import pandas as pd
import random

def create_usa_locations():
    
    df = pd.read_csv("heatmap/processed_roadside_attractions.csv")
    
    selected_attractions = [
        {"title": "Teapot Dome gas station, Zillah, Washington", "state": "WA", "category": "Gas Station"},
        {"title": "Hat n' Boots gas station, Seattle, Washington", "state": "WA", "category": "Gas Station"},
        {"title": "World's Largest Redwood Tree Service Station, Ukiah, California", "state": "CA", "category": "Gas Station"},
        
        {"title": "Mickey's Diner, St. Paul, Minnesota", "state": "MN", "category": "Restaurant"},
        {"title": "The Donut Hole, La Puente, California", "state": "CA", "category": "Restaurant"},
        {"title": "Bob's Java Jive, Tacoma, Washington", "state": "WA", "category": "Restaurant"},
        
        {"title": "Dog Bark Park, Cottonwood, Idaho", "state": "ID", "category": "Entertainment"},
        {"title": "The Barrel, Devils Lake, North Dakota", "state": "ND", "category": "Entertainment"},
        
        {"title": "Wigwam Village #6, Holbrook, Arizona", "state": "AZ", "category": "Lodging"},
        {"title": "Motel Inn (first motel), San Luis Obispo, California", "state": "CA", "category": "Lodging"}
    ]
    
    usa_locations = []
    
    for i, attraction in enumerate(selected_attractions):
        matching_rows = df[
            (df['title'].str.contains(attraction['title'].split(',')[0], case=False)) &
            (df['state'] == attraction['state'])
        ]
        
        if not matching_rows.empty:
            row = matching_rows.iloc[0]
            usa_locations.append({
                'location_name': row['title'],
                'latitude': 0,
                'longitude': 0,
                'activity_type': row['category'].lower().replace(' ', '_'),
                'state': row['state']
            })
    
    coordinates = [
        (46.4232, -120.2644),
        (47.6062, -122.3321),
        (39.1502, -123.2078),
        (44.9537, -93.0900),
        (34.0200, -117.9495),
        (47.2529, -122.4443),
        (46.0511, -116.8963),
        (48.1128, -98.8654),
        (34.9022, -110.1587),
        (35.2828, -120.6596)
    ]
    
    final_locations = []
    for i, location in enumerate(usa_locations):
        if i < len(coordinates):
            location['latitude'] = coordinates[i][0]
            location['longitude'] = coordinates[i][1]
            final_locations.append(location)
    
    df_out = pd.DataFrame(final_locations)
    df_out = df_out[['location_name', 'latitude', 'longitude', 'activity_type']]
    df_out.to_csv("data/locations.csv", index=False)
    
    print(f"Created locations.csv with {len(final_locations)} USA roadside attractions:")
    for location in final_locations:
        print(f"  • {location['location_name']} ({location['state']})")

if __name__ == "__main__":
    create_usa_locations() 