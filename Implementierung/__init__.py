import os
import sys
current_dir = str(os.path.dirname(os.path.abspath(__file__)))
print(current_dir)
#sys.path.append(current_dir)
sys.path.insert(0,current_dir)
"""import os
import sys
from pathlib import Path
parent_path = Path(os.getcwd())
print(parent_path)
sys.path.append(os.path.abspath(parent_path))"""
