import sys

from lib import readMozLZ4, writeMozLZ4, normalizeHost


if __name__ == "__main__":
    window_nos = sorted(set([int(x) for x in sys.argv[1:]]))

    sessionstore = readMozLZ4("sessionstore.jsonlz4")
    print(sessionstore.keys())

    closed_windows = sessionstore.get("_closedWindows", [])
    if not window_nos:
        for wn, win in enumerate(closed_windows):
            tabcount = len(win.get("tabs", []))
            first_tabs = []
            for tab in win.get("tabs", []):

                entries = tab.get("entries")

                if entries:
                    index = tab.get("index", 1) - 1
                    entry = tab.get("entries")[index]
                    url = entry.get("url")
                else:
                    url = tab.get("userTypedValue")

                host = normalizeHost(url)
                if host:
                    first_tabs.append(host)
                    if len(first_tabs) >= 5:
                        break
            print(f"#{wn} {tabcount} tabs: {', '.join(first_tabs)}")
        exit()


    for window_no in window_nos:
        if window_no > len(closed_windows):
            print(f"There are {len(closed_windows)} closed windows.")
            exit(23)

    for window_no in sorted(window_nos, reverse=True):
        sessionstore["windows"].append(closed_windows.pop(window_no))
        print(f"Restored window {window_no}")

    writeMozLZ4("output.jsonlz4", sessionstore)
