import requests, random, json, MeCab
from env import ENV

def make(words):
  prev_sentence = words[0]
  bf = 0
  for w in range(0,5) :
    # predict API
    check_sentence = 4
    check_used_word = 4
    index = w
    
    while True:
      # print('<< retry >> ')
      payload = {'apikey': ENV('TEXT_SUGGEST_KEY'), 'previous_description': prev_sentence}
      json = requests.get('https://api.a3rt.recruit-tech.co.jp/text_suggest/v2/predict', params=payload).json()
      
      # 次のワードの瀕死を抽出
      tagger = MeCab.Tagger('-Ochasen')
      node = tagger.parseToNode(words[index+1])
      next_feature = node.next.feature.split(',')[0]
      
      cnt = 4 # 間に追加する文字数を選択
      word = prev_sentence + json['suggestion'][0]
      next_words = prev_sentence
      node = tagger.parseToNode(json['suggestion'][0])
      while node:
        feature = node.feature.split(",")[0]
        surface = node.surface.split(",")[0]
        # print(node.surface, pos)
        if feature == next_feature and surface in words and check_used_word != 0 :
          # print('used same word')
          check_used_word -= 1
          index = random.randrange(len(words)-1)
          continue
        elif feature == next_feature:
          cnt -= 1
          check_used_word = 4
          if cnt == 0 : break 
        # print(node.surface, pos)
        next_words += node.surface
        node = node.next
      
      # print(next_words + words[index+1])
    
      payload = {'apikey': ENV('PROOFREADING_KEY'), 'sentence': next_words + words[index+1]}
      json = requests.get('https://api.a3rt.recruit-tech.co.jp/proofreading/v1/typo', params=payload).json()
      if json['status'] == 0 or check_sentence == 0:
        break
      elif json['status'] == 1 or check_sentence == 0:
        # for alert in json['alerts']:
          # print("status 1 : " + alert['checkedSentence'])
        break
      # else:
      #   print(json)
      check_sentence -= 1
    # 文字を追加
    prev_sentence = next_words + words[index+1]
    bf = len(prev_sentence)
    # print(next_words + words[index+1])
  
  # 文末に文字を追加
  payload = {'apikey': ENV('TEXT_SUGGEST_KEY'), 'previous_description': prev_sentence}
  r = requests.get('https://api.a3rt.recruit-tech.co.jp/text_suggest/v2/predict', params=payload)
  json = r.json()
  return prev_sentence + json['suggestion'][0]
# print(prev_sentence + json['suggestion'][0])
# print(len(prev_sentence+json['suggestion'][0]))
words = ['投げる','ピッチャー','ボール','ユニフォーム','野球','バッター','試合','打','球','サッカー','チーム','選手','赤い','着','する','緑','球場','バット','人','テニス']

print(make(words))