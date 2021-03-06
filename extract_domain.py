import json
import os
from typing import Dict
import sys
import time

import jinja2
from furl import furl

from lib import getActiveTab, normalizeHost, readMozLZ4, writeMozLZ4


def tabFilter(tab: dict) -> dict:
    at = getActiveTab(tab).copy()
    data = tab.copy()
    data.update(at)

    host = normalizeHost(at.get("url"))
    if host == "youtube.com":
        url = furl(at.get("url"))
        if url.args.has_key("v"):
            data[
                "thumbnail"
            ] = f"https://i.ytimg.com/vi/{url.args.get('v')}/maxresdefault.jpg"

    return data


if __name__ == "__main__":
    timestamp = time.strftime("%Y-%m-%d", time.gmtime())
    to_extract = [normalizeHost(x) for x in sys.argv[1:]]
    domains: Dict[str, int] = {}
    tabs = 0
    sessionstore = readMozLZ4("sessionstore.jsonlz4")

    extracted_tabs: Dict[str, list] = {}

    for win in sessionstore.get("windows", []):
        tablist = win.get("tabs", [])
        for i in range(len(tablist) - 1, -1, -1):
            tab = tablist[i]
            tabs += 1

            entry = getActiveTab(tab)

            url = entry.get("url")
            host = normalizeHost(url)

            if host is None:
                continue

            domains[host] = domains.get(host, 0) + 1

            if host in to_extract:
                extracted_tabs[host] = extracted_tabs.get(host, [])
                extracted_tabs[host].append(tablist.pop(i))

    template: jinja2.Template = jinja2.Template(
        open("extract_domain_template.jinja2").read()
    )

    os.makedirs(f"extracted/{timestamp}", exist_ok=True)
    for host in extracted_tabs.keys():
        html_file = f"extracted/{timestamp}/{host}.html"
        json_file = f"extracted/{timestamp}/{host}.json"

        tablist = extracted_tabs.get(host)

        filtered = [tabFilter(tab) for tab in tablist]

        tstream = template.stream(tabs=filtered)

        with open(html_file, "w") as fh:
            tstream.dump(fh)
        
        url_title_list = list(map(lambda x: dict(url=x.get('url'), title=x.get('title')), filtered))
        with open(json_file, "w") as fh:
            json.dump(url_title_list, fh, indent=2)


    writeMozLZ4("output.jsonlz4", sessionstore)
