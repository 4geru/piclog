
from multiprocessing import Pool
import requests, json

def translate(word): 
    payload = {'from': 'en', 'dest': 'ja', 'format': 'json', 'phrase': word, 'pretty': 'true'}
    r = requests.get('https://glosbe.com/gapi/translate', params=payload)
    japanese = r.json()['tuc'][0]['phrase']['text']
    print(japanese)
    return japanese
    
def translate_array(english_words):
    p = Pool(16)
    japanese_words = p.map( translate, english_words )
    return japanese_words
# print(japanese_words)