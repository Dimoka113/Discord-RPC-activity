import subprocess
import sys
from pathlib import Path
from functions.logger import Logger
import os
import importlib

class Autopip(object):
    REQUIRED_MODULES = (
    "psutil",
    "pythoncom",
    "pypresence",
    "pystray",
    "pycaw",
    "keyboard",
    )
    
    def __init__(self, logger: Logger = Logger("pip"), requirements_path: str = "requirements.txt"):
        self.logger = logger
        self.requirements_path = requirements_path
        self.ensure_requirements()

    def in_venv(self): return sys.prefix != sys.base_prefix

    def restart(self):
        self.logger.info("Restarting application...")

        try:
            subprocess.Popen(
                [sys.executable, *sys.argv],
                cwd=os.getcwd(),
                close_fds=True,
            )
        except OSError as e:
            self.logger.crit(f"Failed to restart application: {e}")
            raise
        else:
            self.logger.info("Restarting application...")
            os._exit(0)
        
    def ensure_requirements(self):
        try:
            for module in self.REQUIRED_MODULES: importlib.import_module(module)
        except ModuleNotFoundError as e:
            self.logger.debug(f'Module "{e.name}" is missing.')
            self.logger.warn("The required dependencies are missing")
            self.logger.info("The auto-pip-installation process has begun...")
            self.logger.debug(sys.executable)
            self.logger.debug(sys.argv)

            self.install_requirements()
            self.restart()
        else:
            self.logger.debug("All Modules installed!")


    def install_requirements(self):
        req_file = Path(self.requirements_path)
        if not req_file.exists(): raise FileNotFoundError(f"{self.requirements_path} not found")
        
        if self.in_venv(): self.logger.info("found virtual env.")
        else: self.logger.info("System Python is used.")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r" , str(req_file)])
        except subprocess.CalledProcessError as e: 
            self.logger.crit("Dependency installation error."); raise e