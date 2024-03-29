# %%
# %pip install aiofiles

# %%
import asyncio
from pathlib import Path

from watchdog.observers import Observer

# %%
player_log = Path("foo.log")
player_log_path = Path(player_log)


# %%
class AsyncWatchdogEventHandler:
    """Schedule a coroutine to run on the given event loop
    whenever a watchdog event is received.

    """

    def __init__(self, loop, coro):
        self._loop = loop
        self._coro = coro

    def dispatch(self, event):
        self._loop.call_soon_threadsafe(asyncio.create_task, self._coro(event))


# """
# moved, deleted, created, modified, closed, opened
# """
# match event.event_type:
#     case "modified":
#         self._run(event)
#     case _:
#         pass


# %%
def tail(filepath: Path):
    assert filepath.is_file()
    f = filepath.open("r")
    f.seek(0, 2)

    async def read_last_line(event):
        print(event, filepath)
        if any((event.event_type == "modified", Path(event.src_path) == filepath)):
            while line := f.readline():
                print(line)

    return read_last_line


# %%
loop = asyncio.get_running_loop()
handle = tail(player_log)
handler = AsyncWatchdogEventHandler(loop, handle)
observer = Observer()
observer.schedule(handler, ".", recursive=False)
observer.start()


# %%
with open(player_log, "a") as f:
    f.write("Hello, world!\nfoo\nbar\nbaz\n")
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
