import json, os
from functions.logger import Logger


class Gateway(object):
    path = str()
    logger: Logger = None

    def __init__(self, path: str, logger: Logger = Logger("Gateway")):
        self.path = path
        self.logger = logger

        if not self._check_exist():
            with open(self.path, "w+", encoding="UTF-8") as file: 
                json.dump(self._create_default_data(), file, indent=3, ensure_ascii=False)

    def _check_exist(self): return os.path.isfile(path=self.path)

    def read(self):
        if not os.path.isfile(self.path):
            self.logger.warn(f"Config not found: {self.path}. Creating default.")
            self._create_default()
            return self._create_default_data()

        with open(self.path, "r", encoding="UTF-8") as file: 
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError as err:
                self.logger.warn(err)
                return self._create_default_data()

    def write(self, data: list) -> bool:
        """
Returns `True` if successful.

If unsuccessful, outputs a log with `WARN` and returns `False`.
        """
        try: 
            with open(self.path, "w", encoding="UTF-8") as file: json.dump(data, file, indent=3, ensure_ascii=False)
        except Exception as err:
            self.logger.warn(err)
            return False
        else: return True

    def _create_default(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="UTF-8") as file: json.dump(self._create_default_data(), file, indent=3, ensure_ascii=False)

    def _create_default_data(self):
        schema_path = os.path.join(os.path.dirname(__file__), "..", "data", "schema.data.json")

        if not os.path.isfile(schema_path):
            self.logger.warn("schema.json missing, using hardcoded fallback")
            return {
                "config": {
                    "sleep": 5,
                    "time_idle": 60,
                    "sound_volume": 10,
                    "buttons": []
                },
                "activity": []
            }

        with open(schema_path, "r", encoding="utf-8") as f:
            return json.load(f)