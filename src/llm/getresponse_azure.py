import os
from openai import AzureOpenAI

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
API_VERSION = os.getenv("API_VERSION")
DEPLOYMENT_ID_FOR_CHAT_COMPLETION = os.getenv("DEPLOYMENT_ID_FOR_CHAT_COMPLETION")

CLIENT = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=API_VERSION
)

def getresponse(prompt):
    response = CLIENT.chat.completions.create(
        model=DEPLOYMENT_ID_FOR_CHAT_COMPLETION,
        messages=prompt,
        max_tokens=4000,     # 応答に使えるトークン数上限
        temperature=0.7,     # 創造性（0~1）
        top_p=0.95,          # nucleus sampling
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    ).choices[0].message.content  # 応答本文

    return response
