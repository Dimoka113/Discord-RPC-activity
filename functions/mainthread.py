from functions.logger import Logger
from data.activity import Activity
import time

def main(logger: Logger, acty: Activity):
    current_activity = None; start = 0
    if logger.logging == Logger.types.DEBUG: 
        logger.info("DEBUG mode enable, All actions will be logged. And all errors will return the exception stack")
        
    while not acty.is_connect:
        running = acty.functions.get_running_processes()
        if 'discord.exe' in running: acty.connect()
        else: 
            if not start: logger.info("Waiting for Discord to open..."); start = 1
            else: logger.debug("Waiting for Discord to open..."); time.sleep(acty.config.sleep)
    while True:
        try:
            running = acty.functions.get_running_processes()
            if 'discord.exe' in running: 
                activity = acty.functions.detect_activity(running, acty.get_activity())
                logger.debug(activity)
                if activity != current_activity:
                    current_activity = activity
                    if activity is None:
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
                logger.debug("Waiting for Discord to open...")
                time.sleep(acty.config.sleep)
        except Exception as e:
            logger.error(e)
            if logger.logging == Logger.types.DEBUG: 
                logger.info("DEBUG mode enable, raising exception...")
                raise e

        time.sleep(acty.config.sleep)