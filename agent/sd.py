import base64
import io

import requests
from PIL import Image

import config
from agent.utils import AgentException


def call_sdapi(endpoint: str, params):
    try:
        response = requests.get(config.SD_ENDPOINT + endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise AgentException(f"调用 Stable Diffusion 失败，URI {str(endpoint)}，{str(e)}")


def post_sdapi(endpoint: str, payload, headers=None):
    try:
        response = requests.post(config.SD_ENDPOINT + endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise AgentException(f"调用 Stable Diffusion 失败：URI {str(endpoint)}，{str(e)}")


def text2Image(prompt: str):
    endpoint = config.SD_T2I_ENDPOINT

    payload = {
        "prompt": prompt,
        "steps": 5
    }

    r = post_sdapi(endpoint, payload)
    return r['images'][0]
