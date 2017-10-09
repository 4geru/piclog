
from multiprocessing import Pool
import requests, json
import multiprocessing as multi
import time
def translate(word): 
    payload = {'from': 'en', 'dest': 'ja', 'format': 'json', 'phrase': word, 'pretty': 'true'}
    r = requests.get('https://glosbe.com/gapi/translate', params=payload)
    japanese = r.json()['tuc'][0]['phrase']['text']
    return japanese
    
def translate_array(english_words):
    p = Pool(len(english_words))
    japanese_words = p.map( translate, english_words )
    p.close()
    return japanese_words