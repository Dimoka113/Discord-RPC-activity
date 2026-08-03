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
            return self._create_default()

        with open(self.path, "r", encoding="UTF-8") as file: 
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError as err:
                self.logger.warn(err)
                return self._create_default()

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
        done = self.write(self._create_default_data())
        if done: return self.read()

    def _create_default_data(self):
        self.logger.warn("A default data.json has been generated.")
        self.logger.info("If you need help filling out data.json, you can check out the example in schema.data.json")
        
        with open("data/default.json", "r", encoding="UTF-8") as file: 
            return json.load(file)