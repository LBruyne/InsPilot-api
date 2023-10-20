from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch

from io import BytesIO


class Blip2(object):
    def __init__(self, path="/data0/refinity_webui/AI_demo/DM_BLIP2/models/blip2-opt-2.7b", cuda_id=0) -> None:
        # self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # torch.cuda.set_device(cuda_id)
        # self.path = path
        self.model = None
        self.processor = None

    def load_blip2(self):
        self.processor = Blip2Processor.from_pretrained(self.path)
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            self.path, torch_dtype=torch.float16
        )
        self.model.to(self.device)

    def image_caption(self, img_data=None):
        image = Image.open(BytesIO(img_data)).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt").to(self.device, torch.float16)
        generated_ids = self.model.generate(**inputs)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

        return generated_text

    def image_qa(self, img_data=None, prompt="What can you see in the image?"):
        prompt = "Question: " + prompt + "? Answer:"
        image = Image.open(BytesIO(img_data)).convert("RGB")
        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(self.device, torch.float16)
        generated_ids = self.model.generate(**inputs)
        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

        return generated_text


mm_blip_2 = Blip2()


# mm_blip_2.load_blip2()

def image_qa(img_data, prompt: str = "What can you see in the image?"):
    return mm_blip_2.image_qa(img_data, prompt=prompt)
