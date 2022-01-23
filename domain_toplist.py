from typing import Dict, Optional

from lib import normalizeHost, readMozLZ4


if __name__ == "__main__":
    domains: Dict[Optional[str], int] = {}
    tabs = 0
    sessionstore = readMozLZ4("sessionstore.jsonlz4")
    print(sessionstore.keys())

    for win in sessionstore.get("windows", []):
        for tab in win.get("tabs", []):
            tabs += 1
            index = tab.get("index", 1) - 1
            entry = tab.get("entries")[index]

            host = normalizeHost(entry.get("url"))

            domains[host] = domains.get(host, 0) + 1

    for host, count in sorted(domains.items(), key=lambda x: x[1]):
        print(f"{host}: {count}")
    print(f"Total tabs: {tabs}")
