# %%
# %pip install sismic
# %%
import re
from ast import Call
from pathlib import Path
from typing import Callable, Sequence

from attr import dataclass, field
from sismic.io import export_to_plantuml, import_from_yaml
from sismic.model import Statechart

# %%
here = Path(__file__).parent
request_holder_path = Path("request_holder.yaml")

statechart = import_from_yaml(filepath=str(here / request_holder_path))

export_to_plantuml(statechart, str(here / "pics/request_holder.plantuml"))


# %%


def coro(x):
    print(x)
    return x


matchers = [
    [False, ("drafts", lambda x: x, "packs", lambda x: x, "picks", lambda x: x), coro],
    [False, ("drafts", lambda x: x, "packs", lambda x: x, "picks"), coro],
    [False, ("drafts", lambda x: x, "packs", lambda x: x), coro],
    [False, ("drafts", lambda x: x), coro],
    [True, [], coro],
    [True, ["foo"], coro],
]

t = ("drafts", "123", "packs", "345", "picks", "1")

# %%


@dataclass
class Node:
    """A prefix tree node. It holds coroutines to be called
    when traversed (its parent node has).

    """
    coros: list[Callable]
    children: list
    matcher: str | Callable | None = None


class PathMatcher:
    def __init__(self, domains) -> None:
        self.root = Node(coros=[],)

    def insert(self, path, handler):
        node = self.root
        for part in path:
            if part not in node.children:
                node.children[part] = Node()
            node = node.children[part]
        node.coros.append(handler)

    def invoke(self, path: Sequence[str]):
        """Call handlers registered for path."""
        node = self.root
        for part in path:



# %%
matcher = PathMatcher()
for prefix, path, handler in matchers:
    matcher.insert(path, handler)

matcher.invoke(t)

# %%
