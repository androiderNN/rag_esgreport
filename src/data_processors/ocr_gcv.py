import os
import time
import pickle
from google.cloud import vision

def get_response(path:str):
    '''
    google cloud vision apiでocrリクエストを送り、そのレスポンスを返す'''
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text

def save_ocr(imgdir:str, ocrdir:str) -> None:
    '''
    画像と保存先のパスを渡すと、各画像のocr結果の生データをpickleで保存する'''
    pdflist = [i for i in os.listdir(imgdir) if os.path.isdir(os.path.join(imgdir, i))]

    for pdf in pdflist: # pdfファイルのループ
        pdf_imgdir = os.path.join(imgdir, pdf)  # あるpdfの画像が格納されたディレクトリ
        pdf_ocrdir = os.path.join(ocrdir, pdf)  # あるpdfのocr結果を格納するディレクトリ

        print(pdf_imgdir)
        
        if not os.path.exists(pdf_ocrdir):
            os.mkdir(pdf_ocrdir)
        
        imglist = [i for i in os.listdir(pdf_imgdir) if i[-4:]=='.jpg']
        
        for img in imglist: # 画像ファイルのループ
            imgpath = os.path.join(pdf_imgdir, img)
            ocrpath = os.path.join(pdf_ocrdir, img+'.txt')

            if os.path.exists(ocrpath): # apiの節約
                continue

            # ocrと結果の保存
            text = get_response(imgpath)

            with open(ocrpath, mode='w') as f:
                f.write(text)

            time.sleep(0.5)
