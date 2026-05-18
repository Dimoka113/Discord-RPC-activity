from functions.autopip import *
from threading import Thread, Event
import time
try:
    from functions.statics import *
    from data.activity import Activity
    import keyboard
    from pystray import MenuItem as item
    from PIL import Image
    from functions.threads import mainthread
    from functions.threads import hotkeyhread
    from functions.threads import traythread
    from functions.logger import Logger
except:
    install_requirements()
    from functions.statics import *
    from data.activity import Activity
    import keyboard
    from functions.threads import mainthread
    from functions.threads import hotkeyhread
    from functions.threads import traythread
    from functions.logger import Logger

    
Logger.level(Logger.types.INFO)
Logger.is_color(False)


if __name__ == "__main__":
    logger = Logger("App")
    event = Event()
    activivty = Activity()
    tray = traythread.Tray(event, Logger("Tray"), activivty)

    Thread(name="Main", target=mainthread.main, args=(event, Logger("Main"), activivty,),).start()
    Thread(name="Keys", target=hotkeyhread.main, args=(Logger("Keys"), activivty, tray), daemon=True,).start()
    Thread(name="Tray", target=tray.main).start()
    Thread(name="Tray-Checker", target=tray.tray_checker).start()


    while not event.is_set(): time.sleep(1)

    logger.info("Shutdown App Thread...") 