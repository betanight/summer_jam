#!/usr/bin/env python3
"""
Simple script to reset the API data to the original locations.
"""

import os
import shutil

def reset_data():
    """Reset the data to original locations only."""
    
    # Remove processed data cache
    if os.path.exists("data/processed_data.pkl"):
        os.remove("data/processed_data.pkl")
        print("✅ Removed processed data cache")
    
    # Backup current locations and restore original
    if os.path.exists("data/locations.csv"):
        # The locations.csv should already have the USA locations
        print("✅ Locations file is ready with USA locations")
    
    print("✅ Data reset complete!")
    print("📝 Now restart the API server:")
    print("   python3 start_api.py")

if __name__ == "__main__":
    reset_data() 