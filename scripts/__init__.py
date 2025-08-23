import sys
import os

def setup_path():
    """Add src directory to Python path for dev script"""
    src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)