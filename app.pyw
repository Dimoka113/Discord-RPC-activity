from functions.logger import Logger
from functions.autopip import *
from functions.threads import mainthread
from functions.threads import notifythread
from threading import Thread
try:
    from functions.statics import *
    from data.activity import Activity
    import keyboard
except:
    install_requirements()
    from functions.statics import *
    from data.activity import Activity
    import keyboard

Logger.level(Logger.types.INFO)
Logger.is_color(False)


if __name__ == "__main__":
    logger = Logger()
    activivty = Activity()

    Thread(name="Main", target=mainthread.main, args=(logger, activivty,),).start()
    Thread(name="Keys", target=notifythread.main, args=(logger, activivty,),).start()

    logger.info("Discord RPC started!") 