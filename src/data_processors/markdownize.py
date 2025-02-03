import os
import pickle
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image

from . import ocr_gcv

VERTEX_GENMODEL = os.getenv('VERTEX_GENMODEL')

def get_markdown(ocrpath:str, imagepath:str):
    '''
    対応するocr結果と画像のパスを渡すとレスポンスを返す'''
    text = ocr_gcv.extract_text(pickle.load(ocrpath, 'rb'))
    image = Image.load_from_file(imagepath)

    prompt = [
        '下記の文章を構造化してmarkdown形式で出力してください。\n'
        '文章は、添付の画像からOCRで抽出したものです。文章と画像両方を参照して適切な構造化を行ってください。\n'
        '回答には本文のみを含めるようにしてください。\n' + \
        text,
        image
    ]
    
    model = GenerativeModel(VERTEX_GENMODEL)
    response = model.generate_content(prompt)

    return response

def extract_markdown(response) -> str:
    '''
    google cloudのレスポンスからmarkdownを抽出する'''
    return response.candidates[0].content.parts[0].text

def markdownize(imgdir, ocrdir:str, mddir:str) -> None:
    '''
    各パスを指定すると各txt&imgファイルをmdファイルに保存する'''
    pdfs = [i for i in os.listdir(imgdir) if i[-4:] == '.pdf']

    for pdf in pdfs:
        imgs = [i for i in os.listdir(os.path.join(imgdir, pdf)) if i[-4:]=='jpg']

        for img in imgs:
            imgpath = os.path.join(imgdir, pdf, img)
            ocrpath = os.path.join(ocrdir, pdf, img + '.pkl')
            mdpath = os.path.join(mddir, pdf, img + '.md')



