"""
LCSH Assistant - Main entry point
"""
import os
import sys
from app.app import main

if __name__ == "__main__":
    # Add the current directory to the Python path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Run the Streamlit app
    main() 