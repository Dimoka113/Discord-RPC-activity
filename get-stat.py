from io import TextIOWrapper
import datetime, time, os
from functions.logger import Logger

class Getstat(object):
    path = None

    def __init__(self, path: str = "logs/Main.log"):
        self.path = path

    def _open(self) -> TextIOWrapper:
        return open(self.path, "r")

    def _get_stat(self) -> list[str]:
        data = []
        file = self._open()

        for i in file.read().split("\n"):
            if (("[DEBUG]" in i) or ("DEBUG mode enable" in i) or ("[ERROR]" in i) or i == ""): 
                continue
            else: 
                gamedata = i.replace("[Get-stat-only] ", "").replace("[INFO] [Main] ", "|| ").split(" || ")
                if len(gamedata[0].split()) > 2:
                    gamedata[0] = " ".join(str(gamedata[0]).split()[1:])

                if ("Shutdown thread Discord RPC" in i) or ("Waiting for Discord to open" in i):
                    data.append([gamedata[0].replace("[", "").replace("]", ""), "{red}Downtime{reset}"])
                else:
                    data.append([gamedata[0].replace("[", "").replace("]", ""), gamedata[1]])
        return data

    @staticmethod
    def _sort(data, information: bool = False, reverse: bool = False):
        if not information:
            newdata = {}
            for i in sorted(data, reverse=reverse): newdata[i] = data[i]
            return newdata
        else:
            return dict(sorted(data.items(), key=lambda x: x[1], reverse=reverse))
    @staticmethod
    def format_time(sec: float) -> str:
        milliseconds = round(sec * 1000)

        months, milliseconds = divmod(milliseconds, 2_592_000_000)
        days, milliseconds = divmod(milliseconds, 86_400_000)
        hours, milliseconds = divmod(milliseconds, 3_600_000)
        minutes, milliseconds = divmod(milliseconds, 60_000)
        seconds, milliseconds = divmod(milliseconds, 1000)

        units = [
            (months, "мес."),
            (days, "дн."),
            (hours, "ч."),
            (minutes, "мин."),
            (seconds, "сек."),
            (milliseconds, "мс."),
        ]

        return " ".join(f"{value} {unit}" for value, unit in units if value != 0) or "0 мс."

    def get_first_stat(self): return self._get_stat()[0]

    def get_games_time(self):
        gamestats = {}
        laststatsession = {}
        lasttimestatsession = {}

        data = self._get_stat()
        now = datetime.datetime.now()

        for current, following in zip(data, data[1:]):
            start = datetime.datetime.fromisoformat(current[0])
            end = datetime.datetime.fromisoformat(following[0])

            diff = (end - start).total_seconds()
            game = current[1]

            if game not in gamestats:
                gamestats[game] = 0.0

            gamestats[game] += diff
            laststatsession[game] = diff
            lasttimestatsession[game] = (
                now - end
            ).total_seconds()

        if data:
            last = data[-1]
            start = datetime.datetime.fromisoformat(last[0])
            game = last[1]

            diff = (now - start).total_seconds()

            if game not in gamestats:
                gamestats[game] = 0.0

            gamestats[game] += diff
            laststatsession[game] = diff
            lasttimestatsession[game] = 0.0

        return [gamestats, laststatsession, lasttimestatsession]

colors = Logger.colors
stat = Getstat()
while True:
    os.system("cls")
    gamestats, laststatsession, lasttimestatsession = stat.get_games_time()
    data = stat._sort(gamestats, True, True)
    all_data = 0

    first_log = stat.get_first_stat()[0]
    start = datetime.datetime.fromisoformat(first_log)
    end = datetime.datetime.now()
    dift_stat = (end - start).total_seconds()

    print(f"{colors.light_green}Статистика с момента: {colors.yellow}{first_log}")
    print(f"{colors.cyan}Глубина статистики: {colors.light_magenta}{stat.format_time(dift_stat)} {colors.white}(Всё время)")
    print(f"{colors.blue}-{colors.magenta}-"*18 + f"{colors.magenta} Общее время сессий: " + f"{colors.blue}-{colors.magenta}-"*18 + f"{colors.reset}")
    for game in data:
        game: str
        print("{green}{game}{resetcolor}: {time}{resetcolor} ({light_magenta}{proc}%{resetcolor})".format(
            game=game.format(red=colors.red, reset=colors.reset), time=stat.format_time(data[game]), 
            proc=round((data[game]/dift_stat)*100, 2),
            resetcolor=colors.reset,
            light_blue=colors.light_blue,
            light_magenta=colors.light_magenta,
            green=colors.green,
            red=colors.red
            ))
        
    print(f"{colors.blue}-{colors.magenta}-"*18 + f"{colors.magenta} Последняя сессия: " + f"{colors.blue}-{colors.magenta}-"*19 + f"{colors.reset}")

    datalast = stat._sort(laststatsession, True, True)
    for g in datalast:
        g: str
        print("{green}{game}{resetcolor}: {time}{resetcolor} ({cyan}{timeago}{resetcolor})".format(
            game=g.format(red=colors.red, reset=colors.reset), time=stat.format_time(datalast[g]), 
            resetcolor=colors.reset,
            timeago=f"{stat.format_time(lasttimestatsession[g])} назад" if lasttimestatsession[g]!=0 else "Сейчас",
            light_blue=colors.light_blue,
            light_magenta=colors.light_magenta,
            green=colors.green,
            cyan=colors.cyan,
            )) 
    time.sleep(2)
