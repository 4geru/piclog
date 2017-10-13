# from app.lib.env import ENV
from env import ENV
import MeCab, copy, requests, re
import multiprocessing as multi

class Word:
  def __init__(self, word):
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse("")
    node = tagger.parseToNode(word).next
    self.surface = word
    self.feature = node.feature.split(",")[0]
 
class Sentence:
  def __init__(self, sentence, word):
    self.sentence = sentence
    if isinstance(word, str):
      self.word = Word(word)
    else:
      self.word = word
    # print("<<< " + str({ 'sentence' : sentence, 'word': word}))
    
  def print(self):
    print(self.sentence)
    return self.sentence
  
  def print_mecab(self):
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse("")
    self.node = tagger.parseToNode(self.sentence)
    node = self.node
    while node:
      feature = node.feature.split(",")[0]
      surface = node.surface.split(",")[0]
      if feature == 'BOS/EOS' : 
        node = node.next
        continue
      print("{0} -> {1}".format(surface,feature))
      node = node.next
  
  def set_word(self, word):
    self.word = Word(word)
  
  def match_feature(self, word):
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse("")
    self.node = tagger.parseToNode(self.sentence)
    node = self.node
    same_cnt = 0 # 同じ品詞を数える
    diff_count = 0 # 違う品詞を数える
    sentence = ''
    word_flag = False
    end = self.sentence.rfind(self.word.surface)
    
    # print({ 'end': self.sentence[0:end] })
    # print({ 'find': self.sentence.find(self.word.surface) })
    # print(self.sentence)
    # print({ 'b4match_feature:word': word.surface , 'feature': word.feature, 'word': self.word.surface})
    while node:
      feature = node.feature.split(",")[0]
      surface = node.surface.split(",")[0]
      if feature == 'BOS/EOS' : 
        node = node.next
        continue
      # print(surface)
      # print(sentence, word_flag)
      if surface == self.word.surface :
        # print('match')
        sentence += surface
        node = node.next
        word_flag = True
        continue
      if word_flag:
        if feature == word.feature:
          # print("{3} {0} -> {1} match {2}".format(surface,feature, word.surface, word_flag))
          if same_cnt == 1 and diff_count >= 0:
            return sentence + word.surface
          same_cnt += 1
        else:
          # print("{2} {0} -> {1}".format(surface,feature,word_flag))
          diff_count += 1
        
      sentence += surface
      
      
      node = node.next
    # print({ 'match_sentence': sentence + word.surface })
    return sentence + word.surface
    
  def get_proofreading(self):
    payload = {'apikey': ENV('PROOFREADING_KEY'), 'sentence': self.sentence}
    self.proofreading = requests.get('https://api.a3rt.recruit-tech.co.jp/proofreading/v1/typo', params=payload).json()
    return self.proofreading
    
  def get_text_suggest(self):
    payload = {'apikey': ENV('TEXT_SUGGEST_KEY'), 'previous_description': self.sentence}
    self.text_suggest = requests.get('https://api.a3rt.recruit-tech.co.jp/text_suggest/v2/predict', params=payload).json()
    
    # 一番良い文を選ぶ
    self.get_best_sentence(self.word)
    # print({ 'text_suggect': self.text_suggest })
    # print({ 'best_sentence': self.get_best_sentence() })
    return self.text_suggest
    
  def get_best_sentence(self, word):
    best_sentence = [1, '']
    # print({ 'suggestion': self.text_suggest['suggestion'] })
    for text in self.text_suggest['suggestion']:
      # 数字が入っている文字列はスキップ
      if  re.search(r"[一|二|三|四|五|六|七|八|九|十|0-9]", text) != None:
        # print({ 'continue': text})
        continue
      
      # 生成された文
      next_sentence = Sentence(self.sentence + text, word)
      # print({ 'next_sentence': next_sentence.sentence })
      proofreading_json = next_sentence.get_proofreading()
      # print(proofreading_json)
      if proofreading_json['status'] == 0:
        # print({ 'status == 0' : text })
        self.best_sentence = next_sentence
        self.best_sentence_score = 0
        return [0, next_sentence]
      maxRankingScore = 0
      for alert in proofreading_json['alerts'] :
        # print(alert['rankingScore'])
        if maxRankingScore < alert['rankingScore']:
          maxRankingScore = alert['rankingScore']
      if best_sentence[0] > maxRankingScore:
        best_sentence = [maxRankingScore, next_sentence]
      # print('maxx', maxRankingScore, next_sentence.sentence)
      
    [self.best_sentence_score, self.best_sentence] = best_sentence
    return best_sentence

if __name__ == "__main__":
  """ ファイルを実行に動作 """
  words = ['トラック', 'アウトドア', '競走', '群', '男性', '人々', '上', 'ケーキ', 'オートバイ', '土', '沢山', '丘', '浜', 'お召し', '躍り', '水', '自転車', '原告適格', '空気']
  
  word = words[0]
  sentence = Sentence(word, word)
  sentence.get_text_suggest()
  # print(sentence.get_text_suggest())
  # print({ 'run': sentence.best_sentence.sentence})
  sentence = sentence.best_sentence
  
  # print({ 'run': sentence.sentence })
  times = 0
  while True:
    times += 1
    # if times == 3:
    #   break
    print("THIS IS TIME !!!" + str(times) + ">>>>>")
    best_sentence_by_word = [1, Sentence('', '')]
    
    # -- 逐次 -- 
    for word in words[times::]:
      _sentence = copy.deepcopy(sentence)
      print(word, end="")
      # print({ '_sentence':_sentence.sentence })
      # print(word)
      new_line = _sentence.match_feature(Word(word))
      # print({ 'newline': new_line})
      new_sentence = Sentence(new_line, word)
      new_sentence.get_text_suggest()
      # print({ 'run': new_sentence.best_sentence.sentence})
      # print({ 'run': new_sentence.best_sentence_score})
      if best_sentence_by_word[0] > new_sentence.best_sentence_score:
        score = new_sentence.best_sentence_score
        best_sentence_by_word = [score, new_sentence.best_sentence]
      # break
    # -- end --
    # print(len(best_sentence_by_word[1].sentence))
    if len(best_sentence_by_word[1].sentence) >= 140:
      break
    else:
      # print({ "best_sentence_by_word" : best_sentence_by_word[1].word.surface})
      sentence = best_sentence_by_word[1]
    # print(type(best_sentence_by_word[1]))
    # break
    print({ 'next_sentence':best_sentence_by_word[1].sentence })
    print({ 'next_sentence':best_sentence_by_word[1].word.surface })
  print(sentence.sentence)
    # break
    # break
    # print({ 'run': sentence.match_feature(Word(word)) })
  # word = Word('犬')
  # print(word.feature)
  # print(word.surface)
  # sentence = Sentence('アウトドア日の部屋は滋賀です。')
  # sentence.print()
  # sentence.print_mecab()
  # sentence.set_word('日')
  # print(sentence.match_feature(word))