import subprocess, sys
from pathlib import Path


def install_requirements(self, requirements_path="requirements.txt"):
    req_file = Path(requirements_path)
    if not req_file.exists():
        raise FileNotFoundError(f"{requirements_path} не найден")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
    except subprocess.CalledProcessError as e:
        self.logger("Ошибка установки зависимостей.")
        raise e