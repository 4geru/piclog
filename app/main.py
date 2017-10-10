import re
import app.lib.image_analizer
import app.lib.translate
import app.lib.make_sentence
import app.lib.make_pdf
from app.lib.env import ENV

def main(argv):
  # このコードは引数と標準出力を用いたサンプルコードです。
  # このコードは好きなように編集・削除してもらって構いません。
  # ---
  # This is a sample code to use arguments and outputs.
  # Edit and remove this code as you like.

  argc = len(argv) # 引数の個数
  if argc != 1:
    print('ERROR : PLEASE INPUT URL')
    return False
  if not re.match(r"http", argv[0]):
    print('ERROR : INPUT IS NOT URL')
  img = argv[0]
  # analyze 単語(DescriptionのTags) -> words
  print("analyze image\t>> doing", end="")
  english_words = app.lib.image_analizer.analyze(img)
  # print(english_words)
  print(' >> finished')
    
  # translate 英単語 -> 日本語単語
  print('translate words\t>> doing', end="")
  japanese_words = app.lib.translate.translate_array(english_words)
  #print(japanese_words)
  print(' >> finished')
    
  # make_sentence00 日本語単語 -> 文
  print('make sentence\t>> doing', end="")
  sentence = app.lib.make_sentence.main(japanese_words)
  # print(sentence)
  print(' >> finished')
    
  # make_pdf 文 -> pdf
  print('make pdf\t>> doing', end="")
  app.lib.make_pdf.make(sentence,img)
  print(' >> finished')