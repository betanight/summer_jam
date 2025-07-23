#!/usr/bin/env python3

import os
import shutil

def reset_data():
    
    if os.path.exists("data/processed_data.pkl"):
        os.remove("data/processed_data.pkl")
        print("✅ Removed processed data cache")
    
    if os.path.exists("data/locations.csv"):
        print("✅ Locations file is ready with USA locations")
    
    print("✅ Data reset complete!")
    print("📝 Now restart the API server:")
    print("   python3 start_api.py")

if __name__ == "__main__":
    reset_data() 