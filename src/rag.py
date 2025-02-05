import sys
import os
import shutil
import subprocess
import csv
import pandas as pd
import time
import datetime
import tiktoken
from dotenv import load_dotenv

load_dotenv()

import config
from data_processors import company_extractor, database
from llm import make_prompt, getresponse_azure

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
API_VERSION = os.getenv("API_VERSION")
DEPLOYMENT_ID_FOR_CHAT_COMPLETION = os.getenv("DEPLOYMENT_ID_FOR_CHAT_COMPLETION")
DEPLOYMENT_ID_FOR_EMBEDDING = os.getenv("DEPLOYMENT_ID_FOR_EMBEDDING")

def clean_answer(answer:str) -> str:
    '''
    回答が要件に沿うよう修正する'''
    # Noneの場合変換　azureのバグlikeな挙動か？
    if answer is None:
        print('answer is None')
        answer = 'わかりません'

    # csvのフォーマットに合わせる
    answer = answer.replace('\n', '、')
    answer = answer.replace("'", '').replace('"', '')
    answer = answer.replace('- ', '')

    # トークン長が長すぎる回答は削除する
    enc = tiktoken.get_encoding('cl100k_base')
    if len(enc.encode(answer)) >= 54:
        answer = 'わかりません'

    return answer

def evaluate(query_path, pred_path):
    '''
    crag.pyによる評価を行う'''
    print('\nevaliation================')
    pred_dir = os.path.dirname(pred_path)
    command = [
        'python3', config.crag_path,
        '--result-dir', pred_dir,
        '--result-name', os.path.basename(pred_path),
        '--ans-dir', os.path.join(config.eval_dir, 'data'),
        '--eval-result-dir', pred_dir
    ]
    cr = subprocess.run(command)

    if cr.returncode != 0:
        raise RuntimeError

    # csv読み込み
    query_df = pd.read_csv(query_path)
    query_df.columns = ['index', 'query']
    answer_df = pd.read_csv(os.path.join(config.eval_dir, 'data', 'ans_txt.csv'))
    answer_df.columns = ['index', 'g_truth']
    pred_df = pd.read_csv(pred_path)
    pred_df.columns = ['index', 'prediction']
    score_df = pd.read_csv(os.path.join(pred_dir, 'scoring.csv'))
    score_df.columns = ['index', 'score', 'num_tokens']

    # スコアを数値に変換
    score_dic = {'Perfect': 1, 'Acceptable': 0.5, 'Missing': 0, 'Incorrect': -1}
    score_df['score'] = score_df['score'].replace(score_dic)

    # 結合して保存
    result_df = pd.merge(answer_df, pred_df, on='index')
    result_df = pd.merge(result_df, score_df, on='index')
    result_df = pd.merge(result_df, query_df, on='index')

    result_df.to_csv(os.path.join(pred_dir, 'evaluation.csv'), header=True, index=False, quoting=csv.QUOTE_ALL)
    os.remove(os.path.join(pred_dir, 'scoring.csv'))

def make_submission(csvpath:str):
    '''
    保存したcsvのパスを渡すと投稿用zipファイルを作成する'''
    savedir = os.path.dirname(csvpath)
    subpath = os.path.join(savedir, 'submission')
    os.mkdir(subpath)

    # submission/prediction.csv作成
    _ = shutil.copy(csvpath, subpath)

    # 圧縮
    shutil.make_archive('submission', format=zip, root_dir=savedir, base_dir='submission')
    # submission削除
    shutil.rmtree(subpath)

def get_answer(
    query:str,
    comlist_path:str = config.test_company_list,
    db_dir:str = config.test_db_dir
) -> str:
    '''
    query一つを渡すと関連情報を検索しllmで回答を得る'''
    pdf_num = company_extractor.gettxtpath(query, comlist_path)

    if pdf_num is None: # queryに企業名が含まれない場合
        return '不明'
    
    # 検索と関連情報の抽出
    db_path = os.path.join(db_dir, pdf_num+'.pdf')
    contexts = database.get_context(db_path, query, n_results=3)

    # プロンプト作成
    prompt = make_prompt.make_prompt(query, contexts)

    answer = getresponse_azure.getresponse(prompt)
    return answer

def answer_all_questions(isvalid:bool =False) -> None:
    '''
    query.csvを読み、全ての質問の回答を得、exportに出力する'''
    if isvalid: # validデータを使用する場合
        query_path = config.valid_query_path
        dirname = 'valid_' + datetime.datetime.now().strftime('%m%d-%H-%M-%S')
        comlist_path = config.valid_company_list
        db_dir = config.valid_db_dir
    else:
        query_path = config.test_query_path
        dirname = datetime.datetime.now().strftime('%m%d-%H-%M-%S')
        comlist_path = config.test_company_list
        db_dir = config.test_db_dir

    query_df = pd.read_csv(query_path)

    for i, j in enumerate(query_df.index):        
        query = query_df.loc[j, 'problem']

        # 回答
        answer = get_answer(
            query,
            comlist_path=comlist_path,
            db_dir=db_dir
        )

        answer = clean_answer(answer)
        query_df.loc[j, 'answer'] = answer

        print(f'{i} {query} : {answer}')
        # time.sleep(1)
    
    # 保存先のパス設定
    dirname = os.path.join(config.export_dir, dirname)
    os.mkdir(dirname)

    pred_path = os.path.join(dirname, 'predictions.csv')
    query_df.loc[:, ['index', 'answer']].to_csv(pred_path, index=False, header=False, quoting=csv.QUOTE_ALL)

    n_unknown = query_df['answer'].tolist().count('わかりません')
    print(f'\nわかりません : {n_unknown} answers')

    # evaluation
    if isvalid:
        evaluate(query_path, pred_path)

    # zip作成
    make_submission(pred_path)

if __name__ == '__main__':
    arg = sys.argv
    isvalid = False

    if len(arg) >= 2:
        if arg[1] == 'valid':
            isvalid = True
        elif arg[1] == 'test':
            pass
        else:
            raise ValueError

    print(f'isvalid : {isvalid}')

    answer_all_questions(isvalid)
