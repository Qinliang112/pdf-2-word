from pdfword import PDFEventHandler, folder_path
from watchdog.observers import Observer
import time


if __name__ == '__main__':
    observer = Observer()
    event_handler = PDFEventHandler()
    observer.schedule(event_handler, path=folder_path, recursive=False)
    observer.start()

    try:
        print(f"Monitoring folder: {folder_path}")
        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()