import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Union

from colossalai_platform.cli.api.utils.multipart_upload import MultiPartUploader, UploadRequest
from colossalai_platform.cli.api.utils.pager import RequestAutoPager
from colossalai_platform.cli.api.utils.types import ApiError, Context

LOGGER = logging.getLogger(__name__)


@dataclass
class DatasetListResponse:
    datasetName: str
    datasetFullName: str
    datasetDescription: str
    createAt: str
    datasetId: str


@dataclass
class DatasetInfoResponse:
    datasetId: str
    datasetName: str
    datasetFullName: str
    datasetDescription: str
    createAt: str
    isPrivate: bool
    isOwned: bool


@dataclass
class DeleteFilesRequest:
    id: str
    filePaths: List[str] = field(default_factory=list)
    folders: List[str] = field(default_factory=list)


class DatasetNotFoundError(Exception):

    def __init__(self, dataset_id: str):
        super().__init__(f"Dataset {dataset_id} not found")


class NoObjectToDeleteError(Exception):

    def __init__(self, dataset_id: str):
        super().__init__(f"No object to delete in {dataset_id}")


class Dataset:

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.uploader = MultiPartUploader(
            ctx,
            self.ctx.config.api_server + "/api/file/dataset",
        )

    def list(
            self,
            is_owned=True,
    ) -> List[DatasetListResponse]:
        url = self.ctx.config.api_server + "/api/dataset/list"

        merged_datasets = RequestAutoPager(self.ctx).post(
            url,
            headers=self.ctx.headers(login=True),
            json={
                "isOwned": is_owned,
            },
            extract_func=lambda response: response.json()["datasets"],
        )

        LOGGER.debug(f"list response: {merged_datasets}")
        return [DatasetListResponse(**d) for d in merged_datasets]

    def info(self, dataset_id: str) -> DatasetInfoResponse:
        url = self.ctx.config.api_server + "/api/dataset/info"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            json={
                "datasetId": dataset_id,
            },
        )

        if response.status_code == 200:
            LOGGER.debug(f"dataset_info response: {response.json()}")
            return DatasetInfoResponse(**response.json())
        elif response.status_code == 404:
            if response.json()["message"] == "dataset not found":
                raise DatasetNotFoundError(dataset_id)
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

    def delete_files(self, req: DeleteFilesRequest):
        url = self.ctx.config.api_server + "/api/file/dataset/delete"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            json={
                "filePaths": req.filePaths,
                "id": req.id,
                "folders": req.folders,
            },
        )

        if response.status_code != 200 or (not response.json()["success"]):
            if response.status_code == 500 and ("You must specify at least one object" in response.json()["message"]):
                raise NoObjectToDeleteError(req.id)
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

    def upload_local_file(
            self,
            dataset_id: str,
            storage_path: str,
            local_file_path: Union[str, Path],
    ):
        self.uploader.upload(
            req=UploadRequest(
                id=dataset_id,
                path=storage_path,
            ),
            local_file_path=local_file_path,
        )

    def create(
            self,
            name: str,
            description: str,
    ) -> str:
        url = self.ctx.config.api_server + "/api/dataset/create"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            json={
                "datasetName": name,
                "datasetDescription": description,
            },
        )

        if response.status_code == 200:
            return response.json()["datasetId"]
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")
