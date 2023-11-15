from dataclasses import dataclass
from typing import Callable, List, Dict, Any

import requests

from colossalai_platform.cli.api.utils.types import Context,ApiError


@dataclass
class RequestAutoPagerOptions:
    page_size: int = 10


@dataclass
class RequestAutoPager:
    ctx: Context

    def post(
            self,
            url,
            extract_func: Callable[[requests.Response], List],
            json: Dict[str, Any] = None,
            pager_options: RequestAutoPagerOptions = RequestAutoPagerOptions(),
            **kwargs,
    ):
        current_page = 1
        merged_response = []
        while True:
            response = self.ctx.session.post(
                url,
                json={
                    **json,
                    "pager": {
                        "pageSize": pager_options.page_size,
                        "currentPage": current_page,
                    },
                },
                **kwargs
            )

            if response.status_code != 200:
                raise ApiError(f"{url} failed with status code {response.status_code}, body: {response.text}")

            merged_response.extend(extract_func(response))

            total_entries = response.json()["pager"]["totalEntries"]
            page_size = response.json()["pager"]["pageSize"]
            if page_size * current_page > total_entries:
                break
            else:
                current_page += 1

        return merged_response
