from enum import unique
import sys

from lib import readMozLZ4, writeMozLZ4


if __name__ == "__main__":
    window_nos = sorted(set([int(x) for x in sys.argv[1:]]))

    sessionstore = readMozLZ4("sessionstore.jsonlz4")
    print(sessionstore.keys())

    windows = sessionstore.get("windows", [])

    for window_no in window_nos:
        if window_no > len(windows):
            print(f"There are {len(windows)} windows.")
            exit(23)

    sessionstore["windows"] = []
    for window_no in window_nos:
        sessionstore["windows"].append(windows[window_no - 1])

    writeMozLZ4("output.jsonlz4", sessionstore)
