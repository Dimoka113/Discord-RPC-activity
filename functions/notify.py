from pathlib import Path
from winotify import Notification


class Notify():
    app_id = "Discord RPC"

    @classmethod
    def bool_to_str(self, data): return "on" if data else "off"

    @classmethod
    def send(self, title, msg):
        toast = Notification(
                    app_id=self.app_id,
                    icon=Path("data/app.ico").resolve(),
                    title=title,
                    msg=msg,
                )
        toast.show()

    @classmethod
    def started(self, status, key=""):
        self.send(
            title = "Discord activity is started",
            msg = "Press \"{key}\" to turn {status} the display".format(key=key, status=self.bool_to_str(not status)),
        )
        
    @classmethod
    def change_activity(self, status, key=""):
        if not key == "":
            self.send(
                title = "Activity display is turned {status}!".format(status=self.bool_to_str(status)),
                msg = "Press \"{key}\" to turn {status} the display".format(key=key, status=self.bool_to_str(not status)),
            )
        else:
            self.send(
                title = "Activity display is turned {status}!".format(status=self.bool_to_str(status)),
                msg = "The focus was moved via the traybar".format(key=key, status=self.bool_to_str(not status)),
            )