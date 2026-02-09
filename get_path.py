import sys
import os 

def get_path(relative_path):
    """Get the absolute path to a resource, works for dev and Nuitka"""
    # Check if we are running as a compiled Nuitka Onefile
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)