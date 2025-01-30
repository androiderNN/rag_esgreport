import os
import shutil
import numpy as np
from dotenv import load_dotenv
from openai import AzureOpenAI
import chromadb
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
API_VERSION = os.getenv('API_VERSION')
DEPLOYMENT_ID_FOR_CHAT_COMPLETION = os.getenv('DEPLOYMENT_ID_FOR_CHAT_COMPLETION')
DEPLOYMENT_ID_FOR_EMBEDDING = os.getenv('DEPLOYMENT_ID_FOR_EMBEDDING')

def azure_embedding_fn(text: str|list[str]) -> list[list]:
    '''
    strまたはstrのlistを渡すとazureのapiでembeddingする'''
    client = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=API_VERSION
    )

    response = client.embeddings.create(
        input=text,
        model=DEPLOYMENT_ID_FOR_EMBEDDING,
    )
    
    embedding = [data.embedding for data in response.data]
    return embedding

def save_db(name:str, texts:list[str], path:str) -> None:
    '''
    pdf1ファイル分のデータベースを作成しpathに保存する'''
    # databaseが既に存在する場合削除する
    if os.path.exists(path):
        shutil.rmtree(path)

    chroma_client = chromadb.PersistentClient(path=path)
    collection = chroma_client.create_collection(name=name)

    collection.add(
        documents=texts,
        # embeddings=azure_embedding_fn(texts),
        ids=[str(i) for i in range(len(texts))]
    )

    chroma_client.close()

def text2db(textdir:str, dbdir:str) -> None:
    '''
    全ファイルのデータベースを保存する'''
    texts = [f for f in os.listdir(textdir) if f[-4:]=='.txt']

    for txtfile in texts:
        print(txtfile)
        dbname = os.path.splitext(txtfile)[0]
        textpath = os.path.join(textdir, txtfile)
        dbpath = os.path.join(dbdir, dbname)

        with open(textpath) as f:
            text = f.read()

        splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size=100,
            chunk_overlap=5
        )
        text = splitter.split_text(text)

        save_db(name=dbname, texts=text, path=dbpath)
        break

def load_db(path:str) -> chromadb.Collection:
    '''
    databaseのパスを渡すとdatabaseを読み込んで返す'''
    name = os.path.basename(path)
    client = chromadb.PersistentClient(path)
    collection = client.get_collection(name)
    return collection

def get_context(db_path:str, query:str, n_results:str =5):
    '''
    databaseのパスとクエリ、返答数を渡すと、関連するドキュメントを検索して返す'''
    db = load_db(db_path)

    result = db.query(
        query_texts=query,
        n_results=n_results
    )
    return result
