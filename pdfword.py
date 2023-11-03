import os
import shutil
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from watchdog.events import FileSystemEventHandler

downloads_dir = 'C:\\Users\\qinli\\Downloads'
folder_path = 'C:\\Users\\qinli\\OneDrive\\Desktop\\pdf'
desktop_path = 'C:\\Users\\qinli\\OneDrive\\Desktop'


class PDFConversionAutomation:
    def __init__(self, downloads_dir, folder_path, desktop_path):
        self.downloads_dir = downloads_dir
        self.folder_path = folder_path
        self.desktop_path = desktop_path
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.ilovepdf.com/pdf_to_word")

    def upload_pdf(self):
        try:
            upload_button = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.ID, "pickfiles"))
            )
            upload_button.click()

            time.sleep(1)
            pyautogui.hotkey('alt', 'd')
            pyautogui.write(self.folder_path)
            pyautogui.press('enter')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('up')
            pyautogui.press('enter')

        except Exception as e:
            print(f"An error occurred during file upload: {str(e)}")

    def convert_pdf(self):
        try:
            convert_button = WebDriverWait(self.driver, 4).until(
                EC.presence_of_element_located((By.ID, "processTask"))
            )
            convert_button.click()
            time.sleep(10)
        except Exception as e:
            print(f"An error occurred during conversion: {str(e)}")

    def download_converted_file(self):
        try:
            download_button = WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located((By.ID, "pickfiles"))
            )
            download_button.click()
            time.sleep(2.5)
        except Exception as e:
            print(f"An error occurred during download: {str(e)}")

    def move_file(self):
        downloaded_files = os.listdir(self.downloads_dir)
        downloaded_files = [file for file in downloaded_files if os.path.isfile(os.path.join(self.downloads_dir, file))]
        downloaded_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.downloads_dir, x)))

        if downloaded_files:
            first_file = downloaded_files[-1]

            source_path = os.path.join(self.downloads_dir, first_file)
            destination_path = os.path.join(self.desktop_path, first_file)
            shutil.move(source_path, destination_path)
        else:
            print("No files found in the Downloads directory.")

        pdf_files = os.listdir(self.folder_path)[0]
        source_path = os.path.join(self.folder_path, pdf_files)
        destination_path = os.path.join(self.desktop_path, pdf_files)
        shutil.move(source_path, destination_path)

    def refresh_page(self):
        time.sleep(1)
        pyautogui.press('f5')

    def close_browser(self):
        self.driver.quit()

class PDFEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith(".pdf"):
            time.sleep(1)
            automation = PDFConversionAutomation(downloads_dir, folder_path, desktop_path)
            automation.upload_pdf()
            automation.convert_pdf()
            automation.download_converted_file()
            automation.move_file()
            automation.close_browser()
            automation.refresh_page()

        else:
            print(f"File not supported: {event.src_path}")
        
