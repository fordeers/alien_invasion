import sys
import os 

def get_path(relative_path):
    """Get the absolute path to a resource, works for dev and Nuitka"""
    # Check if we are running as a compiled Nuitka Onefile
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)

def get_save_path(filename):
    """Get the path to the folder where the EXE is actually sitting"""
    if getattr(sys, 'frozen', False):
        # sys.argv[0] is the path to the .exe file itself
        base_path = os.path.dirname(sys.argv[0])
    else:
        # We are in development mode
        base_path = os.path.dirname(os.path.abspath(__file__))
        
    return os.path.join(base_path, filename)