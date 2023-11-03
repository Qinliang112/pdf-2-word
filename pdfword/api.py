import aiohttp
import os
import re

from typing import Tuple

from .constants import BASE_PDF_URL, BASE_PDF_API_URL


class ILovePDF_API:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session

        self.task_id = None
        self.token = None

        self.file_name = None

        self.server_file_name = None

        self.headers = {
            "Accept": "application/json",
            "Aceept-Encoding": "gzip, deflate, br",
            "Authorization": f"Bearer {self.token}"
        }


    async def get_task_id_and_token(self) -> None:
        result = await self.session.get(BASE_PDF_URL)

        if result.status != 200:
            raise Exception("Fail to get page")

        result_text = await result.text()

        result_task_id = re.search(r"ilovepdfConfig\.taskId = '(.*)';", result_text)
        result_token = re.search(r"token\":\"(.*?)\"", result_text)

        if result_task_id is None:
            raise Exception("Fail to get task id")

        if result_token is None:
            raise Exception("Fail to get token")

        result_task_id = result_task_id.group(1)
        result_token = result_token.group(1)

        self.task_id = result_task_id
        self.token = result_token

        self.headers["Authorization"] = f"Bearer {self.token}"

        
    async def upload(self, file_path: str) -> None:
        self.file_name = os.path.basename(file_path)
        
        formData = aiohttp.FormData()

        formData.add_field("name", self.file_name)
        formData.add_field("chunk", "0")
        formData.add_field("chunks", "1")
        formData.add_field("task", self.task_id)
        formData.add_field("preview", "1")
        formData.add_field("pdfinfo", "0")
        formData.add_field("pdfforms", "0")
        formData.add_field("pdfresetforms", "0")
        formData.add_field("v", "web.0")
        formData.add_field("file", open(file_path, "rb"))

        result = await self.session.post(f"{BASE_PDF_API_URL}/upload", data=formData, headers=self.headers)

        if result.status != 200:
            raise Exception("Fail to upload file")

        result_json = await result.json()

        self.server_file_name = result_json["server_filename"]

    async def process(self) -> None:
        formData = aiohttp.FormData()

        formData.add_field("convert_to", "docx")
        formData.add_field("output_filename", "{filename}")
        formData.add_field("packaged_filename", "ilovepdf_converted")
        formData.add_field("ocr", "0")
        formData.add_field("task", self.task_id)
        formData.add_field("tool", "pdfoffice")
        formData.add_field("files[0][server_filename]", self.server_file_name)
        formData.add_field("files[0][filename]", self.file_name)

        result = await self.session.post(f"{BASE_PDF_API_URL}/process", data=formData, headers=self.headers)

        if result.status != 200:
            raise Exception("Fail to process file")


    async def download(self, save_path) -> str:
        result = await self.session.get(f"{BASE_PDF_API_URL}/download/{self.task_id}")

        if result.status != 200:
            raise Exception("Fail to download file")

        dowload_file_name = result.headers["Content-Disposition"].split('"')[1]
        print(save_path)
        print(dowload_file_name)

        saving_path = os.path.join(save_path, dowload_file_name)
        
        with open(saving_path, "wb") as f:
            f.write(await result.read())

        return str(saving_path)
