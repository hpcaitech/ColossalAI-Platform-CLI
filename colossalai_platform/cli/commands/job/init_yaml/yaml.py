from typing import List, Dict, Any

from pydantic import Field

from colossalai_platform.cli.utils.pydantic_model_with_yaml_comment import ModelWithYamlComment

class MountType(ModelWithYamlComment):
    type: str
    id: str
    version: int
    mountPath: str
    name: str
    readOnly: bool

class Gpu(ModelWithYamlComment):
    gpuType: str
    gpuType_comment_eol_: str = "Available: [NVIDIA-V100, NVIDIA-T4]"

    manufacturer: str
    manufacturer_comment_eol_: str = ""

    number: int
    number_comment_eol_: str = ""

class JobYaml(ModelWithYamlComment):
    jobName: str = "from-project-{xx}"
    jobDescription: str = "from project {xx}"

    image: str = "placeholder"
    image_comment_before_: str = """Available images:
- name: nexus.platform.colossalai.com/base/colossal-ai:cuda11.8-torch2.1.0
  description: image for colossalai 0.3.4
- name: nexus.platform.colossalai.com/hpcaitech/pytorch-npu:2.1.0
  description: image for training on huawei npu
############################
# Example of this section: #
############################
image: nexus.platform.colossalai.com/base/colossal-ai:cuda11.8-torch2.1.0
"""

    hyperParameters: Dict[str, Any] = Field(default_factory=lambda: {
        "key": "value"
    })
    hyperParameters_comment_after_: str = """Available hyperparameters:
{
    "name": "strategy",
    "type": "",
    "defaultValue": "colossalai_zero2",
    "description": "Options for ColossalAI strategies to optimize your training process",
    "choices": [
        "colossalai_zero2_cpu",
        "colossalai_zero2",
        "colossalai_gemini",
        "ddp"
    ],
    "required": false
},
{
    "name": "model",
    "type": "",
    "defaultValue": "opt",
    "description": "The type of LLM model that you want to use in training",
    "choices": [
        "bloom",
        "opt",
        "gpt2",
        "llama2",
        "chatglm"
    ],
    "required": false
},
############################
# Example of this section: #
############################
- strategy: ddp
- model: opt
"""

    resourceType: str = "public"
    resourceType_comment_eol_: str = "Option: [public, private]"

    gpu: Gpu = Field(default_factory=lambda: Gpu(gpuType="NVIDIA-V100", manufacturer="Nvidia", number=1))
    gpu_comment_after_: str = """############################
# Example of this section: #
############################
gpuType: NVIDIA-V100
manufacturer: Nvidia
number: 1
"""

    mounts: List[MountType] = Field(default_factory=lambda: [
        MountType(type="dataset", id="placeholder", version=1, mountPath="/data", name="placeholder", readOnly=True),
    ])
    mounts_comment_after_: str = """############################
# Example of this section: #
############################
- type: project
  id: my-project
  version: 1
  mountPath: /mnt/project
  name: my-project
  readOnly: false
"""

    launchCommand: str = "bash /mnt/project/train.sh"
