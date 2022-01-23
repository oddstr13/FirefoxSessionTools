from lib import readMozLZ4, writeMozLZ4


if __name__ == "__main__":
    sessionstore = readMozLZ4("sessionstore.jsonlz4")
    print(sessionstore.keys())

    for win in sessionstore.get("windows", []):
        for tab in win.get("tabs", []):
            # print(tab.keys())
            index = tab.get("index", 1) - 1
            entries = [tab.get("entries")[index]]
            tab["entries"] = entries
            tab["index"] = 1

    writeMozLZ4("output.jsonlz4", sessionstore)
