from datetime import date
import json
from time import perf_counter
import matplotlib.pyplot as plt
from os import environ, system
import colorama
from colorama import Fore
import sys


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


suppress_qt_warnings()
colorama.init(autoreset=True)
today = date.today()
session_time = 0
work = False


# convert passed time into readable format
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


# class that operates with json file
class Database:
    def __init__(self):
        try:
            with open('data.json', 'r') as f:
                self.data = json.load(f)
        except (Exception, ValueError):
            self.data = {}
        try:
            self.time = self.data[str(today)]
        except (Exception, ValueError):
            self.time = 0

    def update_data(self):
        self.data[str(today)] = self.time

    def upload_to_db(self):
        with open('data.json', 'w+') as f:
            json.dump(self.data, f)


# generate plot from data.json file
def generate_plot():
    with open('data.json', 'r') as f:
        data = json.load(f)
    lists = sorted(data.items())  # data sorted by key, return a list of tuples
    x, y = zip(*lists)  # unpack a list of pairs into two tuples
    converted = []
    print(Fore.CYAN + "* Graph Is Loading *\n")
    for i in y:
        converted.append(convert(i))
    plt.bar(x, [28800 for _ in range(len(y))])
    plt.bar(x, y)
    plt.xlabel('Dzień')
    plt.ylabel("Czas pracy")

    for i in range(len(y)):
        plt.annotate(f"{str(converted[i])}  {round((y[i] / 288), 2)}%", xy=(x[i], y[i]), ha='center', va='bottom')

    plt.show()


# function that operates commands
def working():
    while True:
        x = input()
        if x == "show":
            try:
                generate_plot()
            except (Exception, ValueError):
                print("* ERROR * There Is No Data To Show\n")
        if x == "stop" and work:
            print(Fore.CYAN + "\n* Timer Stopped *")
            print(f"  This Session Lasted {Fore.LIGHTGREEN_EX}{convert(perf_counter() - session_time)}\n")
            return False, session_time
        elif x == "go":
            print(Fore.LIGHTGREEN_EX + "\n* Started New Session *")
            print("  Good Luck !\n")
            return True, perf_counter()
        elif x == "cls":
            system('CLS')
        elif x == "reset_all":
            print(Fore.RED + "Do You Really Want To Delete All Collected Data ?  y/n")
            while True:
                choose = input()
                if choose in ("y", "Y"):
                    with open('data.json', 'w+') as f:
                        json.dump({}, f)
                        db.data = {}
                        db.time = 0
                    print(Fore.YELLOW + "\n* All Data Has Been Deleted *\n")
                    break
                elif choose in ("n", "N"):
                    break
        elif x == "reset_today":
            print(Fore.RED + "Do You Want To Delete Data From Today ?  y/n")
            while True:
                choose = input()
                if choose in ("y", "Y"):
                    with open('data.json', 'r') as f:
                        data = json.load(f)
                    with open('data.json', 'w+') as f:
                        data[str(today)] = 0
                        json.dump(data, f)
                    print(Fore.YELLOW + "\n* Data From Today Has Been Deleted *\n")
                    break
                elif choose in ("n", "N"):
                    break
        elif x == "help":
            print(Fore.CYAN + "\nCommands:\n  go\n  stop\n  show\n  help\n  reset_all\n  reset_today\n  cls\n  exit\n"
                  )
        elif x in ('exit', 'ex', 'e', 'end'):
            sys.exit(1)


db = Database()

# main loop
while True:
    work, session_time = working()
    if not work:
        db.time += perf_counter() - session_time
    db.update_data()
    db.upload_to_db()
