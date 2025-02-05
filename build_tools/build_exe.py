import os
import sys
import shutil
import subprocess
from pathlib import Path

# Ajusta o path para acessar o projeto principal
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Importa o script atual
with open(Path(__file__).parent.parent / "build_exe.py") as f:
    exec(f.read()) 