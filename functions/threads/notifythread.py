from functions.logger import Logger
from data.activity import Activity
import time, keyboard
from winotify import Notification


class Notify():
    app_id = "Discord RPC"

    @classmethod
    def bool_to_str(self, data): return "on" if data else "off"

    @classmethod
    def send(self, title, msg):
        toast = Notification(
                    app_id=self.app_id,
                    title=title,
                    msg=msg,
                )
        toast.show()

    @classmethod
    def started(self, status, key):
        self.send(
            title = "Discord activity is started",
            msg = "Press \"{key}\" to turn {status} the display".format(key=key, status=self.bool_to_str(not status)),
        )
        
    @classmethod
    def change_activity(self, status, key):
        self.send(
            title = "Activity display is turned {status}!".format(status=self.bool_to_str(status)),
            msg = "Press \"{key}\" to turn {status} the display".format(key=key, status=self.bool_to_str(not status)),
        )


def main(logger: Logger, acty: Activity):
    hide_act = acty.config.keyboards.hide_activity
    show_act = acty.config.keyboards.show_activity
    logger.debug("Check hotkeys done!")

    Notify.started(acty.display_activity, show_act)
    
    while True:
        if (acty.display_activity and keyboard.is_pressed(hide_act)): 
            acty.display_activity = not acty.display_activity
            acty.rpc.clear()
            Notify.change_activity(acty.display_activity, show_act)
            logger.info(f"Change status activity to {acty.display_activity}")
            
        elif (not acty.display_activity and keyboard.is_pressed(show_act)): 
            acty.display_activity = not acty.display_activity
            Notify.change_activity(acty.display_activity, hide_act)
            logger.info(f"Change status activity to {acty.display_activity}")
        time.sleep(0.1)