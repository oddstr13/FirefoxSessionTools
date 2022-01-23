import sys

from lib import readMozLZ4, writeMozLZ4


if __name__ == "__main__":
    window_nos = sorted(set([int(x) for x in sys.argv[1:]]), reverse=True)
    print(window_nos)

    sessionstore = readMozLZ4("sessionstore.jsonlz4")
    print(sessionstore.keys())

    windows = sessionstore.get("windows", [])

    for window_no in window_nos:
        if window_no > len(windows):
            print(f"There are {len(windows)} windows.")
            exit(23)

        sessionstore["windows"].pop(window_no - 1)

    total = 0
    for i, win in enumerate(sessionstore.get("windows", [])):
        tabs = len(win.get("tabs", []))
        total += tabs
        print(f"Window {i+1}: {tabs}")

    print(f"Total tabs: {total}")

    writeMozLZ4("output.jsonlz4", sessionstore)
