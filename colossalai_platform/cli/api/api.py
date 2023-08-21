import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, IO
import requests
import enum

from colossalai_platform.cli.config import Config

LOGGER = logging.getLogger(__name__)


class ApiError(Exception):
    pass


class LoginRequiredError(Exception):

    def __init__(self, message="Login required"):
        super().__init__(message)


class StorageType(enum.Enum):
    DATASET = "dataset"
    PROJECT = "project"


@dataclass
class ColossalPlatformApi:
    config: Config
    token: str = ""
    session: requests.Session = requests.Session()

    def login(self):
        # TODO: a better URL construction method,
        #       with pydantic.HttpUrl
        url = str(self.config.api_server) + "/api/user/login"

        if self.config.username == "" or self.config.password == "":
            raise ApiError("Username or password is empty, please call `cap configure` first")

        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({
            "username": self.config.username,
            "password": self.config.password,
        })

        response = self.session.request(
            "POST",
            url,
            headers=headers,
            data=payload,
        )

        if response.status_code == 200:
            self.token = response.json()['accessToken']
        else:
            raise ApiError(f"Login failed with status code {response.status_code}, body: {response.text}")

    def upload(
        self,
        storage_type: StorageType,
        storage_id: str,
        storage_path: str,
        local_file_path: Path | str,
    ):
        # TODO(ofey404): multi part upload for large file
        LOGGER.debug(f"Uploading {local_file_path} to {storage_type.value}://{storage_id}/{storage_path}")
        url = self._get_presigned_upload_urls(
            storage_type=storage_type,
            storage_id=storage_id,
            file_path=storage_path,
            total_parts=1,
        )[0]

        with open(local_file_path) as f:
            content = f.read()
            self._upload(url, content)

    def _upload(
        self,
        presigned_url: str,
        data: str,
    ):
        response = self.session.put(
            presigned_url,
            data,
        )
        response.close()

        if response.status_code != 200:
            raise ApiError(f"Upload failed with status code {response.status_code}, body: {response.text}")

    def _get_presigned_upload_urls(
        self,
        storage_type: StorageType,
        storage_id: str,
        file_path: str,
        total_parts,
    ) -> List[str]:
        url = str(self.config.api_server) + "/api/presignUpload"

        if self.token == "":
            raise LoginRequiredError()

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.token,
        }
        payload = json.dumps({
            "type": storage_type.value,
            "id": storage_id,
            "filePath": file_path,
            "totalParts": total_parts,
        })

        response = self.session.request(
            "POST",
            url,
            headers=headers,
            data=payload,
        )

        if response.status_code == 200:
            return response.json()["presignedUrls"]
        else:
            raise ApiError(f"presignUpload failed with status code {response.status_code}, body: {response.text}")
