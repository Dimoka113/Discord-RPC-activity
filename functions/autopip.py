import subprocess
import sys
from pathlib import Path
from functions.logger import Logger


def in_venv(): return sys.prefix != sys.base_prefix


def install_requirements(self, requirements_path = "requirements.txt", logger: Logger = Logger("pip")):
    req_file = Path(requirements_path)
    if not req_file.exists(): raise FileNotFoundError(f"{requirements_path} not found")
    
    if sys.prefix != sys.base_prefix: logger("found virtual env.")
    else: logger("System Python is used.")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r" , str(req_file)])
    except subprocess.CalledProcessError as e: 
        logger.crit("Dependency installation error."); raise e