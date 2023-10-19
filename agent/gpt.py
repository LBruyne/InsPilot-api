import openai

import config
from agent.utils import AgentException


def chat(messages, model="gpt-4"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                {"role": "user", "content": messages}
            ],
            temperature=0,
            engine=config.AZURE_DEPLOYMENT_NAME,
            # stream=True
        )
        return response['choices'][0]['message']['content'].replace('\n', ' ').replace(' .', '.').strip()
    except Exception as e:
        raise AgentException(f"调用 GPT 失败：{str(e)}")
