from pathlib import Path
from typing import List, Union
from dataclasses import dataclass, field
import json
import logging

from colossalai_platform.cli.api.multipart_upload import MultiPartUploader, UploadRequest
from colossalai_platform.cli.api.types import Context, ApiError

LOGGER = logging.getLogger(__name__)

@dataclass
class ModelListResponse:
    modelId: str
    modelVersion: int
    modelFullName: str
    modelName: str
    modelDescription: str
    createdAt: str
    updatedAt: str
    isFromJob: bool
    jobId: str
    jobName: str
    tags: List[str]

@dataclass
class ModelInfoResponse:
    modelId: str
    modelName: str
    modelFullName: str
    modelDescription: str
    createdAt: str
    updatedAt: str
    modelVersion: int
    private: bool
    isOwned: bool
    jobId: str

@dataclass
class DeleteFilesRequest:
    id: str
    filePaths: List[str] = field(default_factory=list)
    folders: List[str] = field(default_factory=list)

class Model:

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.uploader = MultiPartUploader(
            ctx,
            self.ctx.config.api_server + "/api/file/model",
            )

    def list(
            self,
            tags: List[str],
            is_owned=True,
    ) -> List[ModelListResponse]:
        url = self.ctx.config.api_server + "/api/model/list"

        # TODO(ofey404): extract duplicated code as a function
        current_page = 1
        merged_response = []
        while True:
            response = self.ctx.session.post(
                url,
                headers=self.ctx.headers(login=True),
                data=json.dumps({
                    "tags": tags,
                    "isOwned": is_owned,
                    "pager": {
                        "pageSize": 10,
                        "currentPage": current_page,
                    },
                }),
            )

            if response.status_code != 200:
                raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

            merged_response.extend(response.json()["models"])

            total_entries = response.json()["pager"]["totalEntries"]
            page_size = response.json()["pager"]["pageSize"]
            if page_size * current_page > total_entries:
                break
            else:
                current_page += 1

        LOGGER.debug(f"list response: {merged_response}")
        return [ModelListResponse(**d) for d in merged_response]

    def create(
            self,
            name: str,
            description: str,
    ) -> str:
        url = self.ctx.config.api_server + "/api/model/create"
        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            data=json.dumps({
                "modelName": name,
                "modelDescription": description,
            }),
        )

        if response.status_code == 200:
            return response.json()["modelId"]
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

    def info(self, model_id: str) -> ModelInfoResponse:
        url = self.ctx.config.api_server + "/api/model/info"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            data=json.dumps({
                "modelId": model_id,
            }),
        )

        if response.status_code == 200:
            LOGGER.debug(f"dataset_info response: {response.json()}")
            return ModelInfoResponse(**response.json())
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

    def delete_files(self, req: DeleteFilesRequest):
        url = self.ctx.config.api_server + "/api/model/file/delete"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            data=json.dumps({
                "filePaths": req.filePaths,
                "modelId": req.id,
                "folders": req.folders,
            }),
        )

        if response.status_code != 200 or (not response.json()["success"]):
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

    def upload_local_file(
            self,
            model_id: str,
            storage_path: str,
            local_file_path: Union[str, Path],
    ):
        self.uploader.upload(
            req=UploadRequest(
                id=model_id,
                path=storage_path,
            ),
            local_file_path=local_file_path,
        )
