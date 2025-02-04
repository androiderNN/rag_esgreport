import os
import time
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image

VERTEX_GENMODEL = os.getenv('VERTEX_GENMODEL')

def get_markdown(imagepath:str, ocrpath:str):
    '''
    対応するocr結果と画像のパスを渡すとレスポンスを返す'''
    # ロード
    image = Image.load_from_file(imagepath)

    with open(ocrpath) as f:
        text = f.read()

    # プロンプト
    # prompt = [
    #     '下記の文章を構造化してmarkdown形式で出力してください。\n'
    #     '文章は、添付の画像からOCRで抽出したものです。文章と画像両方を参照して適切な構造化を行ってください。\n'
    #     '回答には本文のみを含めるようにしてください。\n' + \
    #     text,
    #     image
    # ]

    prompt = [
        '下記の画像から文章を読み取り、その結果を構造化してmarkdown形式で出力してください。\n'
        '回答には本文のみを含めるようにしてください。\n',
        image
    ]

    # マークダウン化
    model = GenerativeModel(VERTEX_GENMODEL)
    response = model.generate_content(prompt)

    return response.candidates[0].content.parts[0].text

def markdownize(imgdir, ocrdir:str, mddir:str) -> None:
    '''
    各パスを指定すると各txt&imgファイルをmdファイルに保存する'''
    if not os.path.exists(mddir):
        os.mkdir(mddir)

    pdfs = [i for i in os.listdir(imgdir) if i[-4:] == '.pdf']

    for pdf in pdfs:
        pdf_img_dir = os.path.join(imgdir, pdf)
        pdf_md_dir = os.path.join(mddir, pdf)
        print(pdf_md_dir)

        if not os.path.exists(pdf_md_dir):
            os.mkdir(pdf_md_dir)

        imgs = [i for i in os.listdir(pdf_img_dir) if i[-4:]=='.jpg']

        for img in imgs:
            # path指定
            imgpath = os.path.join(pdf_img_dir, img)
            ocrpath = os.path.join(ocrdir, pdf, img + '.txt')
            mdpath = os.path.join(pdf_md_dir, img + '.md')

            # 上書きしないよう設定
            if os.path.exists(mdpath):
                continue

            # マークダウン化
            md = get_markdown(imgpath, ocrpath)

            # 保存
            with open(mdpath, mode='w') as f:
                f.write(md)

            time.sleep(10)
