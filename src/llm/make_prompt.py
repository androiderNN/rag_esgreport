def make_prompt(query:str, contexts:list[str]) -> str:
    '''
    データベースから取得した関連情報を使用してクエリを作成する'''
    # system_prompt = (
    #     'あなたは優秀なAIアシスタントです。\n'
    #     'ユーザーが与えた情報だけをもとに回答してください。'
    #     '情報がコンテキストに含まれない場合は『わかりません』と答えてください。\n'
    #     '回答は、下記の例のように可能な限り簡潔に行ってください。\n'
    #     '回答には必要な情報のみを記述し、可能であれば単語で答えてください。質問文の情報や解説は含めてはいけません。'
    #     'また、数値に関する質問では、指定された単位を用いて回答してください。\n\n'
    #     '回答例\n'
    #     '良い例：\n'
    #     '営業利益が最高の年は何年ですか？ - 2023年\n'
    #     '従業員数は2018年から2024年までに何％増加したか。 - 34%\n'
    #     '悪い例：\n'
    #     '従業員数は2018年から2024年までに何％増加したか。 - 従業員数は、2018年が998人、2024年が1340人のため、34%増加しています。\n'
    # )
    
    system_prompt = (
        'あなたは優秀なAIアシスタントです。\n'
        'ユーザーが与えた情報だけをもとに回答してください。'
        '情報がコンテキストに含まれない場合は『わかりません』と答えてください。\n'
        '回答は、可能な限り簡潔に行ってください。\n'
        '回答には必要な情報のみを記述し、可能であれば単語で答えてください。質問文の情報や計算過程は含めてはいけません。'
        'また、数値に関する質問では、指定された単位を用いて回答してください。\n'
        'あなたの回答はcsvファイルに挿入します。このため、文中には改行や「,」は使用せず、区切り文字には「、」を使用してください。\n'
        '回答には文字数の制限が存在します。最大でも40文字以内で出力してください。\n\n'
        '回答例\n'
        '良い例：\n5%\n2450億円\n中国\n'
        '悪い例：\n国内の売り上げは500億円、海外の売上は2000億円なので、海外の方が多い\n14,342億円\n'
    )
    
    user_prompt = (
        '以下のコンテキストを参考に回答をしてください。\n'
        '質問:\n'
        f'{query}\n\n'
        'コンテキスト:\n'
        '\n\n'.join(contexts)
    )

    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]

    return messages
