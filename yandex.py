import os
import requests
import json

class YDiskUploader:

    def __init__(self, file_path: str, token: str, destination_folder: str = "/"):
        self.file_path = file_path
        self.oauth_token = token
        self.url = "https://cloud-api.yandex.net:443/v1/disk/resources/upload"
        self.headers = {
            "Authorization": "OAuth " + self.oauth_token
        }

        self.destination_folder = "/"
        if len(destination_folder) != 0:
             destination_folder = destination_folder.replace("\\", "/")
             if not destination_folder.startswith("/"):
                 destination_folder = "/" + destination_folder
             if not destination_folder.endswith("/"):
                 destination_folder += "/"
             self.destination_folder = destination_folder

    def upload(self):
        result = {
            "error": False,
            "msg": ""
        }
        if not os.path.isfile(self.file_path):
             result["error"] = True
             result["msg"] = f'Incorrect path to file: {self.file_path}'
             return result

        with open(self.file_path) as f:
            filedata = f.read()

        ydisk_path = self.destination_folder + os.path.basename(self.file_path)
        params = {
            "path": ydisk_path,
            "overwrite": True
        }

        response = requests.get(self.url, params=params, headers=self.headers)
        resp_info = json.loads(response.text)
        ok_codes = (200, 201)
        if not response.status_code in ok_codes:
             resp_info = json.loads(response.text)
             result["error"] = True
             result["msg"] = f"Error with getting a link to file: {resp_info['message']}"
             return result

        response = requests.put(resp_info['href'], data = filedata)
        if not response.status_code in ok_codes:
            error_info = json.loads(response.text)
            result["error"] = True
            result["msg"] = f"Error with attempt to upload the file to YDisk: {error_info['message']}"
            return result

        result["msg"] = "Upploaded successfully"
        return result

if __name__ == '__main__':
    with open("token.txt", encoding="utf-8") as tokenfile:
        token = tokenfile.read().strip()
    uploader = YDiskUploader('test.txt', token=token, destination_folder='/', encoding="utf-8")
    result = uploader.upload()
    print(result["msg"])