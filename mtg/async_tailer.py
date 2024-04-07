# %%
import asyncio
import json
import random
import time
from pathlib import Path, PurePath

from watchdog.observers import Observer


# %%
class AsyncWatchdogEventHandler:
    """Create a task for `coro` on `loop` for each watchdog file event."""

    def __init__(self, loop, coro):
        self._loop = loop
        self._coro = coro

    def dispatch(self, event):
        self._loop.call_soon_threadsafe(asyncio.create_task, self._coro(event))


# %%
def make_tail_coro(filepath: Path, queue: asyncio.Queue[str]):
    """Returns a coroutine that puts lines appended to `file` into `queue`.
    Works with watchdog events. The file is read in a separate thread to avoid
    blocking the event loop.

    """
    assert filepath.is_file()
    f = filepath.open("r")
    f.seek(0, 2)
    loop = asyncio.get_running_loop()

    def get_lines():
        for line in f:
            loop.call_soon_threadsafe(queue.put_nowait, line)

    async def on_modified(event):
        is_modified = event.event_type == "modified"
        is_same_file = PurePath(event.src_path) == filepath
        if is_modified and is_same_file:
            await asyncio.to_thread(get_lines)

    return on_modified


# %%
async def consume(queue: asyncio.Queue[str]):
    """Take items from `queue` and try to parse them as JSON."""
    while True:
        line = await queue.get()
        try:
            line_json = json.loads(line)
        except json.JSONDecodeError:
            pass
        else:
            print(f"Got JSON: {line_json}")
        queue.task_done()


# %%

player_log = Path("foo.log")
loop = asyncio.get_running_loop()
queue = asyncio.Queue()
handle = make_tail_coro(player_log, queue)
handler = AsyncWatchdogEventHandler(loop, handle)
observer = Observer()
observer.schedule(handler, ".", recursive=False)
observer.start()

consumer = asyncio.create_task(consume(queue))

# %%
with open(player_log, "a") as f:
    f.write("Hello, world!\nfoo\nbar\nbaz\n")

# %%
with open(player_log, "a") as f:
    f.write('{"foo": "bar"}\n')
    f.write('{"baz": "qux"}\n')

# %%
# input_log = Path("C:\\Users\\loren\\Downloads\\UTC_Log - 03-17-2024 23.25.20.log")
input_log = Path("C:\\Users\\loren\\Downloads\\DraftLog_HBG_BotDraft_1657658456.log")


async def append():
    with input_log.open("r") as f, open("foo.log", "a") as g:
        for i, line in enumerate(f):
            # print(i, line)
            g.write(line)
            g.flush()
            await asyncio.sleep(0)


# %%
appender = asyncio.create_task(append())
# %%
DRAFT_START_STRINGS = [
    "[UnityCrossThreadLogger]==> Event_Join ",
    "[UnityCrossThreadLogger]==> BotDraft_DraftStatus ",
]


def draft_start(line):
    for start_string in DRAFT_START_STRINGS:
        if start_string in line:
            json_offset = line.find(start_string)
            event_data = json.loads(line[json_offset + len(start_string) :])
            draft_id = event_data.get("id")
            request_data = json.loads(event_data["request"])
            payload_data = json.loads(request_data["Payload"])
            event_name = payload_data["EventName"]
            update, event_type, draft_id = self.draft_start_search_v1(event_data)
            event_line = line


# %%
observer.stop()

# %%
observer.is_alive()
# %%
try:
    while observer.is_alive():
        observer.join(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
