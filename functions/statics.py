import psutil
import ctypes
from functions.logger import Logger
from types import NoneType
from typing import Any
import time

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

    def lower_list(self, n): return [str(i).lower() for i in n] if n else None

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

    def get_running_processes_exe(self):
        processes = set()
        used = []

        for proc in psutil.process_iter(["name", "pid", "exe", 'create_time']):
            name: str = proc.info["name"]
            if not name in used:
                try:
                    exe: str = proc.info["exe"]
                    create_time: float = (time.time() - proc.info["create_time"])
                    if name: 
                        processes.add((name.lower(), exe, create_time))

                except (psutil.NoSuchProcess,
                        psutil.AccessDenied,
                        psutil.ZombieProcess):
                    pass
                used.append(name)
            else:
                continue
        return list(processes)

    def detect_activity(self, running: Any, act: list[dict]):
        idle_time = self.get_idle_duration()
        self.sounds.add_in_dumps(self.sounds.current_sounds())
        self.logger.debug(self.sounds.dumps)

        self.logger.debug(self.config.time_idle // self.config.sleep)
        if self.sounds.get_len_dumps() >= (self.config.time_idle // self.config.sleep):
            self.sounds.sound = self.sounds.get_dumps(); self.sounds.set_zero()
            self.logger.trace("sum sounds:", self.sounds.sound)

        if idle_time > 0: self.logger.debug("time in afk:", idle_time)
        new_activity = None
        for activity in act:
            if activity.get("idle") or activity.get("chill"): continue

            for name, exe, time in running:
                exe = str(exe).lower()
                if name in self.lower_list(activity["processes"]): 
                    path = activity.get("path")
                    if path:
                        if exe in self.lower_list(path): 
                            new_activity = activity
                            new_activity["time"] = time
                    else:
                        new_activity = activity
                        new_activity["time"] = time
                    
            if new_activity: break

        is_idle_time = idle_time >= self.config.time_idle
        is_loud = self.sounds.sound <= self.config.sound_volume
        result = is_idle_time and is_loud

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