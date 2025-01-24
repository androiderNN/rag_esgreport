import os
from pypdf import PdfReader
import pypdfium2 as pdfium

def get_text_pypdf(fname:str) -> str:
    '''
    pdfファイルのパスを渡すとpypdfで読んだtextを返す'''
    reader = PdfReader(fname)
    text = str()

    for page in reader.pages:
        text += page.extract_text()
    
    return text

def get_text_pdfium(fname:str) -> str:
    '''
    pdfファイルのパスを渡すとpdfiumで読んだtextを返す'''
    reader = pdfium.PdfDocument(fname)
    text = str()

    for page in reader:
        textpage = page.get_textpage()
        text += textpage.get_text_bounded()
    
    return text

def pdf2text(pdfdir:str, textdir:str) -> None:
    '''
    元データのディレクトリと保存先のディレクトリを指定するとpdfをtxtに変換する'''
    files = os.listdir(pdfdir)
    files = [file for file in files if file[-4:]=='.pdf']

    for file in files:
        # pdfの読み込み
        pdfpath = os.path.join(pdfdir, file)
        print(pdfpath)
        # text = get_text_pdfium(pdfpath)
        text = get_text_pypdf(pdfpath)

        # textでの保存
        textpath = os.path.join(textdir, file+'.txt')
        with open(textpath, mode='w') as f:
            f.write(text)
