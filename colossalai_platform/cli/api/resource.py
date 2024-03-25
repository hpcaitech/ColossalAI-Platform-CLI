from dataclasses import dataclass
from typing import List

from colossalai_platform.cli.api.utils.types import Context, ApiError

@dataclass
class GpusResponse:
    gpuType: str
    manufacturer: str
    availableCounts: List[int]

class Resource:
    def __init__(self, ctx: Context):
        self.ctx = ctx

    def gpus(
            self,
            jobType = "job",
            poolType = "public"
    ) -> List[GpusResponse]:
        url = self.ctx.config.api_server + "/api/resource/user/available"
        response = self.ctx.session.post(
            url,
            headers=self.ctx.headers(login=True),
            json={
                "jobType": jobType,
                "poolType": poolType
            }
        )

        if response.status_code == 200:
            return [GpusResponse(**d) for d in response.json()["gpu"]]
        else:
            raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")
