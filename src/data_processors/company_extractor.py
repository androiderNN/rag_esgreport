
def save_company_list(train_list_path:str, valid_list_path:str) -> None:
    '''
    企業名とレポート番号の対応表を保存する'''
    train_company_dict = {
        '4℃': '1',
        'IHI': '2',
        '日産': '3',
        'カゴメ': '4',
        'キッツ': '5',
        'クレハ': '6',
        'グローリー': '7',
        'サントリー': '8',
        'ハウス食品': '9',
        'パナソニック': '10',
        'メディアドゥ': '11',
        'モス': '12',
        'ライフ': '13',
        '高松': '14',
        '全国保証': '15',
        '東急不動産': '16',
        '東洋エンジニアリング': '17',
        '日清食品': '18',
        '明治': '19'
    }
    valid_company_dict = {
    'ウエルシア': '1',
    'エクシオ': '2',
    'ダイドー': '3',
    '花王': '4',
    '太陽誘電': '5',
    '大成温調': '6',
    '大和ハウス': '7',
    '電通': '8',
    '東洋紡': '9',
    '日本化薬': '10',
}

    # trainの保存
    train_list = [i[0]+', '+i[1] for i in train_company_dict.items()]

    with open(train_list_path, mode='w') as f:
        f.write('\n'.join(train_list))
    
    # validの保存
    valid_list = [i[0]+', '+i[1] for i in valid_company_dict.items()]

    with open(valid_list_path, mode='w') as f:
        f.write('\n'.join(valid_list))
    
    print('list updated')

def gettxtpath(query:str, company_list_path:str) -> str:
    '''
    質問文と対象のcompany_listのパス(train/valid)を渡すと、
    質問文に関連する企業のファイル番号を返す'''
    company_dict = dict()
    with open(company_list_path, mode='r') as f:
        for l in f:
            l = l.rstrip().split(', ')
            company_dict[l[0]] = l[1]

    comlist = [c for c in company_dict.keys() if query.find(c) >= 0]
    n = len(comlist)

    if n == 0:
        # queryに企業名が含まれない
        return None
    elif n == 1:
        # queryに一社の企業名のみがふくまれる
        return company_dict[comlist[0]]
    elif n >= 2:
        # queryに2社以上の企業名が含まれる
        return None
