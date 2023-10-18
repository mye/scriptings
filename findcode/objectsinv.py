from typing import Callable, Mapping, Tuple
from pathlib import Path
import re
import zlib
from collections import defaultdict
import logging
from bs4 import BeautifulSoup

InventoryEntry = Tuple[str, str]  # (uri, display name)
_match_inv_line = re.compile(
    r"(?x)(.+?)\s+(\S+)\s+(?:-?\d+)\s+?(\S*)\s+(.*)"
).match
log = logging.getLogger(__name__)


def load_inventory(source: Path) -> Mapping[str, Mapping[str, InventoryEntry]]:
    '{"role": {"name": ("path#anchor", "display-name"}}'
    with (source / "objects.inv").open("rb") as fp:
        assert b"# Sphinx inventory version 2\n" == fp.readline()

        key, value = fp.readline().split(b": ", 1)
        assert b"# Project" == key

        key = fp.readline().split(b": ")[0]
        assert b"# Version" == key

        line = fp.readline()
        assert re.fullmatch(
            b"# The (remainder|rest) of this file is compressed (using|with) "
            b"zlib.\n",
            line,
        )

        entries = zlib.decompress(fp.read()).decode().splitlines()

    return _lines_to_tuples(_exists_in(source), entries)

def _exists_in(source):
	return lambda path: Path(source / path).exists()


def _lines_to_tuples(
    check_exists: Callable[[str], bool],
    entries: list[str]
) -> Mapping[str, dict[str, tuple[str, str]]]:
    """
    Transform inventory lines *entries* to the required dict of dicts of tuples.
    Use *check_exists* callable to verify whether the indexed path exits
    """
    rv: Mapping[str, dict[str, tuple[str, str]]] = defaultdict(dict)

    for line in entries:
        m = _match_inv_line(line.rstrip())
        if not m:
            log.warning("intersphinx: invalid line: %r. Skipping.", line)
            continue

        name, role, uri, display_name = m.groups()
        path, uri = _clean_up_path(uri.replace("$", name))

        if not check_exists(path):
            continue

        rv[role][name] = (uri, display_name)

    return rv


def _clean_up_path(uri: str) -> tuple[str, str]:
    """
    Clean up a path as it comes from an inventory.
    Discard the anchors between head and tail to make it
    compatible with situations where extra meta information is encoded.
    If the path ends with an "/", append an index.html.
    Returns:
        tuple of cleaned up path / URI based on cleaned up path
    """
    path_tuple = uri.split("#")
    if len(path_tuple) > 1:
        # Throw away everything between path and last anchor.
        path = _maybe_index(path_tuple[0])
        return path, f"{path}#{path_tuple[-1]}"

    # No anchor: path = URI
    path = _maybe_index(uri)
    return path, path


def _maybe_index(path: str) -> str:
    if path.endswith("/"):
        return f"{path}index.html"

    return path

if __name__ == '__main__':
	import sys
	from itertools import islice
	source = Path(sys.argv[1])
	inv = load_inventory(source)
	#print(inv)
	#for i in islice(inv.items(), 20):
	#	print(i)
	n = 1
	for type_key, inv_entries in islice(inv.items(), 10):
		#print(type_key)
		for key, data in islice(inv_entries.items(), 3):
			#print(key, '=>', data)
			filename = data[0].split("#")[0] if '#' in data[0] else data[0]
			path = source / filename
			with path.open(encoding="utf-8") as f:
				soup = BeautifulSoup(f, "html.parser")
			#if '#' not in data[0]:
			#	print(key, '=>', data)

			if '#' in data[0]:
				anchor = data[0].split('#')[1]
				pos = (
					soup.find("a", {"class": "headerlink"}, href="#" + anchor)
					or soup.find("a", {"class": "reference internal"}, href="#" + anchor)
					or soup.find("span", id=anchor)
				)
				print(pos)

#first_part =
#with path.open(mode="wb") as fb:
#            fb.write(soup.encode("utf-8"))

# Put