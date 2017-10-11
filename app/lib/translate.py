
from multiprocessing import Pool
import requests, json
import multiprocessing as multi
import time

def translate(english_words):
    """ 英単語リストを翻訳する """
    # 並列処理をしている
    p = Pool(len(english_words))
    japanese_words = p.map( get_translate, english_words )
    p.close()
    return japanese_words
    
def get_translate(word):
    """ 1ワードを翻訳 """
    payload = {'from': 'en', 'dest': 'ja', 'format': 'json', 'phrase': word, 'pretty': 'true'}
    r = requests.get('https://glosbe.com/gapi/translate', params=payload)
    japanese = r.json()['tuc'][0]['phrase']['text']
    return japanese
