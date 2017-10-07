import requests
import random
words = ['投げる','ピッチャー','ボール','ユニフォーム','野球','バッター','試合','打','球','サッカー','チーム','選手','赤い','着','する','緑','球場','バット','人','テニス']

r = {'status' : 1}
while r['status'] == 1:

  sentence = ''

  for word in words :
    sentence += word

  payload = {'apikey': '_api_key_', 'sentence': sentence}
  r = requests.get('https://api.a3rt.recruit-tech.co.jp/proofreading/v1/typo', params=payload).json()
  print(len(r['alerts']))
  print(sentence)
  print('original >> ')
  print(words)
  alert = r['alerts'][0]
  index = words.index(alert['word'])
  words = words[0:index-1] + [words[index]] + [words[index-1]] + words[index+1:len(words)]
  print(alert['word'])
  print(words)
  # for alert in r['alerts']:
  #   print(alert['checkedSentence'])
  #   index = words.index(alert['word'])
  #   print(index)
  #   print(words[0:index-1] + [words[index]] + [words[index-1]] + words[index+1:len(words)])
  #   print(alert['word'])

  # break