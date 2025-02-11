import os
import time
import google.api_core
import google.api_core.exceptions
import pandas as pd
import csv
import google
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image

VERTEX_GENMODEL = os.getenv('VERTEX_GENMODEL')
genmodel = GenerativeModel(VERTEX_GENMODEL)

def get_text_from_gemini(prompt:list) -> str:
    '''
    geminiにプロンプトを送り、レスポンスからテキストのみを返す
    apiリミットエラーの際3回まで再試行'''
    c = 0
    f = True

    while f:
        try:
            response = genmodel.generate_content(prompt)
            text = response.candidates[0].content.parts[0].text
            f = False
        except google.api_core.exceptions.ResourceExhausted as e:
            if c == 3:  # 3回まで再試行
                break

            c += 1
            print(f'ResourceExhausted error raised. retrying : {c}')
            time.sleep(c*30)

    if f:   # レスポンスを得られなかった場合
        print(e)
        raise google.api_core.exceptions.ResourceExhausted

    return text

def get_markdown(imagepath:str, ocrpath:str):
    '''
    対応するocr結果と画像のパスを渡すとレスポンスを返す'''
    # ロード
    image = Image.load_from_file(imagepath)

    with open(ocrpath) as f:
        text = f.read()

    # プロンプト
    prompt = [
    '下記の文章を構造化してmarkdown形式で出力してください。\n'
    '文章は、添付の画像からOCRで抽出したものです。文章と画像両方を参照して適切な構造化を行ってください。\n'
    'この際、書類のヘッダーと思われる部分は無視し、必要な範囲の文章のみを使用してください。'
    '回答には本文のみを含めるようにしてください。\n\n' + \
    text,
    image
    ]

    # マークダウン化
    text = get_text_from_gemini(prompt)
    return text

def get_keywords(text:str, n_keys:int =3) -> str:
    '''
    1ページ分のテキストからキーワードを抽出する'''
    # プロンプト
    prompt = [
    '下記の文章は、あるpdfファイルの1ページをマークダウン化したものです。'
    f'この文章の見出しから、このページの主題となるキーワードを{n_keys}単語抽出してください。\n'
    '抽出の際は、見出しに使用されている単語を特に重視してください。'
    'この際、企業名はキーワードから除外してください。\n'
    '単語はカンマで区切り、改行は含めずに回答してください。\n'
    f'回答には、{n_keys}単語以外の情報は含めないでください\n\n' + \
    text
    ]

    # 抽出
    keywords = get_text_from_gemini(prompt)
    return keywords.replace('\n', '')

def save_keywords(mddir:str) -> None:
    '''
    mdのディレクトリを渡すとその中のmdファイルごとにキーワードを抽出・csvに保存する'''
    csvname = os.path.join(mddir, 'keywords.csv')

    if os.path.exists(csvname): # 上書きしない
        return

    mdfiles = [f for f in os.listdir(mddir) if f[-3:] == '.md']
    mdfiles.sort()

    l = list()

    for md in mdfiles:  # mdファイルごとの処理
        with open(os.path.join(mddir, md)) as f:
            text = f.read()

        # キーワード抽出
        keyword = get_keywords(text)
        l.append([md, keyword])

        time.sleep(1)

    # csv保存
    df = pd.DataFrame(l, columns=['mdfile', 'keywords'])
    df.to_csv(csvname, index=False, header=True, quoting=csv.QUOTE_ALL)

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

            time.sleep(1)

        save_keywords(pdf_md_dir)
