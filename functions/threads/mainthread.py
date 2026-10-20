from functions.logger import Logger
from data.activity import Activity
import time
import pythoncom
from threading import Event
from types import NoneType


def forgetstat_only(logger: Logger, acty: Activity, current_activity: dict):
    running = acty.functions.get_running_processes_exe()
    if not acty.custom_activity["Off"]:
        for custom in acty.custom_activity:
            if acty.custom_activity[custom]:
                activity = next((item for item in acty.get_custom_activity() if item["name"] == custom), None)
    else:
        activity = acty.functions.detect_activity(running, acty.get_activity())

    if activity != current_activity:
        if not acty.custom_activity["Off"]:
            for custom in acty.custom_activity:
                if acty.custom_activity[custom]:
                    activity = next((item for item in acty.get_custom_activity() if item["name"] == custom), None)
        else:
            activity = acty.functions.detect_activity(running, acty.get_activity())

        logger.info("[Get-stat-only] " + activity['name'])
        current_activity = activity
        return current_activity
    else:
        return current_activity

def main(event: Event, logger: Logger, acty: Activity):
    pythoncom.CoInitialize()

    current_activity = None; start = 0; activity = "started"
    if logger.logging == Logger.types.DEBUG: 
        logger.info("DEBUG mode enable, All actions will be logged. And all errors will return the exception stack")
        
    while not acty.is_connect:
        if 'discord.exe' in acty.functions.get_running_processes(): 
            acty.connect()
            logger.debug("Check done, Discord is open...")
        else: 
            if not start: logger.info("Waiting for Discord to open..."); start = 1
            else: logger.debug("Waiting for Discord to open..."); time.sleep(acty.config.sleep)
            current_activity = forgetstat_only(logger, acty, current_activity)

        if event.is_set(): logger.info("Shutdown thread Discord RPC..."); return


    logger.debug("Discord is Open... Send RPC stat.")
    current_activity = None; activity = ""

    while True:
        logger.trace(activity)
        try:
            if acty.display_activity: 
                running = acty.functions.get_running_processes_exe()
                if 'discord.exe' in acty.functions.get_running_processes(): 
                    if acty.is_connect:
                        if not acty.custom_activity["Off"]:
                            for custom in acty.custom_activity:
                                if acty.custom_activity[custom]:
                                    activity = next((item for item in acty.get_custom_activity() if item["name"] == custom), None)
                        else:
                            activity = acty.functions.detect_activity(running, acty.get_activity())

                        logger.debug(activity)
                        if activity != current_activity:
                            current_activity = activity
                            if isinstance(activity, NoneType):
                                acty.rpc.clear()
                                logger.info("Cleared")
                            else:
                                acty.rpc.update(
                                    details=activity["details"],
                                    state=activity["state"],
                                    name=activity["name"],
                                    large_image=activity["large_image"],
                                    small_image=activity["small_image"],
                                    small_text=activity["small_text"],
                                    buttons=acty.config.buttons,
                                    large_text=activity["large_text"]
                                )
                                logger.info(activity['name'])
                    else: 
                        acty.connect()
                        time.sleep(1)
                        continue            
                else:
                    time.sleep(1)
                    if acty.is_connect: acty.disconnect()
                    logger.debug("Waiting for Discord to open...")
                    current_activity = forgetstat_only(logger, acty, current_activity)

            else:
                time.sleep(1)
                if acty.is_connect: acty.disconnect()
                logger.debug("Waiting for the user to enable display activity...")
                current_activity = forgetstat_only(logger, acty, current_activity)

        except Exception as e:
            logger.error(e)
            if logger.logging == Logger.types.DEBUG: 
                logger.info("DEBUG mode enable, raising exception...")
                raise e
            
        if event.is_set(): logger.info("Shutdown thread Discord RPC..."); return
        time.sleep(acty.config.sleep)