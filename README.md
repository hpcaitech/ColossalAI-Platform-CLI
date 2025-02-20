# 🔮 ColossalAI-Platform-CLI

## 🔗 Table Of Contents

- [🔮 ColossalAI-Platform-CLI](#-colossalai-platform-cli)
  - [🔗 Table Of Contents](#-table-of-contents)
  - [📚 概述](#-overview)
  - [🔨 安装](#-installation)
  - [⌨️ 功能说明](#️-usage)
    - [Create a Template](#create-a-template)

## 📚 概述

ColossalAI Platform CLI 是一个命令行工具，用于访问 ColossalAI 云平台的各种功能。CLI 工具名为 `cap`，代表 `C(olossal)A(I) P(latform)`。该工具旨在为用户提供便捷的界面来使用云平台的功能，提高工作效率。

该 CLI 工具基于 [Click](https://click.palletsprojects.com/en/8.0.x/) 构建，这是一个用于创建优雅的命令行界面的 Python 包。

## 🔨 安装

有两种安装方式：

1. 从源代码安装

```bash
pip install git+https://github.com/hpcaitech/ColossalAI-Platform-CLI@main
```

2. 从 PyPI 安装

```bash
pip install colossalai-platform
```

## ⌨️ 功能说明

### 配置和登录

```bash
cap configure
```

用于配置和登录平台。会提示输入：
- 用户名
- 密码（输入时隐藏）

### 项目管理

项目相关命令用于管理训练和推理项目：

```bash
cap project <command>
```

可用的子命令：
- `init <project-name>`: 初始化一个新的 ColossalAI 项目模板
  - 创建项目目录结构
  - 生成基础文件（train.sh、train.py、HyperParameters.json 等）
- `create`: 创建一个空项目
  - 需要输入项目名称和描述
- `list`: 列出所有项目
- `upload-dir <project-id> <directory>`: 上传整个目录作为项目
  - 会覆盖已有的项目内容
  - 支持 `-y` 参数跳过确认

### 数据集管理

数据集相关命令用于管理训练数据集：

```bash
cap dataset <command>
```

可用的子命令：
- `create`: 创建一个空数据集
  - 需要输入数据集名称和描述
- `list`: 列出所有数据集
- `upload-dir <dataset-id> <directory>`: 上传整个目录作为数据集
  - 会覆盖已有的数据集内容
  - 支持 `-y` 参数跳过确认

### 模型管理

模型相关命令用于管理模型：

```bash
cap model <command>
```

可用的子命令：
- `create`: 创建一个空模型
  - 需要输入模型名称和描述
- `list`: 列出所有模型
  - 支持 `--tag` 参数按标签筛选
- `upload-dir <model-id> <directory>`: 上传整个目录作为模型
  - 会覆盖已有的模型内容
  - 支持 `-y` 参数跳过确认

### 作业管理

作业相关命令用于管理训练作业：

```bash
cap job <command>
```

可用的子命令：
- `list`: 列出所有作业
  - 显示作业名称、ID、状态、描述和创建时间等信息
- `init-yaml`: 初始化作业配置 YAML 文件
  - 必需参数：
    - `--project-id/-p`: 项目 ID（可通过 `cap project list` 查看）
  - 可选参数：
    - `--version/-v`: 项目版本（当有多个版本时必须指定）
    - `--output-path/-o`: 输出文件路径（默认为 job.yaml）
    - `--stdout`: 输出到标准输出而不是文件
- `submit <job-yaml>`: 提交作业
  - 根据 YAML 文件提交训练作业
  - 提交后会显示作业 ID 和详情页面链接

### YAML 配置说明

作业的 YAML 配置文件包含以下主要字段：

```yaml
jobName: "job-name"              # 作业名称
jobDescription: "description"     # 作业描述
image: "image:tag"               # 运行环境镜像
hyperParameters:                  # 超参数配置
  param1: value1
  param2: value2
resourceType: "public"           # 资源类型：public 或 private
gpu:                            # GPU 配置
  gpuType: "NVIDIA-V100"        # GPU 类型
  manufacturer: "Nvidia"        # 制造商
  number: 1                     # GPU 数量
mounts:                         # 挂载配置
  - type: "dataset"            # 类型：dataset、project 或 model
    id: "xxx"                  # 对应资源的 ID
    version: 1                 # 版本号
    mountPath: "/mnt/data"     # 挂载路径
    name: "resource-name"      # 资源名称
    readOnly: true            # 是否只读
launchCommand: "bash /mnt/project/train.sh"  # 启动命令
```

## 🔗 相关链接

- 文档网站：https://docs.platform.luchentech.com/
- 控制台：https://platform.luchentech.com/console

## 📝 注意事项

1. 在使用任何需要登录的命令前，请先运行 `cap configure` 进行登录。
2. 上传目录时请注意，会覆盖目标位置的所有内容。
3. 创建项目时建议使用 `cap project init` 命令，它会生成标准的项目模板。
4. 提交作业前，请仔细检查 YAML 配置文件中的各项参数。
