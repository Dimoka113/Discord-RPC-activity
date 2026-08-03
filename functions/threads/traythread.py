import pystray
from pystray import MenuItem as item, Menu
from PIL import Image
from threading import Event
from functions.logger import Logger
from data.activity import Activity
from functions.threads.hotkeyhread import Notify
import time

class Tray(object):
    icon = None
    logger = None
    acty = None
    event = None

    def __init__(self, event: Event, logger: Logger, acty: Activity):
        self.event = event
        self.logger = logger
        self.acty = acty
        self.icon = pystray.Icon(
            "Discord RPC",
            self.load_icon(),
            title="Discord RPC",
            menu=pystray.Menu(
                item(text="Show activity", action=self.change_activity, checked=self.is_activity),
                Menu.SEPARATOR,
                item("Custom activity", Menu(
                    *[item(text=name, action=self.on_custom_activity, checked=self.check_custom_activity) for name in self.acty.get_custom_activity_names()]
                )),
                Menu.SEPARATOR,
                item(text="Exit", action=self.on_exit)
            ),
        )

    def on_exit(self, icon, _):
        self.event.set()
        self.icon.stop()
        self.acty.rpc.clear()
        self.acty.rpc.close()

    def change_activity(self):
        if self.acty.is_activity(): self.acty.rpc.clear()

        self.acty.change_activity()
        Notify.change_activity(self.acty.display_activity)
        self.logger.info(f"Change status activity to turn {Notify.bool_to_str(self.acty.display_activity)}")

    def is_activity(self, _=None): 
        n = self.acty.is_activity()
        return n

    def on_custom_activity(self, icon, _):
        for i in self.acty.custom_activity: self.acty.custom_activity[i] = False
        self.acty.custom_activity[str(_)] = True

    def check_custom_activity(self, item): 
        if not str(item) in self.acty.custom_activity:
            self.acty.custom_activity[str(item)] = False
            self.logger.debug(self.acty.custom_activity)
            return False
        else:
            return self.acty.custom_activity[str(item)]

    def _build_menu(self):
        return Menu(
            item("Show activity", self.change_activity, checked=lambda _: self.is_activity(), ),
            Menu.SEPARATOR,
            item(
                "Custom activity",
                Menu(
                    *[
                        item(
                            name,
                            self.on_custom_activity,
                            checked=self.check_custom_activity,
                        )
                        for name in self.acty.get_custom_activity_names()
                    ]
                ),
            ),

            Menu.SEPARATOR,

            item("Exit", self.on_exit),
        )

    def load_icon(self, path: str = "data/app.ico"):
        img = Image.open(path)
        img = img.convert("RGBA")
        return img

    def tray_checker(self):
        while not self.event.is_set():
            self.logger.debug("Change status in tray...")
            self.icon.menu = self._build_menu()
            self.icon.update_menu()
            time.sleep(3)

        self.logger.info("Shutdown Tray-Checker Thread...") 

    def main(self):
        self.icon.run_detached()

        while not self.event.is_set():
            time.sleep(1)

        self.logger.info("Shutdown Tray Thread...") 