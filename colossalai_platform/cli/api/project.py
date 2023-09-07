import json
from dataclasses import dataclass
from typing import List

from colossalai_platform.cli.api.storage import Storage
from colossalai_platform.cli.api.types import Context, ApiError


@dataclass
class ProjectListResponse:
    projectName: str
    projectDescription: str
    createdAt: str
    projectId: str


class Project:

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.storage = Storage(ctx)

    def create(
        self,
        name: str,
        description: str,
    ) -> str:
        url = self.ctx.config.api_server + "/api/project/create"

        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            data=json.dumps({
                "projectName": name,
                "projectDescription": description,
            }),
        )

        if response.status_code == 200:
            return response.json()["projectId"]
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

    def list(self,) -> List[ProjectListResponse]:
        url = self.ctx.config.api_server + "/api/project/list"

        current_page = 1
        merged = []

        while True:
            response = self.ctx.session.post(
                url,
                headers=self.ctx.headers(login=True),
                data=json.dumps({
                    "pager": {
                        "pageSize": 10,
                        "currentPage": current_page,
                    },
                }),
            )

            if response.status_code != 200:
                raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

            merged.extend(response.json()["projects"])

            total_entries = response.json()["pager"]["totalEntries"]
            page_size = response.json()["pager"]["pageSize"]
            if page_size * current_page > total_entries:
                break
            else:
                current_page += 1

        return [ProjectListResponse(**d) for d in merged]
