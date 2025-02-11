import os
import time
from google.api_core.exceptions import ResourceExhausted
from vertexai.preview.generative_models import GenerativeModel, Image

from . import make_prompt

VERTEX_GENMODEL = os.getenv('VERTEX_GENMODEL')
MODEL = GenerativeModel(VERTEX_GENMODEL, system_instruction=make_prompt.GEMINI_SYSTEM_PROMPT)

def getresponse(prompt):
    '''
    geminiでの回答を得る'''
    try:
        response = MODEL.generate_content(prompt)
        text = response.candidates[0].content.parts[0].text
    except ResourceExhausted:
        time.sleep(30)
        response = MODEL.generate_content(prompt)
        text = response.candidates[0].content.parts[0].text

    # 末尾の読点を削除
    text = text[:-1] if text[-1] == '、' else text

    return text
