from functions.autopip import *
from functions.logger import Logger

Logger.level(Logger.types.TRACE)
Logger.is_color(True)
Autopip()

from threading import Thread, Event
import time

from data.activity import Activity
from functions.threads import mainthread
from functions.threads import hotkeyhread
from functions.threads import traythread




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