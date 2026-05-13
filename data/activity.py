import json
from functions import logger
from functions.gateway import Gateway
from pypresence import Presence
from functions.logger import Logger
from functions.statics import Functions
from data.loader import Client
from pycaw.pycaw import AudioUtilities
from functions.sound import Sound

class Config(object):
    sleep = None
    time_idle = None
    sound_volume = None
    def __init__(self, cfg: dict):
        self.sleep = cfg["sleep"]
        self.time_idle = cfg["time_idle"]
        self.buttons = cfg["buttons"]
        self.sound_volume = cfg["sound_volume"]

class Activity(Gateway):
    path = "data/data.json"
    rpc: Presence = None
    logger: Logger = None
    functions: Functions = None
    config: Config = None
    client = None
    sounds: Sound = None 

    def __init__(self, logger = Logger("Activity")):
        super().__init__(self.path, logger)
        self.logger = logger
        self.client = Client("data/client_id.json")
        self.rpc = Presence(self.client.decode(self.client.id))
        self.config = Config(self.read()["config"])
        self.sounds = Sound()

        self.functions = Functions(self.logger, self.config, self.sounds)

    def connect(self):
        try: self.rpc.connect() 
        except: self.logger.error("Unable to establish connection for RPC")

    def get_activity(self): return self.read()["activity"]
    