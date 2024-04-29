from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class MyEventHandler(FileSystemEventHandler):

    def on_modified(self, event):
        print(event.src_path, "modified.")


observer = Observer()
observer.schedule(MyEventHandler(), ".", recursive=False)
observer.start()
try:
    while observer.is_alive():
        observer.join(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
