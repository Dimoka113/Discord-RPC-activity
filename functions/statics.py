
import psutil
import ctypes
from functions.logger import Logger
from types import NoneType


class LASTINPUTINFO(ctypes.Structure): _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint),]


class Functions(object):
    logger: Logger = None
    config = None
    sounds = None


    def __init__(self, logger: Logger, config, sounds):
        from data.activity import Config
        from functions.sound import Sound
        self.logger = logger
        self.config: Config = config
        self.sounds: Sound = sounds

    def get_idle_duration(self):
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(lii)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0

    def get_running_processes(self):
        processes = set()
        for proc in psutil.process_iter(["name"]):
            try:
                name: str = proc.info["name"]
                if name:
                    processes.add(name.lower())
            except:
                pass
        return processes

    def detect_activity(self, act: list[dict]):
        idle_time = self.get_idle_duration()
        running = self.get_running_processes()
        self.sounds.add_in_dumps(self.sounds.current_sounds())
        self.logger.debug(self.sounds.dumps)

        self.logger.debug(self.config.time_idle // self.config.sleep)
        if self.sounds.get_len_dumps() >= (self.config.time_idle // self.config.sleep):
            self.sounds.sound = self.sounds.get_dumps(); self.sounds.set_zero()
            self.logger.debug("sum sounds:", self.sounds.sound)

        if idle_time > 0: self.logger.debug("time in afk:", idle_time)
        new_activity = None

        for activity in act:
            if activity.get("idle") or activity.get("chill"):
                continue
            for process in activity.get("processes",[]):
                if process.lower() in running:
                    new_activity = activity

        is_idle_time = idle_time >= self.config.time_idle
        is_loud = self.sounds.sound <= self.config.sound_volume
        result = is_idle_time and is_loud
        self.logger.debug(is_idle_time)
        self.logger.debug(is_loud)

        self.logger.debug(result)

        if result:  
            self.logger.debug("-"*10)
            for activity in act:
                if activity.get("idle"):
                    new_activity = activity
        else:
            for activity in act:
                if activity.get("chill") and isinstance(new_activity, NoneType):
                    new_activity = activity


        return new_activity