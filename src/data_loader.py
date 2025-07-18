"""
Data loading utilities for the route optimization system.
Handles loading and preprocessing of location data.
"""

import csv
import numpy as np
import logging
from typing import List, Dict, Tuple
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """
    Data loader for location information.
    """
    
    def __init__(self, data_file: str = "data/locations.csv"):
        """
        Initialize the data loader.
        
        Args:
            data_file (str): Path to the CSV file containing location data
        """
        self.data_file = data_file
        self.locations = []
        self.coordinates = None
        self.location_names = []
    
    def load_data(self) -> Tuple[np.ndarray, List[str]]:
        """
        Load location data from CSV file.
        
        Returns:
            Tuple[np.ndarray, List[str]]: Coordinates array and location names
        """
        try:
            if not os.path.exists(self.data_file):
                raise FileNotFoundError(f"Data file not found: {self.data_file}")
            
            locations = []
            with open(self.data_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    locations.append({
                        'id': int(row['id']),
                        'name': row['name'],
                        'latitude': float(row['latitude']),
                        'longitude': float(row['longitude'])
                    })
            
            self.locations = locations
            self.location_names = [loc['name'] for loc in locations]
            self.coordinates = np.array([[loc['latitude'], loc['longitude']] for loc in locations])
            
            logger.info(f"Successfully loaded {len(locations)} locations from {self.data_file}")
            return self.coordinates, self.location_names
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def validate_data(self) -> bool:
        """
        Validate the loaded data for consistency and completeness.
        
        Returns:
            bool: True if data is valid, False otherwise
        """
        if not self.locations:
            logger.error("No locations loaded")
            return False
        
        for i, location in enumerate(self.locations):
            # Check required fields
            if not all(key in location for key in ['id', 'name', 'latitude', 'longitude']):
                logger.error(f"Missing required fields in location {i}")
                return False
            
            # Validate coordinate ranges
            lat, lon = location['latitude'], location['longitude']
            if not (-90 <= lat <= 90):
                logger.error(f"Invalid latitude {lat} for location {location['name']}")
                return False
            if not (-180 <= lon <= 180):
                logger.error(f"Invalid longitude {lon} for location {location['name']}")
                return False
        
        logger.info("Data validation complete. {} valid locations remaining".format(len(self.locations)))
        return True
    
    def preprocess_data(self) -> Tuple[np.ndarray, List[str]]:
        """
        Preprocess the data for modeling.
        
        Returns:
            Tuple[np.ndarray, List[str]]: Processed coordinates and names
        """
        if not self.validate_data():
            raise ValueError("Data validation failed")
        
        # Ensure coordinates are in the correct format
        coordinates = np.array([[loc['latitude'], loc['longitude']] for loc in self.locations])
        location_names = [loc['name'] for loc in self.locations]
        
        logger.info("Data preprocessing complete. Ready for modeling with {} locations".format(len(location_names)))
        return coordinates, location_names
    
    def get_locations(self) -> List[Dict]:
        """
        Get the loaded locations as a list of dictionaries.
        
        Returns:
            List[Dict]: List of location dictionaries
        """
        return self.locations
    
    def add_location(self, name: str, latitude: float, longitude: float) -> int:
        """
        Add a new location to the dataset.
        
        Args:
            name (str): Location name
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            
        Returns:
            int: ID of the new location
        """
        # Validate coordinates
        if not (-90 <= latitude <= 90):
            raise ValueError(f"Invalid latitude: {latitude}")
        if not (-180 <= longitude <= 180):
            raise ValueError(f"Invalid longitude: {longitude}")
        
        # Generate new ID
        new_id = max([loc['id'] for loc in self.locations]) + 1 if self.locations else 0
        
        new_location = {
            'id': new_id,
            'name': name,
            'latitude': latitude,
            'longitude': longitude
        }
        
        self.locations.append(new_location)
        self.location_names.append(name)
        
        # Update coordinates array
        if self.coordinates is None:
            self.coordinates = np.array([[latitude, longitude]])
        else:
            self.coordinates = np.vstack([self.coordinates, [latitude, longitude]])
        
        logger.info(f"Added location: {name} (ID: {new_id})")
        return new_id 