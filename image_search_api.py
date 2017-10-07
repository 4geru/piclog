import requests
import random
import json
import MeCab
words = ['投げる','ピッチャー','ボール','ユニフォーム','野球','バッター','試合','打','球','サッカー','チーム','選手','赤い','着','する','緑','球場','バット','人','テニス']

prev_sentence = words[0]
for w in range(0,4) :
  # predict API
  payload = {'apikey': 'EtEj5GxZF4uyobFKkoyfo3h7UKCONn2I', 'previous_description': prev_sentence}
  json = requests.get('https://api.a3rt.recruit-tech.co.jp/text_suggest/v2/predict', params=payload).json()
  
  # 次のワードの瀕死を抽出
  tagger = MeCab.Tagger('-Ochasen')
  node = tagger.parseToNode(words[w+1])
  feature = node.next.feature.split(',')[0]
  
  cnt = 2 # 間に追加する文字数を選択
  word = prev_sentence + json['suggestion'][0]
  next_words = prev_sentence
  node = tagger.parseToNode(json['suggestion'][0])
  while node:
    pos = node.feature.split(",")[0]
    print(node.surface, pos)
    if pos == feature :
      cnt -= 1
      if cnt == 0 : break 
    print(node.surface, pos)
    next_words += node.surface
    node = node.next

  # 文字を追加
  prev_sentence = next_words + words[w+1]
  print(next_words + words[w+1])
  
# 文末に文字を追加
payload = {'apikey': 'EtEj5GxZF4uyobFKkoyfo3h7UKCONn2I', 'previous_description': prev_sentence}
r = requests.get('https://api.a3rt.recruit-tech.co.jp/text_suggest/v2/predict', params=payload)
json = r.json()
print(prev_sentence + json['suggestion'][0])