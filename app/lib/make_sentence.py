import requests, random, json, MeCab
from app.lib.env import ENV
# from env import ENV

def make_sentence(words):
  """
  作文を行う
  @param  words : 単語リスト
  @return 日本語文を返す
  """
  prev_sentence = words[0]
  word = ""
  for w in range(0, len(words)):
    check_sentence = 4
    check_used_word = 4
    index = w
    while True:
      # Predict APIを実行
      payload = {'apikey': ENV('TEXT_SUGGEST_KEY'), 'previous_description': prev_sentence}
      json = requests.get('https://api.a3rt.recruit-tech.co.jp/text_suggest/v2/predict', params=payload).json()
      # 提案してきた文字列が長ければ作文を終了する
      if len(prev_sentence + json['suggestion'][0]) > 140 :
        return prev_sentence
      # 次のワードの瀕死を抽出
      tagger = MeCab.Tagger('-Ochasen')
      
      # 携帯基礎解析を行う
      node = tagger.parseToNode(words[index+1])
      next_feature = node.next.feature.split(',')[0]
      
      cnt = 4 # 間に追加する文字数を選択
      
      # 次の状態を next_sentenceとして保存
      next_sentence = prev_sentence
      node = tagger.parseToNode(json['suggestion'][0])
      
      # suggestion文の各要素の品詞を確認
      while node:
        feature = node.feature.split(",")[0]
        surface = node.surface.split(",")[0]
        # 品詞が同じ && 表現がwordsの中に含まれる && 同じ処理を4回繰り返していなければ
        if feature == next_feature and surface in words and check_used_word != 0 :
          # 処理のカウント回数を減らす
          check_used_word -= 1
          # 単語を置き換える
          index = random.randrange(len(words)-1)
          continue
        # 同じ品詞であれば
        elif feature == next_feature:
          # 追加する文字カウントを減らす
          cnt -= 1
          # 処理カウントを減らす
          check_used_word = 4
          # 4 word文中に追加したら終了する
          if cnt == 0 : break 
        # if文に反応しなければ提案された単語を追加する
        next_sentence += node.surface
        # 次のノードへ遷移する
        node = node.next
      
      # 添削を行う
      payload = {'apikey': ENV('PROOFREADING_KEY'), 'sentence': next_sentence + words[index+1]}
      json = requests.get('https://api.a3rt.recruit-tech.co.jp/proofreading/v1/typo', params=payload).json()
      # status が 1 or 0 or checkを4回行った
      if json['status'] == 0 or json['status'] == 1 or check_sentence == 0:
        break
      check_sentence -= 1
    # 文字を追加
    
    prev_sentence = next_sentence 
  return prev_sentence
  
if __name__ == "__main__":
  """
  ファイルを実行に動作
  @return None
  """
    
  words = ['投げる','ピッチャー','ボール','ユニフォーム','野球','バッター','試合','打','球','サッカー','チーム','選手','赤い','着','する','緑','球場','バット','人','テニス']
  sentence = make_sentence(words)
  print(sentence)
  print(len(sentence))