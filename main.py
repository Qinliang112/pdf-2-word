import aiohttp
import os
import time

from watchdog.observers import Observer

from pdfword.api import ILovePDF_API
from pdfword.monitor import FileMonitorEvent


USERPROFILE = os.environ["USERPROFILE"]
USERPROFILE_ONE_DRIVE = os.path.join(USERPROFILE, "OneDrive")

# This is a option that can be changed
MONITOR_PATH = os.path.join(USERPROFILE_ONE_DRIVE, "pdf")
SAVE_PATH = os.path.join(USERPROFILE_ONE_DRIVE, "word")


if not os.path.exists(MONITOR_PATH):
    os.mkdir(MONITOR_PATH)

if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)


async def process_data(file_path):
    async with aiohttp.ClientSession() as session:
        api = ILovePDF_API(session)

        await api.get_task_id_and_token()
        print('Initiating ILovePDF API and Page')

        await api.upload(file_path)
        print('Uploading file to ILovePDF API')

        await api.process()
        print('Processing file to ILovePDF API')

        saving_path = await api.download(SAVE_PATH)
        print(f"Successfully download file to {saving_path}")


def main():
    observer = Observer()
    observer.schedule(FileMonitorEvent(process_data), MONITOR_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    main()