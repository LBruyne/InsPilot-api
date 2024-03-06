# InsPilot-api

API server for [InsPilot](https://github.com/LBruyne/InsPilot).

## Introduction

### Main Dependencies

- `python / conda`: Run `python --version` to check if `python` is already installed. You can also use `conda` to create a python virtual environment. The python version in the development environment is 3.9.18; due to compatibility issues with some dependencies, python versions above 3.11 cannot be used.
- `Flask`: A lightweight backend API service framework.
- `pymongo`: A plugin used for interacting with MongoDB databases in Python.
- `MongoDB`: A NoSQL database used to save user data and data from each experiment (including text and images).
- `openai`: A plugin for interacting with OpenAI services.

Additionally, some dependencies are installed using `pip` and `conda`, see `./environment.yml`.

### Project Architecture

The project structure is as follows:

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


- `app.py` is the entry point of the project. Here you can configure the port and other settings for the application.
- Routing is located in `./apps/routes.py`, where you can easily add new routes and route collections (see `https://flask.palletsprojects.com/en/3.0.x/blueprints/`).
- Designers can write prompts in `./settings`, and developers can dynamically call these prompts in the program using templates.
- Backend business logic is located in `apps/${app_name}`. Currently, there is only one application. If you need to add a new application, create a new folder and add logic. Also, remember to add the new APP_ID in `./config.py`.
- The algorithm invocation module is located in the `agent` directory. Currently, it supports calls to Stable Diffusion and GPT. The SD module includes an instance pool, allowing the balanced invocation of multiple SD instances to improve generation efficiency (requiring the start-up of multiple SD instances).
- Configuration files are located in `./config.py`, where configurable contents include:
    - APP ID.
    - API path for Stable Diffusion service.
    - Configuration related to Azure's OpenAI GPT service.
    - Database-related configurations.

### Data Transfer

The front-end and back-end data transfer completes using the standard HTTP request specifications. All interfaces that need to change the database or use generation capabilities use `POST` requests, while other querying interfaces use `GET` requests.

When the front end needs to transfer text data to the back end using `POST`, it transmits data in JSON format in the request body (thus the front end needs to include `"Content-Type": "application/json"` in the request header). An example of a front-end request is as follows:

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

Correspondingly, the backend needs to retrieve the relevant data from the request body in the route's handling method and complete the subsequent logic:

```python
@apps.route('/paint/start', methods=['POST'])
def paintStart():
    try:
        username = request.json.get('username')
        if username == '':
            raise BusinessException(BUSINESS_FAIL, 'Username is empty')
        ...
```

Note: Currently, all data transfers in the project are completed using the JSON format. If you need to transfer image files, you should get the BASE64 encoding of the file on the front end and transfer the image to the back end as a string. This method is more suitable for scenarios that may need to transfer multiple images.

### LLM Capability Invocation

The system currently utilizes the capabilities of two large models: GPT and Stable Diffusion, with code located in the `agent` directory.

- GPT: The text generation capability uses Open AI's GPT4, accessed via Azure's API. The `chat` interface is implemented to provide prompts needed to generate the required text.
- SD: Image generation capability uses SD. To run the project, you first need to set up the SD service locally and run SD instances; the project uses SD's API interface for image generation capabilities. Implemented are:：
    - `call_sdapi` and `post_sdapi` interfaces, corresponding to the GET and POST methods for calling the SD service's API interface. Based on these interfaces, other specific functional interfaces can be encapsulated, such as `text2Image`.
    - `text2Image` interface, based on `post_sdapi`, calls SD's ability to generate images from text.

In implementing SD, to allow the system to use multiple SD instances simultaneously, we have wrapped an SD instance pool (`SDInstancePool`), and the related code is located in agent/sd/py. The instance pool initializes using SD instances provided in the configuration file. When using SD functionalities, the instance pool automatically allocates an idle SD instance to run the related SD tasks and blocks other generation tasks when all instances are running (until an instance becomes idle).

## Quick Start

1. Create the environment and install dependencies (if the environment is already set up, directly install the dependencies). Run `conda env create -f environment.yml` for setup.

2. Switch to the installed `conda` environment with `conda activate $env_name`.

3. Ensure that various backend services are correctly running and configurations are accurate; services should be accessible:
    - Stable Diffusion
    - Azure's GPT service
    - MongoDB database is already started.

4. Start the project in the `conda` virtual environment: `python app.py`. By default, the project will launch on `localhost:5000`, which can be modified in `app.py`.

5. Alternatively, you can use gunicorn to keep the Flask program running continuously in a production environment: first install the server with `pip install gunicorn`, then start the service with `nohup gunicorn -w 4 app:app &`. This will ignore hangup signals and run the Gunicorn process in the background.
