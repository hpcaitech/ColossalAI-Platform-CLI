import json
from datetime import datetime
from typing import List, Dict, Any

from pydantic import Field

from colossalai_platform.cli.api import job
from colossalai_platform.cli.api.job import ImagesResponse, JobCreateRequest
from colossalai_platform.cli.api.project import HyperParametersResponse
from colossalai_platform.cli.api.resource import GpusResponse
from colossalai_platform.cli.utils.pydantic_model_with_yaml_comment import ModelWithYamlComment
from colossalai_platform.cli.utils.strings import generate_random_string, yaml_dump_dataclass


class MountType(ModelWithYamlComment):
    type: str
    id: str
    version: int
    mountPath: str
    name: str
    readOnly: bool


class Gpu(ModelWithYamlComment):
    gpuType: str
    manufacturer: str
    number: int


class JobYaml(ModelWithYamlComment):
    jobName: str = "from-project-{xx}"
    jobName_comment_eol_: str = "change to your job name"

    jobDescription: str = "from project {xx}"
    jobDescription_comment_eol_: str = "change to your job description"

    image: str = "change/to/your/image:latest"
    image_comment_before_: str = ""

    hyperParameters: Dict[str, str] = Field(default_factory=dict)
    hyperParameters_comment_after_: str = ""

    resourceType: str = "public"
    resourceType_comment_eol_: str = "Options: [public, private]"

    gpu: Gpu = Field(default_factory=lambda: Gpu(gpuType="NVIDIA-V100", manufacturer="Nvidia", number=1))
    gpu_comment_after_: str = ""

    mounts: List[MountType] = []
    mounts_comment_after_: str = ""

    launchCommand: str = "bash /mnt/project/train.sh"

    def to_api_req(self) -> JobCreateRequest:
        return JobCreateRequest(
            jobName=self.jobName,
            jobDescription=self.jobDescription,
            launchCommand=self.launchCommand,
            image=self.image,
            poolType=self.resourceType,
            gpuType=self.gpu.gpuType,
            numberOfGpu=self.gpu.number,
            manufacturer=self.gpu.manufacturer,
            hyperParameters=json.dumps(self.hyperParameters),  # json string
            mounts=[job.MountType(
                type=m.type,
                id=m.id,
                version=m.version,
                mountPath=m.mountPath,
                name=m.name,
                readOnly=m.readOnly
            ) for m in self.mounts],
        )


def new_job_yaml(
        project_id: str,
        version: int,
        hyperparameters: List[HyperParametersResponse],
        images: List[ImagesResponse],
        gpus: List[GpusResponse],
        project_mount: MountType
) -> JobYaml:
    image_comment = f"""Available images:
{yaml_dump_dataclass(images)}
############################
# Example of this section: #
############################
image: nexus.platform.colossalai.com/base/colossal-ai:cuda11.8-torch2.1.0
"""

    hyperparameters_comment = f"""Available hyperparameters specs:
{yaml_dump_dataclass(hyperparameters)}
############################
# Example of this section: #
############################
strategy: ddp
model: opt
"""

    gpu_comment = f"""Available GPU types:
{yaml_dump_dataclass(gpus)}
############################
# Example of this section: #
############################
gpuType: NVIDIA-V100
manufacturer: Nvidia
number: 1
"""

    mounts_comment = """For more storage information,
run `cap dataset list`, `cap project list`, or `cap model list`.
############################
# Example of this section: #
############################
- type: dataset     # Options: [dataset, project, model]
  id: {dataset-id}  # from `cap dataset list` or the web console
  name: my-project
  version: 1        # omit to use latest
  mountPath: /mnt/project
  readOnly: false
"""

    return JobYaml(
        jobName=f"job-{generate_random_string(5)}-from-project-{project_id}-version-{version}",
        jobDescription=f"From project {project_id}, yaml created by cli at {datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}",
        image_comment_before_=image_comment,
        hyperParameters={
            h.name: h.defaultValue
            for h in hyperparameters
        },
        hyperParameters_comment_after_=hyperparameters_comment,
        gpu_comment_after_=gpu_comment,
        mounts_comment_after_=mounts_comment,
        mounts=[project_mount]
    )
