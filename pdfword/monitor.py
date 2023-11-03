import asyncio

from watchdog.events import FileSystemEventHandler


class FileMonitorEvent(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event):
        if event.src_path.endswith(".pdf") and not event.is_directory:
            print(f"Monitor File created: {event.src_path}")
            asyncio.run(self.callback(event.src_path))