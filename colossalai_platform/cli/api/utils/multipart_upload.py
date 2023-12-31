import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Union, BinaryIO

from colossalai_platform.cli.api.utils.types import Context, ApiError

LOGGER = logging.getLogger(__name__)


@dataclass
class UploadRequest:
    id: str
    path: str

@dataclass
class MultiPartUploader:
    ctx: Context
    url: str

    # intermediate data.
    # To simplify the logic, we only assign them explicitly in the upload() method.
    _req: UploadRequest = None
    _upload_id: str = None
    _etags: list[str] = None

    _number_of_chunks: int = None
    _file_size: int = None
    _chunk_size: int = None

    def upload(
            self,
            req: UploadRequest,
            local_file_path: Union[Path, str],
    ):
        self._req = req
        self._file_size = local_file_path.stat().st_size
        self._chunk_size = self.ctx.config.max_upload_chunk_bytes
        self._number_of_chunks = 1 + (self._file_size // self._chunk_size)
        self._upload_id = self._start_multipart_upload()

        with open(local_file_path, "rb") as f:
            self._etags = self._multipart_upload(f)

        self._merge_multipart_upload()

    def _start_multipart_upload(self) -> str:
        url = self.url + "/uploadStart"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            json={
                "id": self._req.id,
                "numberOfSlices": self._number_of_chunks,
            },
        )

        if response.status_code == 200:
            return response.json()["uploadId"]
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

    def _multipart_upload(self, f: BinaryIO) -> list[str]:
        LOGGER.debug(f"start multipart upload, number_of_chunks = {self._number_of_chunks}")

        etags = []
        for i in range(self._number_of_chunks):
            chunk_size = min(
                self._chunk_size,
                self._file_size - i * self._chunk_size,
            )
            offset = i * self._chunk_size

            # prevent reading the whole file into memory
            f.seek(offset, os.SEEK_SET)
            etag = self._raw_upload(
                chunk_number=i,
                chunk_size=chunk_size,
                data=f.read(chunk_size),
            )
            etags.append(etag)
        return etags

    def _merge_multipart_upload(self):
        url = self.url + "/uploadComplete"
        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            json={
                "uploadId": self._upload_id,
                "id": self._req.id,
                "filePath": self._req.path,
                "parts": [
                    {
                        "partNumber": i,
                        "eTag": etag,
                    }
                    for i, etag in enumerate(self._etags)
                ]
            },
        )

        if response.status_code != 200 or response.json()["success"] != True:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

    def _raw_upload(
            self,
            chunk_number: int,
            chunk_size: int,
            data: bytes,
    ) -> str:
        url = self.url + "/upload"
        response = self.ctx.session.post(
            url,
            headers=self.ctx.bearer_token_header(),
            files={
                'uploadId': (None, self._upload_id),
                'chunkNumber': (None, str(chunk_number)),
                'fileSize': (None, str(chunk_size)),
                'data': (self._req.path, data)
            },
        )

        if response.status_code == 200:
            return response.json()["eTag"]
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")
