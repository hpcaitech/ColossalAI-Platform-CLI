import logging
from dataclasses import dataclass
from typing import List

from pydantic import BaseModel

from colossalai_platform.cli.api.utils.pager import RequestAutoPager
from colossalai_platform.cli.api.utils.types import Context, ApiError

LOGGER = logging.getLogger(__name__)

@dataclass
class JobListResponse:
    jobName: str
    jobDescription: str
    jobStatus: str
    jobId: str
    createdAt: str
    updatedAt: str

@dataclass
class ImagesResponse:
    displayName: str
    url: str
    description: str

class MountType(BaseModel):
    type: str
    id: str
    version: int
    mountPath: str
    name: str
    readOnly: bool

class JobCreateRequest(BaseModel):
    jobName: str
    jobDescription: str
    launchCommand: str
    image: str
    poolType: str
    gpuType: str
    numberOfGpu: int
    manufacturer: str
    hyperParameters: str
    mounts: List[MountType]

class JobCreateResponse(BaseModel):
    jobId: str
    podNames: List[str]

class Job:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    def list(
            self,
            status_type: str = "All",
    ) -> List[JobListResponse]:
        url = self.ctx.config.api_server + "/api/job/list"

        # TODO(ofey404): Add a limit and pagination
        merged = RequestAutoPager(self.ctx).post(
            url,
            headers=self.ctx.headers(login=True),
            json={"statusType": status_type},
            extract_func=lambda response: response.json()["jobs"],
        )

        LOGGER.debug(f"list response: {merged}")
        return [JobListResponse(**d) for d in merged]

    def images(self) -> List[ImagesResponse]:
        url = self.ctx.config.api_server + "/api/job/images"

        response = self.ctx.session.get(
            url,
            headers=self.ctx.headers(login=True),
        )

        if response.status_code == 200:
            return [ImagesResponse(**d) for d in response.json()["images"]]
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

    def create(self, req: JobCreateRequest) -> JobCreateResponse:
        url = self.ctx.config.api_server + "/api/job/create"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            json=req.model_dump(),  # to dict
        )

        if response.status_code == 200:
            return JobCreateResponse(**response.json())
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")
