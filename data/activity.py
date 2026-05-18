from functions.gateway import Gateway
from pypresence import Presence
from functions.logger import Logger
from functions.statics import Functions
from data.loader import Client
from functions.sound import Sound
import time

class Config(object):
    sleep = None
    time_idle = None
    sound_volume = None
    display_activity_on_start = None

    class Keysboards(object):
        hide_activity = None
        show_activity = None
        
        def __init__(self, data):
            self.hide_activity = data["hide_activity"]
            self.show_activity = data["show_activity"]

    def __init__(self, cfg: dict):
        self.keyboards = self.Keysboards(cfg["keyboards"])
        self.sleep = cfg["sleep"]
        self.time_idle = cfg["time_idle"]
        self.buttons = cfg["buttons"]
        self.sound_volume = cfg["sound_volume"]
        self.display_activity_on_start = cfg["display_activity_on_start"]

class Activity(Gateway):
    path = "data/data.json"
    rpc: Presence = None
    logger: Logger = None
    functions: Functions = None
    config: Config = None
    client = None
    sounds: Sound = None 
    is_connect = False
    display_activity = None

    def __init__(self):
        super().__init__(self.path, Logger("Activity-Gateway"))
        self.logger = Logger("Activity")
        self.client = Client()
        self.rpc = Presence(self.client.decode(self.client.id))
        self.config = Config(self.read()["config"])
        self.sounds = Sound()
        self.display_activity = self.config.display_activity_on_start
        self.functions = Functions(self.logger, self.config, self.sounds)

    def is_activity(self): return self.display_activity
    def change_activity(self): self.display_activity = not self.display_activity; self.logger.debug(f"Change activity to {self.display_activity}")
    def get_activity(self): return self.read()["activity"]

    def connect(self) -> bool:
        try: self.rpc.connect() 
        except: 
            for wait in range(1, 5+1):
                try:
                    time.sleep(self.config.sleep * wait)
                    self.rpc.connect() 
                except:
                    self.logger.debug("Unable to establish connection for RPC"); 
                    continue
                else:
                    return True
            self.logger.error("Unable to establish connection for RPC"); 
            self.disconnect()
            return False
        else: 
            self.logger.debug("Open new RPC session..")
            self.is_connect = True
            return True

    def disconnect(self): 
        self.logger.debug("Close RPC session..")
        self.is_connect = False
        self.rpc.close()


    