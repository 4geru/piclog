# -*- coding: utf-8 -*-

import requests, random, json
from lib.env import ENV

def request_predict(sentence):
    payload = {'apikey': ENV('TEXT_SUGGEST_KEY'), 'previous_description': sentence, 'separation': 2}
    predict_json = requests.get('https://api.a3rt.recruit-tech.co.jp/text_suggest/v2/predict', params=payload).json()
    # print("predict >> length {0}!".format(len(predict_json['suggestion'])))
    return predict_json

def request_typo(sentence):
    payload = {'apikey': ENV('PROOFREADING_KEY'), 'sentence': sentence}
    typo_json = requests.get('https://api.a3rt.recruit-tech.co.jp/proofreading/v1/typo', params=payload).json()
    return typo_json

def select_best(before, suggestion):
    best_sentence = [1,'']
    for suggestion in suggestion:
        if len(suggestion) < 8:
            continue
        sentence = before + suggestion
        typo_json = request_typo(sentence)
        # print(sentence)
        if typo_json['status'] != 0:
            alert_status = 0
            for alert in typo_json['alerts']:
                # print(alert['rankingScore'])
                alert_status = max(alert_status, alert['rankingScore'])
            # print("alert_status >> " + str(alert_status) + ' ' + sentence)
            if best_sentence[0] > alert_status:
                best_sentence = [alert_status, sentence]
        else : 
            best_sentence = [0, sentence]
            # print("alert_status >> 0 " + sentence)
    # print(best_sentence)
    return best_sentence[1]
    
def main(words = None):
    # original http://farm4.staticflickr.com/3450/3372087016_5176833783_z.jpg
    if words == None:
        words = ['スキー','ウェア','ゼッケン','滑る','着','子供','する','フープ','フラ','選手','付け','ヘルメット','雪','赤い','ピンク','女性','つけ','競技','回し','男性']
    used_words = []
    sentence = ''
    word = words[0]
    idx = 0
    while len(sentence) < 120:
        # 作文
        predict_json = request_predict(word)
        
        accept_sentence = None
        best_sentence = select_best(word, predict_json['suggestion'])
        # print("best_sentence " + best_sentence)
        
        # 文章の長さを判定
        if len(sentence + best_sentence) > 140:
            break
        # 文章に既に使われていたら
        sentence += best_sentence
        indexs = []
        for i in range(0,len(words)):
            if words[i] in best_sentence:
                indexs.append(i)
        indexs.reverse()
        for i in indexs:
            used_words.append(words[i])
            words.pop(i)
        idx = random.randrange(len(words)-1) # 次のindexを設定
        word = words[idx]
    return sentence
    
# print(main())
