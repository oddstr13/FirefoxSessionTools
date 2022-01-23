from lib import readMozLZ4, writeMozLZ4
from furl import furl


if __name__ == "__main__":
    sessionstore = readMozLZ4("sessionstore.jsonlz4")
    print(sessionstore.keys())

    total = 0
    for i, win in enumerate(sessionstore.get("windows", [])):
        tabs = len(win.get("tabs", []))
        total += tabs
        print(f"Window {i+1}: {tabs}")
    print(f"Total tabs: {total}")
