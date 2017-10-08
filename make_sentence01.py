# -*- coding: utf-8 -*-

import requests, random, json, MeCab

def request_predict(sentence):
    payload = {'apikey': 'EtEj5GxZF4uyobFKkoyfo3h7UKCONn2I', 'previous_description': sentence, 'separation': 2}
    predict_json = requests.get('https://api.a3rt.recruit-tech.co.jp/text_suggest/v2/predict', params=payload).json()
    print("predict >> length {0}!".format(len(predict_json['suggestion'])))
    return predict_json

def request_typo(sentence):
    payload = {'apikey': 'a6WEeoq1GLUbSsYL10BHJB4QsNNS8SH1', 'sentence': sentence}
    typo_json = requests.get('https://api.a3rt.recruit-tech.co.jp/proofreading/v1/typo', params=payload).json()
    print(sentence)
    if typo_json['status'] != 0:
        alert_status = 0
        for alert in typo_json['alerts']:
            print( alert['rankingScore'])
            alert_status = max(alert_status, alert['rankingScore'])
        print("alert_status >> " + str(alert_status))
    else : 
        print(0)
    return typo_json
    
def select_best(before, suggestion):
    best_sentence = [1,'']
    for suggestion in suggestion:
        print(len(suggestion))
        if len(suggestion) < 8:
            continue
        typo_json = request_typo(before + suggestion)
    
    return 'hello'
    
def main(words):
    # original http://farm4.staticflickr.com/3450/3372087016_5176833783_z.jpg
    # words = ['スキー','ウェア','ゼッケン','滑る','着','子供','する','フープ','フラ','選手','付け','ヘルメット','雪','赤い','ピンク','女性','つけ','競技','回し','男性']
    used_words = []
    prev_sentence = ''
    sentence = ''
    word = words[0]
    idx = 0
    time = 0
    while len(sentence) < 120 and time < 10:
        print(time)
        # 作文
        predict_json = request_predict(sentence + word)
        
        accept_sentence = None
        print(predict_json)
        best_sentence = select_best(sentence + word, predict_json['suggestion'])
        
        
        break
        idx = random.randrange(len(words)-1) # 次のindexを設定
        word = words[idx]
    
    print(prev_sentence)    
    print(used_words)
