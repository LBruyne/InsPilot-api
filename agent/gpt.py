import openai
from queue import Queue
from threading import Semaphore
import config
import requests

from agent.utils import AgentException
        
class GPTInstance:
    def __init__(self):
        pass
        
        
class GPTInstancePool:
    def __init__(self, instance_num):
        self.gpt_instances = Queue()
        for _ in range(instance_num):
            self.gpt_instances.put(GPTInstance())
        self.semaphore = Semaphore(instance_num)

    def chat(self, task):
        self.semaphore.acquire()
        gpt_instance = self.gpt_instances.get()
        try:
            print("chat: ")
            print(task["messages"])
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    # {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                    {"role": "user", "content": task["messages"]}
                ],
                temperature=0,
                # engine=config.AZURE_DEPLOYMENT_NAME,
                # stream=True
            )
            r = response['choices'][0]['message']['content'].replace('\n', ' ').replace(' .', '.').strip()
            return {
                "text": r
            }
        except Exception as e:
            print(f"Error: 调用GPT生成文本失败，{str(e)}")
            return {
                "text": ""
            }
        finally:
            self.gpt_instances.put(gpt_instance)
            self.semaphore.release()     

    def text2Image(self, task):
        self.semaphore.acquire()
        gpt_instance = self.gpt_instances.get()
        try:
            print("t2i: " + str(task["index"]))
            print(task["prompt"])
            response = openai.Image.create(
                model="dall-e-3",
                prompt=task["prompt"],
                size="1024x576",
                quality="standard",
                n=1,
            )
            r = response.data[0].url
            print("t2i res: " + str(r))
            return {
                "index": task["index"],
                "type": task["task_type"],
                "image": r
            }
        except Exception as e:
            print(f"Error: 调用GPT文生图失败，{str(e)}")
            return {
                "index": task["index"],
                "type": task["task_type"],
                "image": ""
            }
        finally:
            self.gpt_instances.put(gpt_instance)
            self.semaphore.release()       
    
    def ask_image(self, task):
        self.semaphore.acquire()
        gpt_instance = self.gpt_instances.get()
        try:
            print("ask image: ")
            print(task["prompt"])
            print(task['images']) # images 是一个列表，里面每张图片是 B64编码
            
            images_content = [{
                "type": "image_url",
                "image_url": {
                    "url": f"{image}"
                }
            } for image in task['images']]
        
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            *images_content, 
                            {
                                "type": "text",
                                "text": task["prompt"]
                            },
                        ]
                    }
                ],
                max_tokens=300,
            )
            # print(response)

            r = response['choices'][0]['message']['content'].replace('\n', ' ').replace(' .', '.').strip()
            print("ask image res: " + str(r))
            return {
                "text": r
            }
        except Exception as e:
            print(f"Error: 调用GPT图片提问失败，{str(e)}")
            return {
                "text": ""
            }
        finally:
            self.gpt_instances.put(gpt_instance)
            self.semaphore.release()       

gpt_pool = GPTInstancePool(config.OPENAI_GPT_INSTANCE)