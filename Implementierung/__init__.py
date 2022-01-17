import os
import sys
from pathlib import Path
parent_path = Path(os.getcwd())
print(parent_path)
sys.path.append(os.path.abspath(parent_path))