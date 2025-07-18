"""
Data loading utilities for the summer activity route optimization project.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_locations(file_path: str = "data/locations.csv") -> pd.DataFrame:
    """
    Load location data from CSV file.
    
    Args:
        file_path (str): Path to the CSV file containing location data
        
    Returns:
        pd.DataFrame: DataFrame with location data including coordinates
    """
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Successfully loaded {len(df)} locations from {file_path}")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

def validate_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate coordinate data and remove invalid entries.
    
    Args:
        df (pd.DataFrame): DataFrame with location data
        
    Returns:
        pd.DataFrame: Cleaned DataFrame with valid coordinates
    """
    # Check for missing values
    missing_coords = df[['latitude', 'longitude']].isnull().sum()
    if missing_coords.sum() > 0:
        logger.warning(f"Found {missing_coords.sum()} missing coordinate values")
        df = df.dropna(subset=['latitude', 'longitude'])
    
    # Validate coordinate ranges
    valid_lat = (df['latitude'] >= -90) & (df['latitude'] <= 90)
    valid_lon = (df['longitude'] >= -180) & (df['longitude'] <= 180)
    
    invalid_coords = ~(valid_lat & valid_lon)
    if invalid_coords.sum() > 0:
        logger.warning(f"Found {invalid_coords.sum()} invalid coordinate values")
        df = df[valid_lat & valid_lon]
    
    logger.info(f"Data validation complete. {len(df)} valid locations remaining")
    return df

def get_coordinates_array(df: pd.DataFrame) -> Tuple[np.ndarray, List[str]]:
    """
    Extract coordinates as numpy array and location names.
    
    Args:
        df (pd.DataFrame): DataFrame with location data
        
    Returns:
        Tuple[np.ndarray, List[str]]: Array of coordinates and list of location names
    """
    coordinates = df[['latitude', 'longitude']].values
    location_names = df['location_name'].tolist()
    
    return coordinates, location_names

def preprocess_data(file_path: str = "data/locations.csv") -> Tuple[pd.DataFrame, np.ndarray, List[str]]:
    """
    Complete data preprocessing pipeline.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        Tuple[pd.DataFrame, np.ndarray, List[str]]: Processed data
    """
    # Load data
    df = load_locations(file_path)
    
    # Validate data
    df = validate_coordinates(df)
    
    # Extract coordinates and names
    coordinates, location_names = get_coordinates_array(df)
    
    logger.info(f"Data preprocessing complete. Ready for modeling with {len(df)} locations")
    
    return df, coordinates, location_names 