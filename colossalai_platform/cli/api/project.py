import logging
import pathlib
from dataclasses import dataclass
from typing import List, Union

from colossalai_platform.cli.api.dataset import DeleteFilesRequest, NoObjectToDeleteError
from colossalai_platform.cli.api.utils.multipart_upload import MultiPartUploader, UploadRequest
from colossalai_platform.cli.api.utils.pager import RequestAutoPager
from colossalai_platform.cli.api.utils.types import Context, ApiError

LOGGER = logging.getLogger(__name__)


@dataclass
class ProjectListResponse:
    projectName: str
    projectDescription: str
    createAt: str
    projectId: str
    tags: List[str]


@dataclass
class ProjectInfoResponse:
    projectName: str
    projectDescription: str
    createAt: str
    projectId: str

@dataclass
class HyperParametersResponse:
    name: str
    type: str
    defaultValue: str
    description: str
    required: bool
    choices: List[str] = None

class ProjectNotFoundError(Exception):

    def __init__(self, project_id: str):
        super().__init__(f"Project {project_id} not found")


class Project:

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.storage = MultiPartUploader(
            ctx,
            self.ctx.config.api_server + "/api/file/project",
        )

    def create(
            self,
            name: str,
            description: str,
    ) -> str:
        url = self.ctx.config.api_server + "/api/project/create"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            json={
                "projectName": name,
                "projectDescription": description,
            },
        )

        if response.status_code == 200:
            return response.json()["projectId"]
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

    def list(self, ) -> List[ProjectListResponse]:
        url = self.ctx.config.api_server + "/api/project/list"

        current_page = 1
        merged = RequestAutoPager(self.ctx).post(
            url,
            headers=self.ctx.headers(login=True),
            extract_func=lambda response: response.json()["projects"],
        )

        LOGGER.debug(f"list response: {merged}")
        return [ProjectListResponse(**d) for d in merged]


    def info(self, project_id: str) -> ProjectInfoResponse:
        url = self.ctx.config.api_server + "/api/project/info"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            json={
                "projectId": project_id,
            },
        )

        if response.status_code == 200:
            LOGGER.debug(f"project_info response: {response.json()}")
            return ProjectInfoResponse(**response.json())
        elif response.status_code == 404:
            if response.json()["message"] == "project not found":
                raise ProjectNotFoundError(project_id)
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")


    def delete_files(self, req: DeleteFilesRequest):
        url = self.ctx.config.api_server + "/api/file/project/delete"

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
            project_id: str,
            storage_path: str,
            local_file_path: Union[str, pathlib.Path],
    ):
        self.storage.upload(
            req=UploadRequest(
                id=project_id,
                path=storage_path,
            ),
            local_file_path=local_file_path,
        )

    def version_list(self, project_id: str) -> List[int]:
        url = self.ctx.config.api_server + "/api/project/version/list"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            json={
                "projectId": project_id,
            },
        )

        if response.status_code == 200:
            return response.json()["versions"]
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

    def hyperparameters(self, project_id: str, version: int) -> List[HyperParametersResponse]:
        url = self.ctx.config.api_server + "/api/project/hyperparameters"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            json={
                "projectId": project_id,
                "version": version,
            },
        )

        if response.status_code == 200:
            return [HyperParametersResponse(**d) for d in response.json()["hyperParameters"]]
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")
