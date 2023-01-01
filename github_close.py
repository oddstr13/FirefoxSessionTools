import sys
from typing import Dict, Optional, Tuple

from lib import normalizeHost, readMozLZ4, getUrlPath, writeMozLZ4


if __name__ == "__main__":
    to_close = [x.strip() for x in sys.argv[1:] if x.strip()]

    if not to_close:
        print("No repo specifiers specified; organization or organization/repo")
        exit(23)

    repos: Dict[str, Dict[str, int]] = {}
    orgs: Dict[str, int] = {}

    tabs = 0
    sessionstore = readMozLZ4("sessionstore.jsonlz4")
    print(sessionstore.keys())
    closed_tabs: Dict[str, list] = {}

    sessionstore["_closedWindows"] = sessionstore.get("_closedWindows", [])
    closed_windows: list = sessionstore["_closedWindows"]
    print(sessionstore["windows"][0].keys())

    for specifier in to_close:
        sp_org = specifier.split('/')[0]
        sp_repo: Optional[str]
        if '/' in specifier:
            sp_repo = specifier.split('/')[1]
        else:
            sp_repo = None

        for win in sessionstore.get("windows", []):
            win_tabs: list = win.get("tabs", [])
            for tab in win_tabs:

                entries = tab.get("entries")

                if entries:
                    index = tab.get("index", 1) - 1
                    entry = tab.get("entries")[index]
                    url = entry.get("url")
                else:
                    url = tab.get("userTypedValue")

                host = normalizeHost(url)

                if host != "github.com":
                    continue

                path = getUrlPath(url)
                if not path:
                    continue

                tabs += 1

                path = path.strip("/")

                if "/" in path:
                    x = path.split("/")
                    org = x[0]
                    repo = x[1]

                    if org == sp_org and (sp_repo is None or repo == sp_repo):
                        closed_tabs[specifier] = closed_tabs.get(specifier, [])
                        closed_tabs[specifier].append(tab)
                        win_tabs.remove(tab)

    for specifier in closed_tabs.keys():
        print(f"{specifier}: {len(closed_tabs[specifier])}")
        # Firefox doesn't recognize this simple structure as a window.
        # TODO: Add code to construct a new window.
        # closed_windows.insert(0, {'tabs':closed_tabs[specifier]})

    writeMozLZ4("output.jsonlz4", sessionstore)
