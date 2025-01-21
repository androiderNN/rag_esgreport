import os
import pypdfium2 as pdfium

import config

def get_text(fname:str) -> str:
    '''
    pdfファイルのパスを渡すとpdfiumで読んだtextを返す'''
    reader = pdfium.PdfDocument(fname)
    text = str()

    for page in reader:
        textpage = page.get_textpage()
        text += textpage.get_text_bounded()
    
    return text

def pdf2text(pdfdir:str, textdir:str) -> None:
    files = os.listdir(pdfdir)
    files = [file for file in files if file[-4:]=='.pdf']

    for file in files:
        # pdfの読み込み
        pdfpath = os.path.join(pdfdir, file)
        print(pdfpath)
        text = get_text(pdfpath)

        # textでの保存
        textpath = os.path.join(textdir, file+'.txt')
        with open(textpath, mode='w') as f:
            f.write(text)

if __name__ == '__main__':
    pdf2text(config.train_pdf_dir, config.train_text_dir)
    pdf2text(config.valid_pdf_dir, config.valid_text_dir)
