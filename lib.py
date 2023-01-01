import struct
import json
from typing import Optional

import lz4.block
from furl import furl

MOZ_HEADER = b"mozLz40\0"


def readMozLZ4(fn):
    with open(fn, "rb") as fh:
        header = fh.read(8)
        if header != MOZ_HEADER:
            raise ValueError("File does not contain the mozLz40 header.")
        _size = fh.read(4)

        # WARNING: unknown if it is always little-endian, or if it is native byte order
        size = struct.unpack("<I", _size)[0]
        print("Size:", size)
        fh.seek(-4, 1)
        return json.loads(lz4.block.decompress(fh.read()))


def writeMozLZ4(fn, data):
    with open(fn, "wb") as fh:
        fh.write(MOZ_HEADER)
        fh.write(lz4.block.compress(json.dumps(data).encode("utf-8")))


def normalizeHost(url: Optional[str]) -> Optional[str]:
    if url is None:
        return None

    if url.startswith("view-source:"):
        url = url[12:]

    if "/" in url:
        host = furl(url).host
    else:
        host = url

    if host is None:
        return None

    if host.startswith("www."):
        host = host[4:]
    return host


def getUrlPath(url: Optional[str]) -> Optional[str]:
    if url is None:
        return None
    path = furl(url).path
    return str(path) if path else None


def getActiveTab(tab) -> dict:
    entries = tab.get("entries")
    if not entries:
        return {}
    index = tab.get("index", 1) - 1
    return entries[index]


if __name__ == "__main__":
    x = readMozLZ4("sessionstore.jsonlz4")
    print(x.keys())

    writeMozLZ4("output.jsonlz4", x)
