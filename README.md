# 🔮 ColossalAI-Platform-CLI

## 🔗 Table Of Contents

- [🔮 ColossalAI-Platform-CLI](#-colossalai-platform-cli)
  - [🔗 Table Of Contents](#-table-of-contents)
  - [📚 Overview](#-overview)
  - [🔨 Installation](#-installation)
  - [⌨️ Usage](#️-usage)
    - [Create a Template](#create-a-template)

## 📚 Overview

This repository contains the Command Line Tools for the ColossalAI Platform. 
The CLI is called `cap` which stands for `C(olossal)A(I) P(latform)`.
This CLI aims to provide an interface for users to access the various functions provided on the cloud platform and boost their productivity. 


The CLI is built on top of [Click](https://click.palletsprojects.com/en/8.0.x/), a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.


## 🔨 Installation

1. From Source

```bash
pip install git+https://github.com/hpcaitech/ColossalAI-Platform-CLI@main
```

2. From PyPI (**Not Available Yet**)
```bash
pip install colossalai-platform
```

## ⌨️ Usage 

A documentation website will be built when this CLI is mature.
Before that, you can refer to the following sections to use the CLI.

### Create a Template

```bash
cap template init <template-name>
```