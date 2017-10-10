
from multiprocessing import Pool
import requests, json
import multiprocessing as multi
import time

class translate:
    """ 翻訳に関するclass """
    def __init__(self, english_words):
        """ 英単語を翻訳する """
        # 並列処理をしている
        p = Pool(len(english_words))
        self.japanese_words = p.map( self.get_translate, english_words )
        p.close()
        
    def get(self):
        return self.japanese_words
        
    def get_translate(self, word):
        """ 1ワードを翻訳 """
        payload = {'from': 'en', 'dest': 'ja', 'format': 'json', 'phrase': word, 'pretty': 'true'}
        r = requests.get('https://glosbe.com/gapi/translate', params=payload)
        japanese = r.json()['tuc'][0]['phrase']['text']
        return japanese
    