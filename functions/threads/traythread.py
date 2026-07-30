import pystray
from pystray import MenuItem as item, Menu
from PIL import Image
from threading import Event
from functions.logger import Logger
from data.activity import Activity
from functions.threads.hotkeyhread import Notify
import time

class Tray(object):
    change = False
    icon = None
    logger = None
    acty = None
    event = None

    def __init__(self, event: Event, logger: Logger, acty: Activity):
        def on_exit(icon, _):
            event.set()
            icon.stop()
            acty.rpc.clear()
            acty.rpc.close()

        def change_activity(item):
            if acty.is_activity(): acty.rpc.clear()

            acty.change_activity()
            Notify.change_activity(acty.display_activity)
            logger.info(f"Change status activity to turn {Notify.bool_to_str(acty.display_activity)}")

        def is_activity(item): 
            n = acty.is_activity()
            return n

        def on_custom_activity(icon, _):
            for i in self.acty.custom_activity: self.acty.custom_activity[i] = False
            self.acty.custom_activity[str(_)] = True

        def check_custom_activity(item): 
            if not str(item) in self.acty.custom_activity:
                self.acty.custom_activity[str(item)] = False
                self.logger.debug(self.acty.custom_activity)
                return False
            else:
                return self.acty.custom_activity[str(item)]
            
        self.event = event
        self.logger = logger
        self.acty = acty
        self.icon = pystray.Icon(
            "Discord RPC",
            self.load_icon(),
            title="Discord RPC",
            menu=pystray.Menu(
                item(text="Show activity", action=change_activity, checked=is_activity),
                Menu.SEPARATOR,
                item("Custom activity", Menu(
                    *[item(text=name, action=on_custom_activity, checked=check_custom_activity) for name in self.acty.get_custom_activity_names()]
                )),
                Menu.SEPARATOR,
                item(text="Exit", action=on_exit)
            ), 
        )

    def load_icon(self, path: str = "data/app.ico"):
        img = Image.open(path)
        img = img.convert("RGBA")
        return img

    def tray_checker(self):
        while not self.event.is_set():
            if self.change: 
                self.logger.debug("Change status in tray...")
                self.icon.update_menu()
                self.change = False
            time.sleep(1)

        self.logger.info("Shutdown Tray-Checker Thread...") 
    def main(self):
        self.icon.run_detached()

        while not self.event.is_set():
            time.sleep(1)

        self.logger.info("Shutdown Tray Thread...") 