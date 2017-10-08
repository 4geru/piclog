# -*- coding: utf-8 -*-

import requests, random, json, MeCab

def api_search(query):
    payload = {'apikey': 'o9gtfHaCYjvQgc4cjGXH3JuGJZLw4571', 'query': query}
    search_by_image_json = requests.get('https://api.a3rt.recruit-tech.co.jp/image_search/v1/search_by_image', params=payload).json()
    print(search_by_image_json['result']['txt'])
    
def search_random():
    payload = {'apikey': 'o9gtfHaCYjvQgc4cjGXH3JuGJZLw4571'}
    random_json = requests.get('https://api.a3rt.recruit-tech.co.jp/image_search/v1/random', params=payload).json()
    for img in random_json['result']['img']:
        api_search(img['id'])
    
# search_random()

# api_search(3644)