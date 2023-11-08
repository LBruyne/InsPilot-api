from queue import Queue
from threading import Semaphore

import requests

import config
from agent.utils import AgentException
from settings.sd_default import sd_default_options


class SDInstance:
    def __init__(self, url):
        self.url = url


class SDInstancePool:
    def __init__(self, sd_urls):
        self.sd_instances = Queue()
        for url in sd_urls:
            self.sd_instances.put(SDInstance(url))
        self.semaphore = Semaphore(len(sd_urls))

    def text2Image(self, task):
        self.semaphore.acquire()
        sd_instance = self.sd_instances.get()
        try:
            url = sd_instance.url + config.SD_T2I_ENDPOINT
            payload = {
                "prompt": task["prompt"],
                "negative_prompt": task["negative_prompt"],
            }

            payload.update(sd_default_options)

            if task["options"] is not None:
                payload.update(task["options"])

            print("t2i: " + str(task["index"]))
            print(payload)
            r = post_sdapi(url, payload)
            print("t2i res.")
            return {
                "index": task["index"],
                "type": task["task_type"],
                "image": r['images'][0]
            }
        except Exception as e:
            print(f"Error: 调用Stable Diffusion失败，{str(e)}")
            return {
                "index": task["index"],
                "type": task["task_type"],
                "image": ""
            }
        finally:
            self.sd_instances.put(sd_instance)
            self.semaphore.release()


def call_sdapi(url: str, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise AgentException(f"调用 Stable Diffusion 失败，URI {str(url)}，{str(e)}")


def post_sdapi(url: str, payload, headers=None):
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise AgentException(f"调用 Stable Diffusion 失败：URI {str(url)}，{str(e)}")


sd_pool = SDInstancePool(config.SD_ENDPOINTS)
