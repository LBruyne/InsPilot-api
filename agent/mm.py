from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch


class Blip2(object):
    def __init__(self, path="/data0/refinity_webui/AI_demo/DM_BLIP2/models/blip2-opt-2.7b", cuda_id=6) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        torch.cuda.set_device(cuda_id)
        self.path = path

    def load_blip2(self):
        self.processor = Blip2Processor.from_pretrained(self.path)
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            self.path, torch_dtype=torch.float16
        )
        self.model.to(self.device)

    def image_caption(self, img_url="tree.jpg"):
        image = Image.open(img_url).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt").to(self.device, torch.float16)
        generated_ids = self.model.generate(**inputs)

        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        print(generated_text)
        return generated_text

    def image_qa(self, prompt="What can you see in the image?", img_url="tree.jpg"):
        prompt = "Question: " + prompt + "? Answer:"

        image = Image.open(img_url).convert("RGB")
        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(self.device, torch.float16)
        generated_ids = self.model.generate(**inputs)

        generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
        print(generated_text)
        return generated_text