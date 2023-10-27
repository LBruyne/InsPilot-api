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

### 数据传输

前后端的数据传输使用标准的HTTP请求规范完成。所有需要对数据库进行更改，或者需要使用生成能力的接口都使用 `POST` 请求，其它查询接口使用  `GET` 请求。

当前端需要使用 `POST` 传输文本数据到后端时，在请求体（Body）中以JSON的形式传输数据（即前端需要在请求头（Header）中加入 `"Content-Type": "application/json"`。一个前端请求示例如下：

```javascript
const res = await fetch(`${baseUrl}/paint/start`, {
    method: "POST",
    body: JSON.stringify({
        username
    }),
    headers: {
        "Content-Type": "application/json",
    },
});
```

相应的，后端需要在对应的路由的处理方法中，从请求体中拿到相应的数据，并完成后续的逻辑：

```python
@apps.route('/paint/start', methods=['POST'])
def paintStart():
    try:
        username = request.json.get('username')
        if username == '':
            raise BusinessException(BUSINESS_FAIL, '用户名字为空')
        ... 
```

注意：目前项目中所有传输都是使用JSON格式完成的。如果需要传输图片文件，需要在前端获取文件的BASE64编码，并以字符串的形式将
图片传输到后端。这种方式更加适合可能需要传输多个图片的需求。

### 大模型能力调用

系统目前采用了GPT和Stable Diffusion两个大模型的能力。代码位于 `agent` 目录下。

- GPT。文本生成能力使用Open AI提供的GPT4。项目中使用Azure提供的 API 接口进行访问。实现了 `chat` 接口，能够提供prompts来生成需要的文本。
- SD。图片生成能力使用SD。为了运行项目，需要首先在本地搭建SD服务，运行SD实例，项目通过SD的API接口来使用图片生成能力。实现了：
    - `call_sdapi` 和 `post_sdapi` 两个接口，分别对应使用 `GET` 和 `POST` 方法调用SD服务的API接口。基于此接口，可以封装其它具体的功能接口，如 `text2Image`。
    - `text2Image` 接口，基于 `post_sdapi` ，调用SD的根据文本生成图片的能力。

    在实现SD时，为了允许系统同时使用多个SD实例的能力，我们封装了一个SD实例池（SDInstancePool），相关代码位于 `agent/sd/py` 中。该实例池接受配置文件中提供的SD实例完成初始化。在使用SD的功能时，实例池会自动分配空闲的SD实例去运行相关的SD任务，并在所有实例都在运行时，阻塞其它的生成任务（直到有实例空闲）。


## Quick start

1. 建立环境并安装依赖（如果已经有环境，可以直接安装依赖）。
运行 `conda env create -f environment.yml` 即可。

2. 确保后端的各种服务正常运行且各项配置正确，服务可以访问：

    - Stable Diffusion
    - Azure 的 GPT 服务
    - MongoDB 数据库已经启动。

3. 在 `conda` 虚拟环境中启动项目：`python app.py`。默认项目会启动在 `localhost:5000` 端口，可以在 `app.py` 中进行修改。

<!-- 4. 也可以使用 uWSGI 来实现让 Flask 程序在生产环境中一直运行的效果：首先 `pip install uwsgi` 安装服务器，然后 `nohup uwsgi --ini uwsgi.ini &` 来启动服务。这样可以通过 uwsgi 来访问服务器（此时端口为 `.int` 文件中配置的端口）。 -->