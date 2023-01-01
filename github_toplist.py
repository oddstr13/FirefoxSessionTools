from typing import Dict, Optional

from lib import normalizeHost, readMozLZ4, getUrlPath


if __name__ == "__main__":
    repos: Dict[str, Dict[str, int]] = {}
    orgs: Dict[str, int] = {}

    tabs = 0
    sessionstore = readMozLZ4("sessionstore.jsonlz4")
    print(sessionstore.keys())

    for win in sessionstore.get("windows", []):
        for tab in win.get("tabs", []):

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

                orgs[org] = orgs.get(org, 0) + 1

                repos[org] = repos.get(org, dict())
                repos[org][repo] = repos[org].get(repo, 0) + 1

    for org, count in sorted(orgs.items(), key=lambda x: x[1]):
        for repo, rcount in sorted(repos.get(org, {}).items(), key=lambda x: x[1]):
            print(f"{org}/{repo}: {rcount}")
        print(f"{org}: {count}")

    print(f"Total tabs: {tabs}")
    repocount = sum([len(x) for x in repos.items()])
    print(f"A total of {repocount} repos over {len(orgs.keys())} organizations.")
