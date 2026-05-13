from functions.logger import Logger
from functions.autopip import *
from functions.mainthread import main

try:
    from functions.statics import *
    from data.activity import Activity
except:
    install_requirements()
    from functions.statics import *
    from data.activity import Activity

Logger.level(Logger.types.INFO)
Logger.is_color(False)


if __name__ == "__main__":
    main(Logger(), Activity())