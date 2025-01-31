import os
import shutil
import pandas as pd
import time
import datetime
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
    回答に改行等が含まれると評価時にエラーとなるので除く'''
    answer = answer.replace('\n', '、').replace(',', '、')
    answer = answer.replace("'", '').replace('"', '')
    answer = answer.replace('- ', '')
    return answer

def make_submission(csvpath:str):
    '''
    保存したcsvのパスを渡すと投稿用zipファイルを作成する'''
    savedir = os.path.dirname(csvpath)
    subpath = os.path.join(savedir, 'submission')
    os.mkdir(subpath)

    # submission/prediction.csv作成
    _ = shutil.copy(csvpath, subpath)

    # 圧縮
    shutil.make_archive(subpath, format=zip, root_dir=savedir, base_dir='submission')
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
        return 'わかりません'
    
    # 検索と関連情報の抽出
    db_path = os.path.join(db_dir, pdf_num+'.pdf')
    contexts = database.get_context(db_path, query, n_results=3)

    # プロンプト作成
    prompt = make_prompt.make_prompt(query, contexts)

    answer = getresponse_azure.getresponse(prompt)
    return answer

def answer_all_questions() -> None:
    '''
    query.csvを読み、全ての質問の回答を得、exportに出力する'''
    query_df = pd.read_csv(config.test_query_path)

    for i, j in enumerate(query_df.index):        
        query = query_df.loc[j, 'problem']

        # 回答
        answer = get_answer(query)

        answer = clean_answer(answer)
        query_df.loc[j, 'answer'] = answer

        print(f'{i} {query} : {answer}')
        time.sleep(1)
    
    # 保存先のパス設定
    dirname = datetime.datetime.now().strftime('%m%d-%H-%M-%S')
    dirname = os.path.join(config.export_dir, dirname)
    os.mkdir(dirname)

    pred_path = os.path.join(dirname, 'predictions.csv')
    query_df.loc[:, ['index', 'answer']].to_csv(pred_path, index=False, header=False)

    n_unknown = query_df['answer'].tolist().count('わかりません')
    print(query_df)
    print(f'わかりません : {n_unknown} answers')

    # zip作成
    make_submission(pred_path)

if __name__ == '__main__':
    answer_all_questions()
