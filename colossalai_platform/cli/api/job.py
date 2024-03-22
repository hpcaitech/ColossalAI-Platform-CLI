import logging

from colossalai_platform.cli.api.utils.types import Context

LOGGER = logging.getLogger(__name__)

class Job:
    def __init__(self, ctx: Context):
        self.ctx = ctx
