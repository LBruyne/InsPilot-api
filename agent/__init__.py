import openai

import config

openai.api_key = config.AZURE_OPENAI_KEY
openai.api_base = config.AZURE_OPENAI_ENDPOINT
openai.api_type = 'azure'
openai.api_version = '2023-05-15'

