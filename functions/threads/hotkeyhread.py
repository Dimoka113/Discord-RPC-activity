from functions.logger import Logger
from data.activity import Activity
import keyboard
from functions.notify import Notify
from functions.threads.traythread import Tray

def main(logger: Logger, acty: Activity, tray: Tray):
    hide_act = acty.config.keyboards.hide_activity
    show_act = acty.config.keyboards.show_activity

    Notify.started(acty.display_activity, show_act)

    def hide():
        if acty.display_activity:
            acty.display_activity = not acty.display_activity
            acty.rpc.clear()
            tray.change = True
            Notify.change_activity(False, show_act)
            logger.info(f"Change status activity to turn {Notify.bool_to_str(acty.display_activity)}")

    def show():
        if not acty.display_activity:
            acty.display_activity = not acty.display_activity
            tray.change = True
            Notify.change_activity(True, hide_act)
            logger.info(f"Change status activity to turn {Notify.bool_to_str(acty.display_activity)}")

    def toggle():
        if acty.display_activity: 
            hide()
        else: 
            show()

    if hide_act == show_act:
        keyboard.add_hotkey(hide_act, toggle)
    else:
        keyboard.add_hotkey(hide_act, hide)
        keyboard.add_hotkey(show_act, show)

    logger.debug("Check hotkeys done!")
    keyboard.wait()