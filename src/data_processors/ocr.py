import os
import shutil
from pypdf import PdfReader
import pdf2image

def pdf2jpg(pdfpath:str, imgpath:str) -> None:
    '''
    pdfファイルを1ページごとにjpgとして保存する'''
    # ファイル名のジェネレータ
    def imgname_gen():
        i = 1
        while True:
            yield '{:03d}.jpg'.format(i)
            # yield ''
            i += 1

    # 保存先のディレクトリが存在した場合、削除して作り直す
    if os.path.exists(imgpath):
        shutil.rmtree(imgpath)

    os.mkdir(imgpath)

    pdf = PdfReader(pdfpath)
    num_pages = pdf.get_num_pages()
    ng = iter(imgname_gen())
    page_range = 10 # =スレッド数

    # 一括で変換すると落ちるので、数ページずつ分割して処理
    for i in range(0, num_pages, page_range):
        pdf2image.convert_from_path(
            pdf_path=pdfpath,
            output_folder=imgpath,
            output_file=ng,
            first_page=i,
            last_page=i+page_range-1,
            fmt='jpg',
            dpi=200,
            thread_count=page_range,
            paths_only=True
        )

    # popplerの仕様？により指定したファイル名の末尾に-01.jpg等の接尾辞がつくので削除する
    images = [i for i in os.listdir(imgpath) if i[-4:]=='.jpg']

    for iname in images:
        os.rename(os.path.join(imgpath, iname), os.path.join(imgpath, iname.split('-')[0]))

def save_jpg(pdf_path:str, img_path:str) -> None:
    '''
    forループで各pdfファイルをjpgに変換'''
    pdffiles = [f for f in os.listdir(pdf_path) if f[-4:]=='.pdf']

    for pdf in pdffiles:
        print(os.path.join(pdf_path, pdf))
        pdf2jpg(os.path.join(pdf_path, pdf), os.path.join(img_path, pdf))
