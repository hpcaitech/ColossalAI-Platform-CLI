import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Union

from colossalai_platform.cli.api.storage import Storage, UploadRequest, StorageType
from colossalai_platform.cli.api.types import ApiError, Context

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
    createdAt: str
    private: bool
    isOwned: bool


@dataclass
class DeleteFilesRequest:
    Id: str
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
        self.storage = Storage(ctx)

    def list(
        self,
        is_owned=True,
    ) -> List[DatasetListResponse]:
        url = self.ctx.config.api_server + "/api/dataset/list"

        current_page = 1
        merged_datasets = []
        while True:
            response = self.ctx.session.post(
                url,
                headers=self.ctx.headers(login=True),
                data=json.dumps({
                    "isOwned": is_owned,
                    "pager": {
                        "pageSize": 10,
                        "currentPage": current_page,
                    },
                }),
            )

            if response.status_code != 200:
                raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

            merged_datasets.extend(response.json()["datasets"])

            total_entries = response.json()["pager"]["totalEntries"]
            page_size = response.json()["pager"]["pageSize"]
            if page_size * current_page > total_entries:
                break
            else:
                current_page += 1

        LOGGER.debug(f"list response: {merged_datasets}")
        return [DatasetListResponse(**d) for d in merged_datasets]

    def info(self, dataset_id: str) -> DatasetInfoResponse:
        url = self.ctx.config.api_server + "/api/dataset/info"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            data=json.dumps({
                "datasetId": dataset_id,
            }),
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
        url = self.ctx.config.api_server + "/api/dataset/file/delete"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            data=json.dumps({
                "filePaths": req.filePaths,
                "datasetId": req.Id,
                "folders": req.folders,
            }),
        )

        if response.status_code != 200 or (not response.json()["success"]):
            if response.status_code == 500 and ("You must specify at least one object" in response.json()["message"]):
                raise NoObjectToDeleteError(req.Id)
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

    def upload_local_file(
        self,
        dataset_id: str,
        storage_path: str,
        local_file_path: Union[str, Path],
    ):
        self.storage.upload(
            req=UploadRequest(
                storage_type=StorageType.DATASET,
                storage_id=dataset_id,
                storage_path=storage_path,
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
            data=json.dumps({
                "datasetName": name,
                "datasetDescription": description,
            }),
        )

        if response.status_code == 200:
            return response.json()["datasetId"]
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")
