from functions.logger import Logger
from data.activity import Activity
import time
import pythoncom
from threading import Event
from datetime import datetime


def main(event: Event, logger: Logger, acty: Activity):
    pythoncom.CoInitialize()

    current_activity = None; start = 0
    if logger.logging == Logger.types.DEBUG: 
        logger.info("DEBUG mode enable, All actions will be logged. And all errors will return the exception stack")
        
    while not acty.is_connect:
        if 'discord.exe' in acty.functions.get_running_processes(): 
            acty.connect()
            logger.debug("Check done, Discord is open...")
        else: 
            if not start: logger.info("Waiting for Discord to open..."); start = 1
            else: logger.trace("Waiting for Discord to open..."); time.sleep(acty.config.sleep)
    
    while True:
        if not event.is_set():
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
                                if activity is None:
                                    acty.rpc.clear()
                                    logger.info("Cleared")
                                else:
                                    acty.update_activity(activity)
                                logger.info(activity['name'])
                                logger.debug(activity["time"]+1)
                        else: 
                            acty.connect()
                            time.sleep(1)
                            acty.update_activity(activity)
                            logger.info(activity['name'])
                            continue            
                    else:
                        current_activity = None
                        time.sleep(1)
                        if acty.is_connect: acty.disconnect()
                        logger.trace("Waiting for Discord to open...")
                else:
                    current_activity = None
                    time.sleep(1)
                    if acty.is_connect: acty.disconnect()
                    logger.trace("Waiting for the user to enable display activity...")     

            except Exception as e:
                logger.error(e)
                if "debug" in logger.logging: 
                    logger.info("DEBUG mode enable, raising exception...")
                    raise e
        else:
            logger.info("Shutdown thread Discord RPC...")
            break
        time.sleep(acty.config.sleep)