import os
import pickle
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

def get_concatted_text(fname:str, txtdirname:str) -> str:
    '''
    ページごとに分割されたテキストファイルの中身を連結して返す'''
    # pdfのファイル名からgcloudのレスポンスが格納されたディレクトリの名前を作成する
    # あまりよい実装ではない
    fname = fname.split('/')
    fname[-2] = txtdirname
    sourcedir = os.path.join('/', *fname)

    if not os.path.exists(sourcedir):
        print(f'path {sourcedir} not exist')
        raise FileNotFoundError

    # mdファイルもあるため拡張子によるフィルターなし
    files = os.listdir(sourcedir)
    text = ''

    for file in files:
        sourcepath = os.path.join(sourcedir, file)

        # テキスト以外のファイルが存在したときの保険
        try:
            with open(sourcepath) as f:
                text += f.read()
        except Exception as e:
            f = input(f'while loading {sourcepath} an error occured. skip?(y/n)') == 'y'
            
            if f:
                continue
            else:
                raise e

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
        # text = get_text_pypdf(pdfpath)
        # text = get_concatted_text(pdfpath, 'docs_ocr')
        text = get_concatted_text(pdfpath, 'docs_markdown')

        # textでの保存
        textpath = os.path.join(textdir, file+'.txt')
        with open(textpath, mode='w') as f:
            f.write(text)
