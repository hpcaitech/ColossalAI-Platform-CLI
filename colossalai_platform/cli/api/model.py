from typing import List
from dataclasses import dataclass, field
import json
import logging

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

class Model:

    def __init__(self, ctx: Context):
        self.ctx = ctx

    def list(
            self,
            tags: List[str],
            is_owned=True,
    ) -> List[ModelListResponse]:
        url = self.ctx.config.api_server + "/api/model/list"

        # TODO(ofey404): extract duplicated code as a function
        current_page = 1
        merged_datasets = []
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

            merged_datasets.extend(response.json()["models"])

            total_entries = response.json()["pager"]["totalEntries"]
            page_size = response.json()["pager"]["pageSize"]
            if page_size * current_page > total_entries:
                break
            else:
                current_page += 1

        LOGGER.debug(f"list response: {merged_datasets}")
        return [ModelListResponse(**d) for d in merged_datasets]

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
