import json
import os
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, IO
from urllib.parse import urlparse, parse_qs

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
class UploadRequest:
    storage_type: StorageType
    storage_id: str
    storage_path: str


@dataclass
class ColossalPlatformApi:
    config: Config
    token: str = ""
    session: requests.Session = requests.Session()

    def login(self):
        url = str(self.config.api_server) + "/api/user/login"

        if self.config.username == "" or self.config.password == "":
            raise ApiError("Username or password is empty, please call `cap configure` first")

        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({
            "username": self.config.username,
            "password": self.config.password,
        })

        response = self.session.post(
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
        req: UploadRequest,
        local_file_path: Path | str,
    ):
        total_parts = 1 + local_file_path.stat().st_size // self.config.max_upload_chunk_bytes
        LOGGER.debug(f"Uploading {local_file_path} to {req.storage_type.value}://{req.storage_id}/{req.storage_path}")

        if total_parts > 1:
            urls, upload_id = self._get_multipart_presigned_urls(
                req=req,
                total_parts=total_parts,
            )
            LOGGER.debug(f"urls = {urls}, upload_id = {upload_id}")

            etags = []
            with open(local_file_path, 'rb') as f:
                for i, url in enumerate(urls):
                    offset = i * self.config.max_upload_chunk_bytes
                    f.seek(offset, os.SEEK_SET)
                    etag = self._raw_upload(url, f.read(self.config.max_upload_chunk_bytes))
                    etags.append(etag)

            self._complete_multipart_upload(
                req=req,
                upload_id=upload_id,
                etags=etags,
            )
        else:
            url = self._get_presigned_url(req)
            with open(local_file_path) as f:
                content = f.read()
                self._raw_upload(url, content)

    def _get_presigned_url(
        self,
        req: UploadRequest,
    ) -> str:
        urls, _ = self._get_multipart_presigned_urls(
            req,
            total_parts=1,
        )
        return urls[0]

    def _get_multipart_presigned_urls(
        self,
        req: UploadRequest,
        total_parts,
    ) -> Tuple[List[str], str]:
        """Get presigned upload urls for a file.

        Weird API behavior:
        if total_parts == 1:
          there is no `uploadId` in the response.
        """
        url = str(self.config.api_server) + "/api/presignUpload"

        payload = json.dumps({
            "type": req.storage_type.value,
            "id": req.storage_id,
            "filePath": req.storage_path,
            "totalParts": total_parts,
        })

        response = self.session.post(
            url,
            headers=self._headers(login=True),
            data=payload,
        )

        if response.status_code == 200:
            urls = response.json()["presignedUrls"]
            return urls, _get_upload_id(urls[0])
        else:
            raise ApiError(f"presignUpload failed with status code {response.status_code}, body: {response.text}")

    def _raw_upload(
        self,
        presigned_url: str,
        data: bytes,
    ) -> str:
        """Upload data to presigned_url and return the etag"""
        response = self.session.put(
            presigned_url,
            data,
        )
        response.close()

        if response.status_code != 200:
            raise ApiError(f"Upload failed with status code {response.status_code}, body: {response.text}")

        return response.headers["ETag"]

    def _headers(
        self,
        login=False,
    ):
        headers = {
            'Content-Type': 'application/json',
        }
        if login:
            if self.token == "":
                raise LoginRequiredError()
            headers["Authorization"] = "Bearer " + self.token
        return headers

    def _complete_multipart_upload(
        self,
        req: UploadRequest,
        upload_id: str,
        etags: List[str],
    ):
        url = str(self.config.api_server) + "/api/completeMultipartUpload"

        payload = json.dumps({
            "parts": [{
                "partNumber": i + 1,
                "eTag": etag,
            } for i, etag in enumerate(etags)],
            "uploadId": upload_id,
            "type": req.storage_type.value,
            "id": req.storage_id,
            "filePath": req.storage_path,
        })

        response = self.session.post(
            url,
            headers=self._headers(login=True),
            data=payload,
        )

        if response.status_code != 200 or (not response.json()["success"]):
            raise ApiError(f"completeMultipartUpload failed with body: {response.text}")


def _get_upload_id(presigned_url: str) -> str:
    """URL example:
    https://xxx.volces.com/1/dataset/11/a.txt?uploadId=342e7846666568512a
    """
    LOGGER.debug(f"presigned_url = {presigned_url}")
    p = urlparse(presigned_url)
    try:
        return parse_qs(p.query)["uploadId"][0]
    except KeyError:
        return ""
