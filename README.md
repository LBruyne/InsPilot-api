# Refinity-api

API server for Refinity。

## Intro

### 主要依赖

- `python / conda`。运行 `python --version` 来检查是否已经安装 `python`。 也可以使用 `conda` 来创建一个 python 虚拟环境。开发环境中的 python 版本为 3.9.18，由于一些依赖的兼容性，不能使用 3.11 以上版本的 python。
- `Flask`。轻量级的后端 API 服务框架。
- `pymongo`。使用 python 与 MongoDB 数据库进行交互的插件。
- `MongoDB`。非关系型数据库，用于保存用户和每次实验的数据（包括文本和图片）。
- `openai`。与 openai 服务进行交互的插件。

此外，还有一些依赖是通过 `pip` 和 `conda` 进行安装的，见 `./environment.yml`。

### 项目架构

项目结构如下：

``` sh
├── agent
├── app.py
├── apps
├── config.py
├── environment.yml
├── __pycache__
├── README.md
├── settings
└── uwsgi.ini
```

- `app.py` 是项目的入口。在里面可以配置程序的端口等信息。

- 路由位于 `./apps/routes.py` 中，可以按照类似的方式简便地添加新的路由和路由集合（见 `https://flask.palletsprojects.com/en/3.0.x/blueprints/` ）。

- 设计人员可以在 `./settings` 中编写 prompts，开发人员可以使用模版方便地在程序中动态调用 prompts。

- 后端的业务逻辑位于 `apps/${app_name}` 中。目前仅有一个应用。如果需要加入新的应用，可以新建文件夹并加入逻辑。同时请记得在 `./config.py` 中加入新的 APP_ID。

- 算法的调用模块位于 `agent` 目录下。目前支持对于Stable Diffustion和GPT的调用。其中，SD模块包含一个实例池，允许负载均衡地调用多个SD实例，来提高生成效率（相应的需要启动多个SD实例）。

- 配置文件位于 `./config.py` 中，可以修改的配置内容包括：
    - APP ID。
    - Stable Diffusion 服务的 API 路径。
    - Azure 提供的 OpenAI GPT 服务相关配置。
    - 数据库的相关配置。

## Quick start

1. 建立环境并安装依赖（如果已经有环境，可以直接安装依赖）。
运行 `conda env create -f environment.yml` 即可。

2. 确保后端的各种服务正常运行且各项配置正确，服务可以访问：

    - Stable Diffusion
    - Azure 的 GPT 服务
    - MongoDB 数据库已经启动。

3. 在 `conda` 虚拟环境中启动项目：`python app.py`。默认项目会启动在 `localhost:5000` 端口，可以在 `app.py` 中进行修改。

<!-- 4. 也可以使用 uWSGI 来实现让 Flask 程序在生产环境中一直运行的效果：首先 `pip install uwsgi` 安装服务器，然后 `nohup uwsgi --ini uwsgi.ini &` 来启动服务。这样可以通过 uwsgi 来访问服务器（此时端口为 `.int` 文件中配置的端口）。 -->