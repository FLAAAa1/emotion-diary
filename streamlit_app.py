"""Entry point for Streamlit Community Cloud deployment."""
import sys, os

# Ensure project root is on Python path
sys.path.insert(0, os.path.dirname(__file__))

# Run the main frontend app
import frontend.app
