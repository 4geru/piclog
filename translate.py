import requests, json

def translate(word): 
    payload = {'from': 'en', 'dest': 'ja', 'format': 'json', 'phrase': word, 'pretty': 'true'}
    r = requests.get('https://glosbe.com/gapi/translate', params=payload)
    japanese = r.json()['tuc'][0]['phrase']['text']
    print(japanese)
    return japanese
    
def translate_array(english_words):
    japanese_words = []
    for word in english_words:
        japanese_words.append(translate(word))
    return japanese_words
# print(japanese_words)